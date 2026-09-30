from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from typing import Optional

from hirecore.candidato import Candidato, RespaldoCandidato
from hirecore.etapas import Etapa
from hirecore.eventos import EventoCandidato, TipoCambio


class Comando(ABC):
    @abstractmethod
    def ejecutar(self) -> EventoCandidato: ...

    @abstractmethod
    def deshacer(self, actorId: str) -> EventoCandidato: ...


class CambiarEtapa(Comando):
    def __init__(self, candidato: Candidato, destino: Etapa, actorId: str) -> None:
        self._candidato = candidato
        self._destino = destino
        self._actorId = actorId
        self._respaldo: Optional[RespaldoCandidato] = None

    def ejecutar(self) -> EventoCandidato:
        self._respaldo = self._candidato.crearRespaldo()
        origen = self._candidato.etapa()
        self._candidato.cambiarEtapa(self._destino)
        return EventoCandidato(
            candidatoId=self._candidato.id(),
            nombreCandidato=self._candidato.nombre(),
            reclutadorId=self._candidato.reclutadorId(),
            tipo=TipoCambio.AVANCE,
            origen=origen,
            destino=self._destino,
            actorId=self._actorId,
            instante=datetime.now(),
        )

    def deshacer(self, actorId: str) -> EventoCandidato:
        if self._respaldo is None:
            raise ValueError("El comando aún no fue ejecutado")
        deshecha = self._candidato.etapa()
        self._candidato.restaurar(self._respaldo)
        return EventoCandidato(
            candidatoId=self._candidato.id(),
            nombreCandidato=self._candidato.nombre(),
            reclutadorId=self._candidato.reclutadorId(),
            tipo=TipoCambio.REVERSION,
            origen=deshecha,
            destino=self._candidato.etapa(),
            actorId=actorId,
            instante=datetime.now(),
        )


class HistorialDeCambios:
    def __init__(self, profundidadMaxima: int = 1) -> None:
        self._profundidadMaxima = profundidadMaxima
        self._porCandidato: dict[str, deque[Comando]] = {}

    def registrar(self, candidato: Candidato, comando: Comando) -> None:
        pila = self._porCandidato.setdefault(candidato.id(), deque())
        pila.append(comando)
        while len(pila) > self._profundidadMaxima:
            pila.popleft()

    def retirarUltimo(self, candidato: Candidato) -> Comando:
        return self._porCandidato[candidato.id()].pop()

    def hayCambios(self, candidato: Candidato) -> bool:
        return bool(self._porCandidato.get(candidato.id()))
