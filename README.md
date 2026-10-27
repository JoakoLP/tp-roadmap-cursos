# OpenRoadmap — Plataforma Comunitaria de Cursos y Aprendizaje

> WebApp de gestión de comunidad de cursos: catálogo comunitario de cursos gratuitos aportados por estudiantes y validados + roadmaps personales de aprendizaje.
>
> **Estado:** 📚 Documentación (Instancia A) — desarrollo pendiente de aprobación docente.

**Stack:** React 19 + Vite + pnpm · FastAPI + uv · PostgreSQL 18.6 · Docker Compose (dev)

---

## Qué hace

OpenRoadmap resuelve la dispersión de recursos educativos gratuitos en la web. Permite a una comunidad de estudiantes aportar cursos de cualquier plataforma (YouTube, Coursera, edX, open-source), validarlos bajo criterios de calidad y centralizarlos en un catálogo público paginado. A partir de este catálogo, cada estudiante puede diseñar, ordenar y seguir su propio **roadmap personal de aprendizaje**, registrando su progreso de forma transparente.

## Documentación

| Documento | Responde la pregunta | Link |
|-----------|----------------------|------|
| **SPEC** | ¿Qué nos pidieron construir y qué decidimos nosotros? | [docs/SPEC.md](docs/SPEC.md) |
| **PRD** | ¿Para quién, qué problema resuelve, qué hace y qué NO hace? | [docs/PRD.md](docs/PRD.md) |
| **TRD** | ¿Cómo lo construimos técnicamente y por qué? | [docs/TRD.md](docs/TRD.md) |
| **UX-UI** | ¿Cómo se ve, se siente y se comporta? | [docs/UX-UI.md](docs/UX-UI.md) |
| **APPFlow** | ¿Qué pantallas hay y cómo se navega? | [docs/APPFlow.md](docs/APPFlow.md) |
| **BackendSchema** | ¿Qué datos persistimos y qué API expone? | [docs/BackendSchema.md](docs/BackendSchema.md) |
| **Implementation Plan** | ¿En qué orden construimos y qué significa "hecho"? | [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) |

## Cómo revisar este repo

- Los archivos `.md` se renderizan automáticamente en GitHub.
- Los diagramas Mermaid (`erDiagram`, `flowchart`, `stateDiagram`) están formateados para renderizado nativo en GitHub.
- **Preview local:** En VS Code con `Ctrl+Shift+V` o extensión Markdown Preview.

## Estado del trabajo

| Instancia | Contenido | Estado |
|-----------|-----------|--------|
| **A — Documentación** | Repo estructurado + 7 documentos normativos | 🚀 En revisión / completada |
| **B — Desarrollo del MVP** | Ejecución de tareas P0 (Scaffold T1-T5 + MVP) | ⏳ Pendiente de aprobación |
| **C — Clase práctica** | Testing unitario/integración, Docker multi-stage | ⏳ Programada |

## Versionado

- **Flujo de Git:** Flujo basado en ramas de características (`feat/*`, `docs/*`) que integran a `dev` y finalmente a `main` para releases taggeados (vX.Y.Z). No se commitea directo en `main`. Detalle completo en [docs/TRD.md](docs/TRD.md).
- **Convención de commits:** Conventional Commits obligatorio al 100% (`feat:`, `fix:`, `docs:`, `test:`, `docker:`, `chore:`).

---

## Licencia / Uso

Trabajo Práctico Individual — Desarrollo de Software (Sección S34), UTN FR La Plata, Ciclo Lectivo 2026.
