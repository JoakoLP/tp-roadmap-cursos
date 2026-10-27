# PRD — Product Requirements Document — OpenRoadmap

> **Qué es:** Define el QUÉ y el POR QUÉ del producto. Establece para quién construimos, qué necesidades satisface, qué funcionalidades incluye y qué queda estrictamente fuera de alcance. No contiene decisiones de implementación técnica (para ello consultar el [TRD](TRD.md)).

## 1. Resumen ejecutivo

**OpenRoadmap** es una plataforma web colaborativa donde estudiantes de tecnología descubren cursos gratuitos de calidad y planifican su formación mediante roadmaps personales. La comunidad alimenta el catálogo cargando cursos con metadatos rigurosos (enlace activo, rubro, tema, docentes, cuestionarios, exámenes, certificados, aval institucional) y declarando si los cursaron; moderadores asignados validan cada aporte antes de su publicación. Cada estudiante organiza los cursos validados en una secuencia estructurada de aprendizaje para monitorear su propio progreso.

## 2. Objetivos y métricas de éxito

| Objetivo | Cómo sabemos que lo logramos (Métrica / Señal) |
|----------|------------------------------------------------|
| **Catálogo confiable y libre de spam** | El 100% de los cursos visibles en el catálogo comunitario pasaron por validación humana; 0 enlaces caídos reportados en el seed inicial. |
| **Adopción de roadmaps personales** | Al menos el 70% de los usuarios registrados agregan al menos 2 cursos a su roadmap personal en su primera semana. |
| **Transparencia en el aporte** | El 100% de los cursos aportados registran el flag explícito `tomo_el_curso` para orientar a la comunidad con opiniones reales. |
| **Experiencia de navegación ágil** | Carga del catálogo comunitario paginado en menos de 1 segundo en conexiones estándar 3G/4G móviles. |

## 3. Personas

### Persona 1 — Lucas Gómez (Estudiante Universitario de Sistemas)
- **Contexto:** Alumno de 3er año de Ingeniería/Licenciatura en Sistemas. Busca materias complementarias y especialización práctica que su plan de estudio universitario no cubre en profundidad (por ejemplo Docker, FastAPI o Kubernetes).
- **Motivaciones:** Encontrar cursos actualizados, en español o inglés técnico, que sean 100% gratuitos y tengan ejercicios o cuestionarios para practicar.
- **Frustraciones hoy:** Pierde horas buscando en YouTube o blogs, encontrando tutoriales obsoletos de hace 6 años o cursos promocionados como "gratuitos" que piden tarjeta de crédito en el módulo 2.
- **En su propia voz:** *"Solo quiero una lista ordenada de cursos recomendados por otros compañeros, saber de antemano si dan certificado o si tiene ejercicios prácticos, y poder armar mi plan de estudio para las vacaciones."*

### Persona 2 — Sofía Martínez (Docente / Moderadora Comunitaria)
- **Contexto:** Ayudante de cátedra o profesional graduado que colabora validando recursos formativos y guiando a ingresantes.
- **Motivaciones:** Asegurar que los recursos sugeridos cumplan un estándar mínimo de seriedad académica y verificar que las URLs sigan activas y sean de acceso público y gratuito.
- **Frustraciones hoy:** La saturación de enlaces promocionales, cursos clonados o enlaces rotos sin curaduría.
- **En su propia voz:** *"Si un curso dice que tiene certificado o aval universitario, quiero verificar el link en dos minutos y darle el visto bueno para que toda la comunidad lo aproveche con confianza."*

## 4. User Stories

| ID | Prioridad | Historia | Criterios de aceptación |
|----|-----------|----------|-------------------------|
| **US-001** | **P0** | **Como** visitante o estudiante, **quiero** ver el catálogo comunitario paginado y filtrar por categoría o texto, **para** descubrir cursos de calidad sin barreras de entrada. | - [ ] Dado que visito `/catalogo`, veo los primeros 20 cursos validados en orden cronológico inverso.<br>- [ ] Dado que hay más de 20 cursos, se muestra el componente de paginación indicando página actual y total.<br>- [ ] Dado que busco por texto (ej. "Python"), la grilla actualiza los resultados en tiempo real o al presionar Enter.<br>- [ ] Dado que el catálogo no tiene resultados para un filtro, se muestra un *empty state* claro con invitación a aportar un curso. |
| **US-002** | **P0** | **Como** usuario autenticado, **quiero** aportar un curso gratuito completando sus metadatos obligatorios y declarando si lo cursé, **para** sumarlo al catálogo comunitario. | - [ ] Dado que ingreso a `/aportar`, se me presenta un formulario con: URL activa, categoría, tema, título, versión, año de edición, docentes, cuestionarios (Sí/No), examen (Sí/No), certificado (Sí/No), aval organización (texto opcional).<br>- [ ] Es obligatorio marcar si tomé o no el curso (`tomo_el_curso`).<br>- [ ] Dado que envío el formulario con datos válidos, se genera el registro en estado `en_revision` y recibo confirmación visual.<br>- [ ] Dado que la URL ya existe en el sistema, el formulario rechaza el envío con un mensaje explicativo. |
| **US-003** | **P0** | **Como** usuario autenticado, **quiero** agregar un curso del catálogo comunitario a mi roadmap personal, **para** planificar mi itinerario de estudio. | - [ ] Dado que veo un curso en `/catalogo` o en `/catalogo/:id`, dispongo de un botón "Agregar a mi roadmap".<br>- [ ] Al hacer clic, el curso se añade a mi roadmap en estado `pendiente` con el orden consecutivo disponible.<br>- [ ] Si el curso ya está en mi roadmap, el botón se muestra deshabilitado indicando "Ya en tu roadmap".<br>- [ ] Dado que visito `/roadmap`, veo mis cursos ordenados con su estado (`pendiente`, `en_progreso`, `completado`). |
| **US-004** | **P0** | **Como** usuario, **quiero** registrarme e iniciar sesión de forma segura, **para** guardar mis aportes y mi roadmap personal. | - [ ] Dado que envío email y contraseña válidos en `/registro`, se crea mi cuenta con contraseña cifrada (bcrypt).<br>- [ ] Dado que inicio sesión en `/login` con credenciales correctas, recibo un token JWT de autenticación y acceso a mi perfil.<br>- [ ] Dado que ingreso credenciales incorrectas 5 veces consecutivas en menos de un minuto, el sistema activa rate limiting y bloquea nuevos intentos por 60 segundos. |
| **US-005** | **P0** | **Como** validador/moderador, **quiero** revisar la bandeja de cursos en revisión y aprobarlos o rechazarlos, **para** mantener la calidad y veracidad del catálogo público. | - [ ] Dado que ingreso como validador a `/validar`, veo la lista de cursos en estado `en_revision`.<br>- [ ] Puedo abrir el enlace externo del curso en una pestaña nueva para auditarlo.<br>- [ ] Al hacer clic en "Aprobar", el estado cambia inmediatamente a `publicado` y pasa a ser visible en `/catalogo`.<br>- [ ] Al hacer clic en "Rechazar", se solicita un motivo y el curso queda marcado como `rechazado`. |
| **US-006** | **P1** | **Como** usuario autenticado, **quiero** reordenar y actualizar el estado de avance de los cursos en mi roadmap, **para** reflejar mi progreso académico. | - [ ] En `/roadmap`, puedo cambiar el selector de estado de un ítem a `en_progreso` o `completado`.<br>- [ ] Puedo quitar un curso de mi roadmap mediante un botón de confirmación.<br>- [ ] La interfaz refleja el cambio de estado de inmediato y persiste en la base de datos. |

## 5. Requisitos funcionales

| ID | Requisito funcional | Historia relacionada |
|----|---------------------|----------------------|
| **RF-001** | El sistema debe permitir el registro de usuarios con nombre, email único y contraseña cifrada. | US-004 |
| **RF-002** | El sistema debe emitir tokens JWT al autenticarse exitosamente y validar los permisos en rutas protegidas. | US-004 |
| **RF-003** | El sistema debe proveer recuperación de contraseña mediante token temporal de un solo uso con vigencia de 15 minutos. | US-004 |
| **RF-004** | El catálogo público debe exponer listados paginados de 20 elementos por defecto, con filtros por categoría y búsqueda por palabra clave. | US-001 |
| **RF-005** | El formulario de aporte debe validar que la URL sea sintácticamente válida (HTTP/HTTPS) y que no exista previamente en la base de datos. | US-002 |
| **RF-006** | Todo aporte debe requerir los 10 metadatos estipulados por la cátedra más la declaración obligatoria de toma del curso. | US-002 |
| **RF-007** | El sistema debe mantener los estados del curso: `borrador`, `en_revision`, `publicado` y `rechazado`. | US-002, US-005 |
| **RF-008** | La bandeja de validación debe ser accesible únicamente para usuarios con rol `validador` o `admin`. | US-005 |
| **RF-009** | El usuario debe poder asociar cursos publicados a su roadmap personal, asignando posición secuencial y estado (`pendiente`, `en_progreso`, `completado`). | US-003, US-006 |
| **RF-010** | El usuario puede eliminar ítems de su propio roadmap en cualquier momento. | US-006 |

## 6. Requisitos no funcionales

| ID | Requisito no funcional | Origen / Justificación |
|----|------------------------|------------------------|
| **RNF-001** | **Paginación obligatoria:** Todos los endpoints de listado y componentes de tabla deben paginarse por servidor. | Heredado de la SPEC de clase. Evita sobrecarga de memoria y latencia innecesaria. |
| **RNF-002** | **Mobile-First con mejora progresiva:** Estilos base diseñados para viewport de 360px sin media queries; ampliaciones exclusivas vía `@media (min-width: ...)`. | Heredado de la SPEC de clase. Garantiza compatibilidad universal en dispositivos móviles modestos. |
| **RNF-003** | **Menú sándwich responsivo:** En pantallas inferiores a 768px la navegación colapsa en un menú hamburguesa accesible con teclado y lectores de pantalla. | Heredado de la SPEC de clase. |
| **RNF-004** | **Seguridad en autenticación:** Rate limiting estricto en `/api/v1/auth/login` (máximo 5 requests/minuto por IP); passwords almacenados con hash bcrypt (factor de trabajo de al menos 12 rondas). | Heredado de la SPEC de clase. Mitiga fuerza bruta y filtraciones. |
| **RNF-005** | **Rendimiento:** Tiempo de respuesta en endpoints de consulta del catálogo < 200 ms bajo carga moderada en entorno local. | Decisión de arquitectura. |
| **RNF-006** | **Accesibilidad:** Cumplimiento de pautas WCAG 2.1 nivel AA en contraste cromático (mínimo 4.5:1 para texto normal) y navegación por teclado. | Estándar de calidad Google/Material. |

## 7. Reglas de negocio

| ID | Regla | Fuente |
|----|-------|--------|
| **BR-001** | **Gate de publicación:** Ningún curso aportado será visible en el catálogo comunitario general hasta que su estado sea transicionado a `publicado` por un validador. | SPEC de clase |
| **BR-002** | **Declaración de toma obligatoria:** El campo `tomo_el_curso` (booleano) es mandatorio en cada aporte. No se aceptan aportes sin esta declaración. | SPEC de clase |
| **BR-003** | **Unicidad de recursos:** Una misma URL canónica de curso no puede existir dos veces en el sistema (evita duplicación de aportes idénticos). | Decisión de producto |
| **BR-004** | **Privacidad del roadmap:** El roadmap es personal del usuario; solo el titular de la cuenta puede consultar, añadir, reordenar o eliminar cursos en su roadmap. | Decisión de producto |
| **BR-005** | **Restricción de inclusión en roadmap:** Solo se pueden incorporar al roadmap personal cursos que se encuentren en estado `publicado`. | Decisión de producto |
| **BR-006** | **Gratuidad absoluta:** No se admiten cursos que exijan suscripciones pagas, períodos de prueba con tarjeta de crédito o costos ocultos. | SPEC de clase |

## 8. Fuera de alcance (Out of Scope)

Para el MVP de la Instancia B quedan explícitamente fuera de alcance:
- Pasarelas de cobro o monetización (Stripe, MercadoPago, etc.).
- Reproductor de video nativo o almacenamiento de archivos multimedia pesados.
- Generación y firmado de certificados propios de la plataforma.
- Aplicaciones móviles nativas (iOS/Android).
- Sistema de mensajería privada entre estudiantes.
- Inicio de sesión mediante proveedores sociales de terceros (Google OAuth, GitHub OAuth) para la versión inicial (se usa auth local con JWT).

## 9. Supuestos y decisiones sobre la SPEC de clase

1. **Moderación asistida por roles:** Se asumió que la validación requiere una figura de moderador (`validador`) para evitar que el catálogo se llene de enlaces fraudulentos o spam.
2. **Ciclo de vida del curso:** Se adoptó una máquina de estados finita: `borrador` → `en_revision` → `publicado` / `rechazado`.
3. **Tracking de progreso:** Se asumió que el roadmap personal no es solo un listado de favoritos, sino una herramienta de aprendizaje con estados secuenciales (`pendiente`, `en_progreso`, `completado`).

## 10. Preguntas abiertas

| Pregunta | Impacto | Estado | Resolución adoptada |
|----------|---------|--------|---------------------|
| ¿Qué ocurre si un enlace externo deja de funcionar con el tiempo? | Medio | Decidida | Se contemplará a futuro un botón de reporte "Enlace roto" en la card del curso. |
| ¿Puede un usuario editar su aporte una vez enviado a revisión? | Bajo | Decidida | Solo si se encuentra en estado `borrador` o si fue `rechazado` con observaciones; en `en_revision` queda bloqueado para no adulterar lo que el validador audita. |
