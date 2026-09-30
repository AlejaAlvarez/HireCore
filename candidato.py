from hirecore.etapas import Etapa


class RespaldoCandidato:
    def __init__(self, etapaGuardada: Etapa) -> None:
        self._etapaGuardada = etapaGuardada

    def etapa(self) -> Etapa:
        return self._etapaGuardada


class Candidato:
    def __init__(self, id: str, nombre: str, reclutadorId: str, etapaActual: Etapa) -> None:
        self._id = id
        self._nombre = nombre
        self._reclutadorId = reclutadorId
        self._etapaActual = etapaActual

    def id(self) -> str:
        return self._id

    def nombre(self) -> str:
        return self._nombre

    def reclutadorId(self) -> str:
        return self._reclutadorId

    def etapa(self) -> Etapa:
        return self._etapaActual

    def cambiarEtapa(self, destino: Etapa) -> None:
        self._etapaActual = destino

    def crearRespaldo(self) -> RespaldoCandidato:
        return RespaldoCandidato(self._etapaActual)

    def restaurar(self, respaldo: RespaldoCandidato) -> None:
        self._etapaActual = respaldo.etapa()
