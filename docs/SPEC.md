# SPEC — OpenRoadmap (Comunidad de Cursos & Roadmaps)

> **Qué es este documento:** Versión refinada de la SPEC de clase para la webapp de gestión comunitaria de cursos y roadmaps personales.
> El repositorio comenzó con la SPEC original de clase tal como fue recibida en el commit inicial. Este documento representa su evolución formal: consolida los requisitos, resuelve las ambigüedades y documenta todas las decisiones de producto y de arquitectura.

## 1. Identidad del producto

- **Nombre propio:** OpenRoadmap
- **Una línea:** Para estudiantes y autodidactas de tecnología · centraliza cursos gratuitos evaluados por pares y organiza rutas de aprendizaje secuenciales · para evitar la dispersión de contenidos y asegurar calidad sin costo.

## 2. Problema

Hoy en día, la oferta de cursos gratuitos en internet (YouTube, plataformas abiertas, universidades, repositorios comunitarios) es masiva pero caótica. Los estudiantes enfrentan tres problemas críticos:
1. **Falta de curaduría y enlaces rotos:** Muchos cursos gratuitos están desactualizados, incompletos o ya no están disponibles en sus URLs originales.
2. **Incertidumbre sobre el rigor formativo:** Rara vez se sabe de antemano si un curso incluye cuestionarios, si exige exámenes reales, si emite certificados verificables o si cuenta con el aval de una institución u organización reconocida.
3. **Falta de estructura de estudio (el "abismo del autodidacta"):** Encontrar cursos sueltos no equivale a tener un plan. Los estudiantes necesitan hilvanar cursos en una secuencia lógica ordenada (un *roadmap*) para avanzar desde los fundamentos hasta habilidades avanzadas sin perderse.

OpenRoadmap resuelve esto mediante la colaboración comunitaria: los estudiantes aportan los cursos que descubren o realizan, un proceso de validación filtra el contenido basura o no gratuito, y cada usuario puede seleccionar del catálogo consolidado para construir su propio itinerario de aprendizaje personal.

## 3. Visión

En 12 meses, OpenRoadmap será la plataforma comunitaria de referencia en habla hispana para estudiantes universitarios y autodidactas de tecnología, alojando más de 2.000 cursos rigurosamente categorizados y permitiendo compartir y bifurcar (*fork*) roadmaps de especialización recomendados por la comunidad.

## 4. Alcance

### Dentro (MVP - Instancia B)
- **Catálogo comunitario paginado:** Visualización pública de cursos validados con filtros por categoría y búsqueda textual.
- **Aporte de cursos comunitarios:** Formulario estructurado para cargar cursos gratuitos con todos los metadatos obligatorios (URL activa, rubro, tema, título, versión, año, docentes, cuestionarios, examen, certificado, aval) y declaración explícita de si quien aporta cursó el contenido.
- **Flujo de validación:** Los cursos aportados ingresan en estado `en_revision`. Usuarios con rol validador revisan y aprueban para pasar a `publicado`.
- **Roadmap personal de aprendizaje:** Capacidad para que un usuario autenticado agregue cursos del catálogo comunitario a su roadmap personal, organice su orden de estudio y actualice su estado (pendiente, en progreso, completado).
- **Autenticación y seguridad:** Registro con email/contraseña, login con JWT, contraseñas hasheadas con bcrypt, protección contra fuerza bruta con rate limiting.

### Fuera (out of scope explícito)
- Pasarelas de pago o cursos de pago (el catálogo es 100% gratuito).
- Hosting o reproducción de video dentro de la plataforma (siempre se redirige a la URL externa oficial del curso).
- Emisión propia de certificados (solo se audita si el proveedor externo los otorga).
- Aplicaciones móviles nativas (se provee una WebApp PWA/responsive mobile-first).
- Chat en tiempo real o foros de discusión complejos (se prioriza el catálogo y el roadmap).

## 5. Reglas de producto clave

| # | Regla | Origen |
|---|-------|--------|
| **BR-001** | Un curso aportado entra siempre en estado `en_revision` y solo pasa a `publicado` tras la aprobación de un validador. | SPEC de clase |
| **BR-002** | Cada usuario gestiona su propio roadmap personal de forma privada; nadie puede modificar el roadmap de otro usuario. | Decisión de producto (PRD) |
| **BR-003** | Todo aporte exige declarar obligatoriamente si el aportante completó/tomó el curso (`tomo_el_curso = true/false`). | SPEC de clase |
| **BR-004** | No se permiten URLs duplicadas en cursos publicados o en revisión. Si la URL ya existe, se informa al usuario. | Decisión de producto (PRD) |
| **BR-005** | El catálogo público es de libre lectura sin requerir inicio de sesión previo. | Decisión de producto (PRD) |

## 6. Stack registrado (versiones exactas del entorno de desarrollo)

| Capa | Tecnología | Versión exacta instalada | Notas |
|------|------------|--------------------------|-------|
| Frontend | React 19 + Vite + pnpm | React 19.x · Vite 6.x · pnpm 11.20.0 · Node v24.18.0 | SPA moderna con JSX y CSS nativo |
| Backend | FastAPI + uv | FastAPI 0.115.x / standard · uv 0.12.9 · Python 3.12+ | API REST asíncrona de alto rendimiento |
| Base de datos | PostgreSQL | 18.6 | Estándar relacional fijado por la cátedra |
| Infra (dev) | Docker + Docker Compose | Docker 29.7.2 · Docker Compose v2.30+ | Orquestación local multicontenedor |

## 7. Restricciones técnicas heredadas de la SPEC de clase

| # | Restricción | Cómo la vamos a cumplir |
|---|-------------|-------------------------|
| 1 | **Mobile-first con mejora progresiva:** Estilos base sin media queries; `@media (min-width: …)` únicamente para agregar o mejorar en pantallas más anchas. | Sistema de diseño en Vanilla CSS con variables CSS puras. Reglas base pensadas para 360px móvil; media queries de ampliación en `768px` (tablet) y `1024px` (desktop). |
| 2 | **Paginación obligatoria:** Todas las consultas de listado y sus tablas en pantalla deben ser paginadas. | Paginación basada en offset (`page`, `page_size=20`) con metadatos de respuesta (`items`, `total`, `page`, `page_size`, `total_pages`). |
| 3 | **Menú sándwich en mobile:** Menú desplegable responsivo. | Header con botón hamburguesa accesible (`aria-expanded`, `aria-label`), overlay y menú lateral drawer en pantallas < 768px. |
| 4 | **Screaming Architecture:** La estructura de carpetas debe comunicar el dominio del negocio, no los frameworks. | En backend: carpetas por dominio (`app/cursos/`, `app/aportes/`, `app/roadmap/`, `app/auth/`). En frontend: `src/features/catalogo/`, `src/features/aportar/`, `src/features/roadmap/`, `src/features/auth/`. |
| 5 | **Inspiración Google / Material:** Estética limpia, espacio en blanco, azul primario (`#1a73e8`), jerarquía tipográfica con Roboto, bordes redondeados y sombras sutiles. | Guía detallada en `docs/UX-UI.md` con tokens de color, sombras Material de 2 niveles y tipografía Roboto. |

## 8. Vacíos de la SPEC de clase y decisiones tomadas

| # | Vacío detectado en la SPEC de clase | Opciones consideradas | Decisión tomada | Dónde se desarrolla |
|---|-------------------------------------|-----------------------|-----------------|---------------------|
| 1 | **¿Quién valida los cursos aportados?** | A) Votación comunitaria.<br>B) Validación por docentes/moderadores.<br>C) Aprobación automática. | **Opción B:** Roles diferenciados (`estudiante` y `validador`). Un panel de moderación en `/validar` permite a usuarios con rol `validador` inspeccionar la URL, verificar la gratuidad y publicar o rechazar con motivo. | PRD §7 (BR-001), TRD §2 (TD-005), BackendSchema §3.3 |
| 2 | **¿Qué roles de usuario existen?** | A) Rol único.<br>B) Estudiante y Validador/Admin. | **Opción B:** Roles `estudiante` y `validador`. Los estudiantes aportan y gestionan su roadmap; los validadores moderan el catálogo. | PRD §3, BackendSchema §1.2 |
| 3 | **¿Qué significa exactamente "incluir en mi catálogo / roadmap"?** | A) Bookmark plano.<br>B) Colección ordenada con tracking de progreso. | **Opción B:** Cada ítem en el roadmap almacena `curso_id`, `orden_secuencia` (entero) y `estado_progreso` (`pendiente`, `en_progreso`, `completado`), permitiendo un seguimiento real del aprendizaje. | PRD §4 (US-003), BackendSchema §1.1 |
| 4 | **¿Cómo se maneja la recuperación de contraseña?** | A) Enlace mágico temporal con token firmado.<br>B) Envío de clave provisional. | **Opción A:** Flujo seguro por token criptográfico de un solo uso con expiración de 15 minutos (`/auth/forgot-password` → token → `/auth/reset-password`). En entorno dev se registra en logs de consola. | PRD §5 (RF-003), BackendSchema §3.1 |
| 5 | **Estrategia de Rate Limiting en el login** | A) En memoria por IP.<br>B) Redis distribuido.<br>C) Base de datos. | **Opción A (para dev/MVP):** Middleware en FastAPI (utilizando `slowapi` con storage in-memory) con un umbral de 5 intentos por minuto por IP para evitar ataques de fuerza bruta. | TRD §2 (TD-006), BackendSchema §3.1 |

## 9. Historia de la SPEC

| Fecha | Cambio | Por qué |
|-------|--------|---------|
| 20/10/2026 | SPEC de clase presentada en el aula | Requisitos base de la cátedra |
| 21/10/2026 | Primer commit en Git con la SPEC original íntegra | Regla obligatoria de la consigna |
| 27/10/2026 | Creación de `docs/SPEC.md` refinada | Incorporación de identidad OpenRoadmap, resolución de vacíos, stack verificado y reglas de negocio |
