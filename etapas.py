from abc import ABC, abstractmethod
from enum import Enum


class NaturalezaEtapa(Enum):
    INTERMEDIA = "INTERMEDIA"
    DECISION = "DECISION"
    CIERRE_POSITIVO = "CIERRE_POSITIVO"
    CIERRE_NEGATIVO = "CIERRE_NEGATIVO"


class Visibilidad(Enum):
    INTERNA = "INTERNA"
    PUBLICA = "PUBLICA"


class Etapa(ABC):
    @abstractmethod
    def id(self) -> str: ...

    @abstractmethod
    def etiqueta(self) -> str: ...

    @abstractmethod
    def naturaleza(self) -> NaturalezaEtapa: ...

    @abstractmethod
    def visibilidad(self) -> Visibilidad: ...


class EtapaBase(Etapa):
    def __init__(
        self,
        identificador: str,
        etiquetaVisible: str,
        naturalezaEtapa: NaturalezaEtapa,
        visibilidadEtapa: Visibilidad,
    ) -> None:
        self._identificador = identificador
        self._etiquetaVisible = etiquetaVisible
        self._naturalezaEtapa = naturalezaEtapa
        self._visibilidadEtapa = visibilidadEtapa

    def id(self) -> str:
        return self._identificador

    def etiqueta(self) -> str:
        return self._etiquetaVisible

    def naturaleza(self) -> NaturalezaEtapa:
        return self._naturalezaEtapa

    def visibilidad(self) -> Visibilidad:
        return self._visibilidadEtapa


class Aplicado(EtapaBase):
    def __init__(self) -> None:
        super().__init__("APLICADO", "Aplicado", NaturalezaEtapa.INTERMEDIA, Visibilidad.PUBLICA)


class Entrevista(EtapaBase):
    def __init__(self) -> None:
        super().__init__("ENTREVISTA", "Entrevista", NaturalezaEtapa.INTERMEDIA, Visibilidad.PUBLICA)


class PruebaTecnica(EtapaBase):
    def __init__(self) -> None:
        super().__init__("PRUEBA_TECNICA", "Prueba técnica", NaturalezaEtapa.INTERMEDIA, Visibilidad.PUBLICA)


class VerificacionReferencias(EtapaBase):
    def __init__(self) -> None:
        super().__init__(
            "VERIFICACION_REFERENCIAS",
            "Verificación de referencias",
            NaturalezaEtapa.INTERMEDIA,
            Visibilidad.INTERNA,
        )


class Oferta(EtapaBase):
    def __init__(self) -> None:
        super().__init__("OFERTA", "Oferta", NaturalezaEtapa.DECISION, Visibilidad.PUBLICA)


class Contratado(EtapaBase):
    def __init__(self) -> None:
        super().__init__("CONTRATADO", "Contratado", NaturalezaEtapa.CIERRE_POSITIVO, Visibilidad.PUBLICA)


class Rechazado(EtapaBase):
    def __init__(self) -> None:
        super().__init__("RECHAZADO", "Rechazado", NaturalezaEtapa.CIERRE_NEGATIVO, Visibilidad.PUBLICA)


class FlujoDeSeleccion:
    def __init__(self) -> None:
        self._transiciones: dict[str, set[str]] = {}

    def permitir(self, origen: Etapa, destino: Etapa) -> None:
        self._transiciones.setdefault(origen.id(), set()).add(destino.id())

    def permite(self, origen: Etapa, destino: Etapa) -> bool:
        return destino.id() in self._transiciones.get(origen.id(), set())
