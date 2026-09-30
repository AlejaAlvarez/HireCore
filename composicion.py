from typing import Callable, Optional

from hirecore.auditoria import AuditorDeCambios, RepositorioAuditoriaEnMemoria
from hirecore.comandos import HistorialDeCambios
from hirecore.etapas import (
    Aplicado,
    Contratado,
    Entrevista,
    Etapa,
    FlujoDeSeleccion,
    NaturalezaEtapa,
    Oferta,
    PruebaTecnica,
    Rechazado,
    VerificacionReferencias,
)
from hirecore.eventos import PublicadorDeEventos
from hirecore.gestor import GestorDeCandidato
from hirecore.notificacion import (
    CanalCorreo,
    CanalDeNotificacion,
    CanalPortal,
    DestinatarioCandidato,
    DestinatarioFijo,
    DestinatarioReclutador,
    Notificador,
    ReglaPorNaturaleza,
    ReglaSiempre,
    ReglaVisibleParaCandidato,
)

CORREO_GERENTE = "gerente.contratacion@empresa.com"
CORREO_NOMINA = "nomina@empresa.com"


def construirEtapas() -> dict[str, Etapa]:
    etapas = [
        Aplicado(),
        Entrevista(),
        PruebaTecnica(),
        VerificacionReferencias(),
        Oferta(),
        Contratado(),
        Rechazado(),
    ]
    return {etapa.id(): etapa for etapa in etapas}


def construirFlujo(etapas: dict[str, Etapa]) -> FlujoDeSeleccion:
    flujo = FlujoDeSeleccion()
    camino = ["APLICADO", "ENTREVISTA", "PRUEBA_TECNICA", "VERIFICACION_REFERENCIAS", "OFERTA", "CONTRATADO"]
    for origen, destino in zip(camino, camino[1:]):
        flujo.permitir(etapas[origen], etapas[destino])
    for origen in camino[:-1]:
        flujo.permitir(etapas[origen], etapas["RECHAZADO"])
    return flujo


def construirSistema(
    canalCorreo: Optional[CanalDeNotificacion] = None,
    canalPortal: Optional[CanalDeNotificacion] = None,
    profundidadMaxima: int = 1,
    configurarFlujo: Optional[Callable[[FlujoDeSeleccion, dict[str, Etapa]], None]] = None,
):
    correo = canalCorreo or CanalCorreo()
    portal = canalPortal or CanalPortal()
    etapas = construirEtapas()
    repositorio = RepositorioAuditoriaEnMemoria()
    publicador = PublicadorDeEventos()
    publicador.suscribir(AuditorDeCambios(repositorio))
    publicador.suscribir(Notificador(ReglaSiempre(), DestinatarioReclutador(), correo))
    publicador.suscribir(
        Notificador(
            ReglaPorNaturaleza([NaturalezaEtapa.DECISION, NaturalezaEtapa.CIERRE_POSITIVO]),
            DestinatarioFijo(CORREO_GERENTE),
            correo,
        )
    )
    publicador.suscribir(
        Notificador(
            ReglaPorNaturaleza([NaturalezaEtapa.CIERRE_POSITIVO]),
            DestinatarioFijo(CORREO_NOMINA),
            correo,
        )
    )
    publicador.suscribir(Notificador(ReglaVisibleParaCandidato(), DestinatarioCandidato(), portal))
    flujo = construirFlujo(etapas)
    if configurarFlujo:
        configurarFlujo(flujo, etapas)
    gestor = GestorDeCandidato(
        flujo,
        HistorialDeCambios(profundidadMaxima),
        publicador,
    )
    return gestor, etapas, repositorio
