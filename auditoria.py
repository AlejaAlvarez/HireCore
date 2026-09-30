from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from hirecore.eventos import EventoCandidato, ObservadorDeCambios, TipoCambio


@dataclass(frozen=True)
class RegistroAuditoria:
    candidatoId: str
    actorId: str
    operacion: TipoCambio
    etapaOrigenId: str
    etapaDestinoId: str
    instante: datetime


class RepositorioAuditoria(ABC):
    @abstractmethod
    def guardar(self, registro: RegistroAuditoria) -> None: ...

    @abstractmethod
    def consultarPorCandidato(self, candidatoId: str) -> list[RegistroAuditoria]: ...


class RepositorioAuditoriaEnMemoria(RepositorioAuditoria):
    def __init__(self) -> None:
        self._registros: list[RegistroAuditoria] = []

    def guardar(self, registro: RegistroAuditoria) -> None:
        self._registros.append(registro)

    def consultarPorCandidato(self, candidatoId: str) -> list[RegistroAuditoria]:
        return [r for r in self._registros if r.candidatoId == candidatoId]


class AuditorDeCambios(ObservadorDeCambios):
    def __init__(self, repositorio: RepositorioAuditoria) -> None:
        self._repositorio = repositorio

    def actualizar(self, evento: EventoCandidato) -> None:
        self._repositorio.guardar(
            RegistroAuditoria(
                candidatoId=evento.candidatoId,
                actorId=evento.actorId,
                operacion=evento.tipo,
                etapaOrigenId=evento.origen.id(),
                etapaDestinoId=evento.destino.id(),
                instante=evento.instante,
            )
        )
