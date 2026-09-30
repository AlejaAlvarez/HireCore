from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from hirecore.etapas import Etapa


class TipoCambio(Enum):
    AVANCE = "AVANCE"
    REVERSION = "REVERSION"


@dataclass(frozen=True)
class EventoCandidato:
    candidatoId: str
    nombreCandidato: str
    reclutadorId: str
    tipo: TipoCambio
    origen: Etapa
    destino: Etapa
    actorId: str
    instante: datetime

    def etapaAfectada(self) -> Etapa:
        if self.tipo is TipoCambio.REVERSION:
            return self.origen
        return self.destino

    def describir(self) -> str:
        if self.tipo is TipoCambio.REVERSION:
            return (
                f"Se revirtió el cambio de {self.nombreCandidato}: "
                f"volvió a '{self.destino.etiqueta()}' desde '{self.origen.etiqueta()}'"
            )
        return f"{self.nombreCandidato}: {self.origen.etiqueta()} -> {self.destino.etiqueta()}"


class ObservadorDeCambios(ABC):
    @abstractmethod
    def actualizar(self, evento: EventoCandidato) -> None: ...


class PublicadorDeEventos:
    def __init__(self) -> None:
        self._observadores: list[ObservadorDeCambios] = []

    def suscribir(self, observador: ObservadorDeCambios) -> None:
        self._observadores.append(observador)

    def publicar(self, evento: EventoCandidato) -> None:
        for observador in self._observadores:
            observador.actualizar(evento)
