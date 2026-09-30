from abc import ABC, abstractmethod

from hirecore.etapas import NaturalezaEtapa, Visibilidad
from hirecore.eventos import EventoCandidato, ObservadorDeCambios


class ReglaDeInteres(ABC):
    @abstractmethod
    def aplica(self, evento: EventoCandidato) -> bool: ...


class ReglaPorNaturaleza(ReglaDeInteres):
    def __init__(self, naturalezas: list[NaturalezaEtapa]) -> None:
        self._naturalezas = naturalezas

    def aplica(self, evento: EventoCandidato) -> bool:
        return evento.etapaAfectada().naturaleza() in self._naturalezas


class ReglaVisibleParaCandidato(ReglaDeInteres):
    def aplica(self, evento: EventoCandidato) -> bool:
        return evento.etapaAfectada().visibilidad() is Visibilidad.PUBLICA


class ReglaSiempre(ReglaDeInteres):
    def aplica(self, evento: EventoCandidato) -> bool:
        return True


class ResolvedorDeDestinatario(ABC):
    @abstractmethod
    def resolver(self, evento: EventoCandidato) -> list[str]: ...


class DestinatarioReclutador(ResolvedorDeDestinatario):
    def resolver(self, evento: EventoCandidato) -> list[str]:
        return [evento.reclutadorId]


class DestinatarioFijo(ResolvedorDeDestinatario):
    def __init__(self, direccion: str) -> None:
        self._direccion = direccion

    def resolver(self, evento: EventoCandidato) -> list[str]:
        return [self._direccion]


class DestinatarioCandidato(ResolvedorDeDestinatario):
    def resolver(self, evento: EventoCandidato) -> list[str]:
        return [evento.candidatoId]


class CanalDeNotificacion(ABC):
    @abstractmethod
    def entregar(self, destinatario: str, mensaje: str) -> None: ...


class CanalCorreo(CanalDeNotificacion):
    def entregar(self, destinatario: str, mensaje: str) -> None:
        print(f"[CORREO] para {destinatario}: {mensaje}")


class CanalPortal(CanalDeNotificacion):
    def entregar(self, destinatario: str, mensaje: str) -> None:
        print(f"[PORTAL] para {destinatario}: {mensaje}")


class Notificador(ObservadorDeCambios):
    def __init__(
        self,
        regla: ReglaDeInteres,
        destinatario: ResolvedorDeDestinatario,
        canal: CanalDeNotificacion,
    ) -> None:
        self._regla = regla
        self._destinatario = destinatario
        self._canal = canal

    def actualizar(self, evento: EventoCandidato) -> None:
        if not self._regla.aplica(evento):
            return
        for destinatario in self._destinatario.resolver(evento):
            self._canal.entregar(destinatario, evento.describir())
