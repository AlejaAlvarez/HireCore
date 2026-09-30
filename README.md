# HireCore

Rediseño del sistema de seguimiento de candidatos (ATS) a partir de la conversación con RRHH.
Reto evaluativo del Bloque 1 — Principios y patrones de diseño (Posgrado).

# Integrante: 
Alejandra Alvarez Serna

## Qué resuelve

El código original concentraba en un solo método (`avanzarEstado`) la validación de transiciones, el cambio de estado y el envío de correos, todo con una cadena de `if/else` sobre textos.
Esta versión separa cada responsabilidad para que:

- `GestorDeCandidato` **no conozca** nombres de etapas, destinatarios de notificación ni la lógica de deshacer.
- Se puedan **agregar etapas** (el proceso todavía se está definiendo) sin modificar clases existentes.
- Se pueda **revertir el último cambio** de un candidato y saber **quién hizo qué y cuándo**.

## Estructura

```
hirecore_repo/
├── main.py
├── hirecore/
│   ├── etapas.py          Etapa, EtapaBase, 7 etapas concretas, FlujoDeSeleccion, NaturalezaEtapa, Visibilidad
│   ├── candidato.py       Candidato, RespaldoCandidato
│   ├── comandos.py        Comando, CambiarEtapa, HistorialDeCambios
│   ├── gestor.py          GestorDeCandidato
│   ├── eventos.py         TipoCambio, EventoCandidato, ObservadorDeCambios, PublicadorDeEventos
│   ├── notificacion.py    Notificador, reglas, resolvedores de destinatario y canales
│   ├── auditoria.py       RegistroAuditoria, RepositorioAuditoria, AuditorDeCambios
│   └── composicion.py     Ensamblado del sistema (qué regla, destinatario y canal usa cada público)
└── tests/
    └── test_hirecore.py
```
