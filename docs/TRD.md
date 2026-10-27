# TRD — Technical Requirements Document — OpenRoadmap

> **Qué es:** Define la arquitectura técnica, decisiones de diseño, contratos de componentes y convenciones de ingeniería. Es la guía para construir el software de forma consistente y mantenible.

## 1. Stack y versiones exactas

| Capa | Elección | Versión exacta | Justificación |
|------|----------|----------------|---------------|
| **Frontend** | React + Vite + pnpm | React 19.x · Vite 6.x · pnpm 11.20.0 · Node v24.18.0 | React 19 con soporte para hooks modernos y React Server Components listos; Vite provee Hot Module Reloading casi instantáneo; pnpm garantiza instalaciones eficientes y reproducibles mediante hard-links. |
| **Backend** | FastAPI + uv | FastAPI 0.115.x · uv 0.12.9 · Python 3.12+ | uv resuelve y gestiona dependencias hasta 10 veces más rápido que pip tradicional; FastAPI ofrece validación automática con Pydantic v2 y documentación OpenAPI interactiva sin overhead. |
| **ORM / Acceso a datos** | SQLAlchemy 2.0 (async) / psycopg3 | SQLAlchemy 2.0.x · psycopg 3.2.x | Patrón Data Mapper tipado con soporte asíncrono nativo para maximizar el throughput sobre PostgreSQL. |
| **Base de datos** | PostgreSQL | **18.6** | Requisito fijo de la cátedra; motor relacional robusto con soporte nativo para restricciones de integridad, transacciones ACID y tipos enumerados. |
| **Infraestructura (dev)** | Docker + Docker Compose | Docker 29.7.2 · Docker Compose v2.30+ | Aislamiento completo de dependencias; garantiza reproducibilidad idéntica entre entornos de desarrollo y evaluación docente. |

## 2. Decisiones técnicas

| # | Decisión | Alternativas consideradas | Opción elegida | Justificación |
|---|----------|---------------------------|----------------|---------------|
| **TD-001** | **Estrategia de autenticación** | A) Sesiones con cookies stateful en Redis.<br>B) Tokens JWT stateless.<br>C) Basic Auth HTTP. | **B) Tokens JWT stateless** con algoritmo HS256 y hashing de contraseñas con **bcrypt** (12 rondas de salteo). | Permite escalar horizontalmente sin requerir almacenamiento de sesiones en memoria; desacopla el backend del frontend; el token se envía en el header `Authorization: Bearer <token>`. |
| **TD-002** | **Estrategia de paginación** | A) Paginación por cursor (keyset).<br>B) Paginación por offset (`page` y `page_size`). | **B) Paginación por offset** estándar con metadatos `{ "items": [...], "total": N, "page": n, "page_size": 20, "total_pages": T }`. | Permite a los usuarios saltar a páginas arbitrarias en tablas y vistas de catálogo; el volumen previsto para el dominio es perfectamente manejable por índices en PostgreSQL sin degradación. Cumple estrictamente la restricción de paginación de la SPEC. |
| **TD-003** | **Formato uniforme de errores de API** | A) Mensajes de error en texto plano.<br>B) Formato RFC 7807 (Problem Details).<br>C) Formato Envelope propio unificado. | **C) Envelope unificado:** `{ "error": { "code": "STRING_CODE", "message": "Mensaje legible", "details": [...] } }`. | Provee un contrato predecible para el frontend en React; facilita mostrar validaciones de campos inline y toasters de error globales con el mismo parser. |
| **TD-004** | **Modelado de "Mi Roadmap"** | A) Array de IDs en una columna JSONB dentro del usuario.<br>B) Tabla intermedia relacional `roadmap_items`. | **B) Tabla intermedia relacional `roadmap_items`** con clave foránea a `usuarios`, clave foránea a `cursos`, columna de posición `orden` (entero) y columna de avance `estado_progreso` (`pendiente`, `en_progreso`, `completado`). | Preserva la integridad referencial relacional, facilita consultas indexadas para evitar duplicados mediante índice único `(usuario_id, curso_id)` y permite reordenamiento secuencial seguro. |
| **TD-005** | **Rate Limiting en Login** | A) Middleware Redis externo.<br>B) Middleware en memoria en FastAPI (`slowapi`). | **B) Middleware `slowapi` con backend in-memory** configurado a 5 peticiones por minuto por IP para el endpoint `/api/v1/auth/login`. | No introduce servicios adicionales de infraestructura en desarrollo (cumpliendo con la consigna de scaffold simple sin dependencias superfluas), mitigando ataques de fuerza bruta de manera inmediata. |

## 3. Arquitectura

### 3.1 Patrón de capas y Screaming Architecture
El sistema implementa una **arquitectura por capas desacoplada** combinada con **Screaming Architecture**: los módulos y carpetas del código reflejan explícitamente los conceptos del negocio (`cursos`, `aportes`, `roadmap`, `auth`), en lugar de agrupar todo por categorías técnicas genéricas del framework.

```mermaid
flowchart LR
    HTTP[HTTP / FastAPI Routers<br>Validación de esquemas Pydantic] --> SVC[Services — Lógica de negocio pura<br>Sin dependencias de HTTP ni SQL]
    SVC --> REPO[Repositories — Acceso a datos<br>SQLAlchemy / Queries específicas]
    REPO --> DB[(PostgreSQL 18.6)]
    SVC --> MODELS[Domain Models / Schemas]
```

- **Routers / Controllers:** Reciben las peticiones HTTP, validan los schemas de entrada con Pydantic y delegan el procesamiento al servicio correspondiente. No contienen lógica de negocio ni sentencias SQL.
- **Services:** Implementan las reglas de negocio puras (ej. transiciones de estado de cursos, validación de reglas de duplicados, cálculo de secuencias de roadmap). Son testeables unitariamente de forma aislada sin requerir base de datos activa.
- **Repositories:** Encapsulan toda interacción con PostgreSQL mediante SQLAlchemy. Los servicios nunca invocan directamente el ORM o SQL crudo.

### 3.2 Estructura de carpetas del repositorio

La estructura sigue estrictamente el principio de Screaming Architecture para la fase de desarrollo (Instancia B):

```
tp-roadmap-cursos/
├── backend/
│   ├── pyproject.toml               # Dependencias manejadas con uv
│   ├── uv.lock
│   ├── Dockerfile                   # Dockerfile de desarrollo
│   ├── app/
│   │   ├── main.py                  # Entrypoint de FastAPI y configuración de middlewares
│   │   ├── config.py                # Pydantic Settings y carga de variables de entorno
│   │   ├── database.py              # Sesión asíncrona de SQLAlchemy y conexión a Postgres
│   │   ├── auth/                    # Dominio: Autenticación y Usuarios
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── models.py
│   │   ├── cursos/                  # Dominio: Catálogo de cursos públicos y categorías
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── models.py
│   │   ├── aportes/                 # Dominio: Carga de aportes y bandeja de validación
│   │   │   ├── router.py
│   │   │   ├── service.py
│   │   │   ├── repository.py
│   │   │   └── models.py
│   │   └── roadmap/                 # Dominio: Roadmap personal de aprendizaje
│   │       ├── router.py
│   │       ├── service.py
│   │       ├── repository.py
│   │       └── models.py
│   └── tests/
│       ├── test_cursos_service.py   # Tests unitarios de lógica pura
│       └── test_roadmap_service.py
├── frontend/
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── vite.config.js               # Proxy de dev: /api/* -> http://backend:8000
│   ├── Dockerfile                   # Dockerfile de desarrollo Vite
│   ├── index.html
│   └── src/
│       ├── main.jsx                 # Entrypoint de React 19
│       ├── App.jsx                  # Shell global y enrutamiento
│       ├── styles/
│       │   ├── variables.css        # Tokens de diseño Google Material (UX-UI §2)
│       │   └── index.css            # Estilos base mobile-first sin media queries
│       ├── components/              # Componentes comunes (Header sándwich, Paginador, Cards)
│       └── features/                # Screaming Architecture en Frontend
│           ├── catalogo/            # Catálogo comunitario paginado
│           ├── aportar/             # Formulario de aporte de cursos
│           ├── roadmap/             # Vista y gestión de roadmap personal
│           ├── validar/             # Bandeja de moderación
│           └── auth/                # Login y registro
├── docker-compose.yml               # Orquestación de dev (postgres, backend, frontend)
├── .env.example                     # Plantilla de variables de entorno
├── .gitignore
├── CHANGELOG.md                     # Registro Keep a Changelog
├── README.md                        # Documentación principal
└── docs/                            # Documentación de la Instancia A
```

### 3.3 Servicios Docker (Entorno de Desarrollo)

| Servicio | Imagen / Build | Puerto | Rol |
|----------|----------------|--------|-----|
| `postgres` | `postgres:18.6` | `5432:5432` | Base de datos relacional persistente (volumen nombrado `pgdata_dev`). |
| `backend` | Build `backend/Dockerfile` (Python 3.12 + uv) | `8000:8000` | Servidor API REST ejecutando FastAPI con recarga en caliente (`uvicorn --reload`). |
| `frontend` | Build `frontend/Dockerfile` (Node 20 + pnpm) | `5173:5173` | Servidor de desarrollo Vite con proxy reverso hacia el backend. |

```mermaid
flowchart LR
    BROWSER["Navegador Web<br>(Cliente HTTP)"] -->|"http://localhost:5173"| FE["Frontend (Vite Dev Server :5173)"]
    FE -- "Proxy /api/*" --> BE["Backend (FastAPI Uvicorn :8000)"]
    BROWSER -. "Acceso directo API :8000" .-> BE
    BE -->|"TCP 5432 / asyncpg"| PG[("PostgreSQL 18.6 :5432")]
```

## 4. Convenciones

### 4.1 Commits: Conventional Commits 1.0
Todo commit debe adherir al estándar de Conventional Commits:
- `feat:` Nueva funcionalidad para el usuario.
- `fix:` Corrección de un error o bug.
- `docs:` Cambios o incorporaciones exclusivas de documentación.
- `test:` Agregado o refactor de pruebas automatizadas.
- `refactor:` Modificación de código sin alteración de comportamiento.
- `docker:` Cambios en Dockerfile, Compose o infraestructura local.
- `chore:` Tareas rutinarias de configuración, dependencias o tooling.

### 4.2 Flujo de Git (Git Flow simplificado)

El flujo garantiza trazabilidad total y prohíbe commits directos en `main`:

```mermaid
gitGraph
   commit id: "Initial commit"
   commit id: "docs: agrega SPEC original"
   branch dev
   checkout dev
   commit id: "chore: init dev branch"
   branch feat/T1-scaffold
   checkout feat/T1-scaffold
   commit id: "feat: scaffold structure"
   checkout dev
   merge feat/T1-scaffold
   branch feat/T2-backend
   checkout feat/T2-backend
   commit id: "feat: add backend"
   checkout dev
   merge feat/T2-backend
   checkout main
   merge dev tag: "v0.1.0"
```

- **`main`:** Contiene exclusivamente código en estado de release listo para producción. Solo recibe merges desde `dev` acompañados por un tag anotado semántico (`vX.Y.Z`).
- **`dev`:** Rama principal de desarrollo e integración continua. Todo cambio ingresa a `dev` mediante ramas de características.
- **`feat/T{N}-descripcion-corta` o `docs/...`:** Ramas de trabajo temporales nacidas de `dev` (o `main` en la fase de documentación inicial) que se mergean de vuelta al completar la tarea correspondiente.

### 4.3 Formato de Errores de API
Toda respuesta de error HTTP (códigos 4xx y 5xx) expone la siguiente estructura JSON uniforme:

```json
{
  "error": {
    "code": "RESOURCE_ALREADY_EXISTS",
    "message": "Ya existe un curso registrado con la URL proporcionada.",
    "details": [
      {
        "field": "url",
        "issue": "Valor duplicado en base de datos"
      }
    ]
  }
}
```

### 4.4 Variables de Entorno

| Variable | Ejemplo | Requerida | Propósito |
|----------|---------|-----------|-----------|
| `ENVIRONMENT` | `development` | Sí | Define el entorno de ejecución (`development`, `testing`, `production`). |
| `DATABASE_URL` | `postgresql+psycopg://postgres:postgres@postgres:5432/roadmap_db` | Sí | Cadena de conexión al motor PostgreSQL. |
| `SECRET_KEY` | `dev-insecure-secret-key-32-chars-min!!` | Sí | Clave para la firma y verificación criptográfica de tokens JWT. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Sí | Tiempo de expiración de la sesión del usuario. |
| `BACKEND_PORT` | `8000` | Sí | Puerto de escucha del servicio backend. |
| `FRONTEND_PORT` | `5173` | Sí | Puerto de escucha del dev server de Vite. |

## 5. Requisitos no funcionales técnicos

| Restricción de la SPEC | Cómo se cumple técnicamente | Verificación |
|-------------------------|-----------------------------|--------------|
| **Paginación obligatoria** | Implementación de `page` y `page_size` en queries SQL con `LIMIT` y `OFFSET`. Los repositorios devuelven una tupla `(items, total_count)` para armar la respuesta paginada completa. | Endpoint `GET /api/v1/cursos?page=1&page_size=20` verificado vía tests y en UI con el componente paginador. |
| **Mobile-First con mejora progresiva** | `index.css` define todos los estilos por defecto sin ninguna media query para resoluciones de 360px. Se agregan `@media (min-width: 768px)` y `@media (min-width: 1024px)` únicamente para enriquecer el layout (ej. pasar de grilla de 1 columna a 2 o 3 columnas). | Auditoría con DevTools en simulación de pantallas de 360px, 768px y 1280px. |
| **Menú sándwich responsivo** | Componente `<Header />` que oculta la barra de navegación tradicional en pantallas < 768px y expone un botón hamburguesa que despliega un drawer lateral con accesibilidad ARIA (`aria-expanded`, `aria-label`). | Navegación accesible probada con teclado y tabulación. |
| **Screaming Architecture** | Estructura modular dividida en subcarpetas de dominio (`cursos/`, `aportes/`, `roadmap/`, `auth/`) tanto en backend como en frontend. | Revisión visual del árbol de directorios del repositorio. |

## 6. Riesgos técnicos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| **Conectividad a base de datos al levantar Docker** | Alta | Alta | Configurar script de inicio o dependencia de salud (`depends_on` con condición de servicio listo) para asegurar que PostgreSQL acepte conexiones antes de levantar FastAPI. |
| **Inconsistencias de orden en el roadmap** | Media | Media | Manejar el campo `orden` con transacciones de base de datos y reindexación automática cuando se elimina un ítem intermedio. |
| **Aportes con URLs caídas o fraudulentas** | Alta | Alta | Obligatoriedad del paso por la bandeja de validación humana antes de publicar cualquier curso en el catálogo general. |
