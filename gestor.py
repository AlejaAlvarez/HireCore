from hirecore.candidato import Candidato
from hirecore.comandos import CambiarEtapa, Comando, HistorialDeCambios
from hirecore.etapas import Etapa, FlujoDeSeleccion
from hirecore.eventos import PublicadorDeEventos


class GestorDeCandidato:
    def __init__(
        self,
        flujo: FlujoDeSeleccion,
        historial: HistorialDeCambios,
        publicador: PublicadorDeEventos,
    ) -> None:
        self._flujo = flujo
        self._historial = historial
        self._publicador = publicador

    def avanzar(self, candidato: Candidato, destino: Etapa, actorId: str) -> None:
        if not self._flujo.permite(candidato.etapa(), destino):
            raise ValueError(
                f"Transición inválida: {candidato.etapa().id()} -> {destino.id()}"
            )
        comando: Comando = CambiarEtapa(candidato, destino, actorId)
        evento = comando.ejecutar()
        self._historial.registrar(candidato, comando)
        self._publicador.publicar(evento)

    def revertirUltimo(self, candidato: Candidato, actorId: str) -> None:
        if not self._historial.hayCambios(candidato):
            raise ValueError(f"No hay cambios que revertir para {candidato.id()}")
        comando = self._historial.retirarUltimo(candidato)
        evento = comando.deshacer(actorId)
        self._publicador.publicar(evento)
