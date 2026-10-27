# UX-UI — Guía Visual de Estilos y Sistema de Diseño — OpenRoadmap

> **Qué es:** Define la identidad visual, tokens de diseño, componentes y directrices de interacción de OpenRoadmap.
> Cumple rigurosamente con las restricciones de la SPEC: **estética inspirada en Google / Material Design**, **mobile-first con mejora progresiva** (estilos base sin media queries) y **menú sándwich accesible**.

## 1. Principios de diseño

1. **Claridad y espacio en blanco:** El contenido y los cursos son los protagonistas. Se prioriza el aire y la respiración visual antes que recuadros pesados o decoraciones innecesarias.
2. **Jerarquía tipográfica Google:** Uso de la familia **Roboto** con tamaños, grosores y contrastes contrastados que guían la lectura sin esfuerzo.
3. **Azul de acción unificado:** Todo elemento clickeable primario o estado interactivo activo utiliza el azul primario de Google (`#1a73e8`), generando una experiencia predecible.
4. **Mobile-First genuino:** Cada vista se concibe y maqueta primero para una pantalla móvil de 360px de ancho sin ninguna media query. Las pantallas más grandes (tablets y desktops) solo agregan columnas y comodidades visuales progresivamente.

## 2. Design Tokens

### 2.1 Paleta de colores

| Token CSS | Valor | Uso previsto | Ratio de contraste WCAG |
|-----------|-------|--------------|-------------------------|
| `--color-primary` | `#1a73e8` | Botones de acción principal, enlaces, bordes de foco, tabs activas | 4.6:1 vs blanco (Cumple AA) |
| `--color-primary-dark` | `#185abc` | Estado hover y active en botones primarios | 6.2:1 vs blanco (Cumple AA) |
| `--color-primary-container` | `#e8f0fe` | Chips activos, fondo de ítems de menú seleccionados | 1.2:1 (superficie decorativa) |
| `--color-on-primary` | `#ffffff` | Texto e iconos sobre superficies primarias | 4.6:1 vs `#1a73e8` (Cumple AA) |
| `--color-surface` | `#ffffff` | Fondo de cards, modales, menú drawer y header | 16:1 vs texto principal |
| `--color-background` | `#f8f9fa` | Fondo global de la aplicación (gris claro Google) | Neutro suave |
| `--color-text` | `#202124` | Texto principal de títulos, párrafos y labels | 15.8:1 vs blanco (Cumple AAA) |
| `--color-text-muted` | `#5f6368` | Metadatos secundarios, placeholders, iconos de apoyo | 7.1:1 vs blanco (Cumple AA) |
| `--color-border` | `#dadce0` | Bordes de inputs, divisores horizontales de tabla | 1.4:1 (límites estructurales) |
| `--color-hover` | `#f1f3f4` | Hover sutil en botones secundarios y filas de tabla | Superficie interactiva |
| `--color-success` | `#188038` | Badges de "publicado", estados "completado", toast exitoso | 4.8:1 vs blanco (Cumple AA) |
| `--color-warning` | `#f9ab00` | Badges de "en revisión", alertas de advertencia | 2.1:1 (requiere texto oscuro `#202124`) |
| `--color-error` | `#d93025` | Mensajes de error de validación, badges de "rechazado", acciones destructivas | 4.7:1 vs blanco (Cumple AA) |

### 2.2 Tipografía

- **Familia principal:** `'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif`
- **Carga:** Google Fonts CDN con directiva `font-display: swap`.

| Token CSS | Tamaño / Line-height | Peso | Uso |
|-----------|----------------------|------|-----|
| `--text-xs` | 12px / 16px | 400 regular | Badges pequeños, pies de página |
| `--text-sm` | 14px / 20px | 400 regular / 500 medium | Metadatos, etiquetas de chips, celdas de tabla |
| `--text-base` | 16px / 24px | 400 regular | Cuerpo de texto, campos de entrada, botones |
| `--text-lg` | 18px / 26px | 500 medium | Títulos de cards de cursos, subtítulos de sección |
| `--text-xl` | 24px / 32px | 500 medium | Títulos de página principales (H1) |

### 2.3 Espaciado, radios y sombras (Material Elevation)

| Token CSS | Valor | Aplicación |
|-----------|-------|------------|
| `--space-1` … `--space-6` | 4px, 8px, 12px, 16px, 24px, 32px | Ritmo modular en base 4px/8px |
| `--radius-sm` | 6px | Tags, badges y chips pequeños |
| `--radius-md` | 8px | Campos de formulario (input, select, textarea) |
| `--radius-lg` | 12px | Cards de cursos, paneles contenedores |
| `--radius-pill` | 9999px | Botones estilo Material 3 |
| `--shadow-1` | `0 1px 2px 0 rgba(60,64,67,0.1), 0 1px 3px 1px rgba(60,64,67,0.15)` | Cards en reposo, header |
| `--shadow-2` | `0 1px 2px 0 rgba(60,64,67,0.1), 0 2px 6px 2px rgba(60,64,67,0.15)` | Hover en cards, menú drawer sándwich |

### 2.4 Bloque de tokens CSS listo para importar

```css
:root {
  /* Colores */
  --color-primary: #1a73e8;
  --color-primary-dark: #185abc;
  --color-primary-container: #e8f0fe;
  --color-on-primary: #ffffff;
  --color-surface: #ffffff;
  --color-background: #f8f9fa;
  --color-text: #202124;
  --color-text-muted: #5f6368;
  --color-border: #dadce0;
  --color-hover: #f1f3f4;
  --color-success: #188038;
  --color-warning: #f9ab00;
  --color-error: #d93025;

  /* Tipografía */
  --font-family: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.5rem;     /* 24px */

  /* Espaciado */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;

  /* Bordes y elevaciones */
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-pill: 9999px;
  --shadow-1: 0 1px 2px 0 rgba(60, 64, 67, 0.1), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
  --shadow-2: 0 1px 2px 0 rgba(60, 64, 67, 0.1), 0 2px 6px 2px rgba(60, 64, 67, 0.15);

  /* Capas de z-index */
  --z-header: 100;
  --z-drawer: 200;
  --z-modal: 300;
  --z-toast: 400;
}
```

## 3. Estrategia Mobile-First con mejora progresiva

- **Regla base:** Los estilos principales se escriben pensando en un viewport de 360px de ancho sin encapsular en ninguna media query.
- **Grillas:**
  - En mobile base: La grilla de cursos del catálogo es estrictamente de **1 columna** (`grid-template-columns: 1fr`).
  - `@media (min-width: 768px)`: Pasa a **2 columnas** con filtros laterales accesibles.
  - `@media (min-width: 1024px)`: Pasa a **3 columnas** con espaciado amplio.

## 4. Componentes clave y estados

### 4.1 Header con menú sándwich responsivo
- **En mobile (< 768px):** Muestra el logotipo de OpenRoadmap, el título y un botón sándwich (icono de 3 barras con `aria-label="Abrir menú de navegación"` y `aria-expanded="false"`). Al activarse, despliega un drawer lateral suave desde la izquierda sobre un overlay traslúcido oscuro.
- **En desktop (>= 768px):** El botón sándwich se oculta (`display: none`), y los enlaces de navegación (`Catálogo`, `Aportar`, `Mi Roadmap`, `Iniciar Sesión`) se presentan horizontales directamente en el header.

### 4.2 Card de curso del catálogo
- **Estructura visual:**
  - Header de card: Chip de categoría (ej. "Frontend", "Backend", "DevOps") y año de edición.
  - Título: H2 limpio de 18px en `--color-text`.
  - Metadatos: Docente o disertante y tema principal.
  - Badges de características (íconos y etiquetas de 12px):
    - Cuestionarios: `[?] Con cuestionarios`
    - Examen: `[!] Examen obligatorio`
    - Certificado: `[✓] Certificado incluido`
    - Aval: Nombre de la organización o universidad.
  - Footer de card: Declaración "Aportado por quien cursó" (o "No cursado por quien aporta") + Botón primario estilo pill "Agregar a mi roadmap".
- **Estados interactivos:**
  - *Reposo:* Sombra `--shadow-1`, fondo blanco.
  - *Hover:* Sombra `--shadow-2`, elevación sutil de 2px (`transform: translateY(-2px)`).
  - *Loading (Skeleton):* Bloque gris suave animado con pulso de opacidad mientras los datos viajan por red.

### 4.3 Componente de paginación
- **Disposición:** Centrado al pie de la grilla de cursos o tabla de aportes.
- **Elementos:**
  - Botón "Anterior" (deshabilitado en página 1).
  - Indicador numérico de página: `Página X de Y (Total: Z cursos)`.
  - Botón "Siguiente" (deshabilitado en la última página).
  - Selector de tamaño de página (20, 50).

### 4.4 Formulario de aporte de cursos
- Campos con etiquetas claras (`<label>`), textos de ayuda y bordes de 8px.
- Indicador visual inmediato de error inline en `--color-error` si la URL no es válida o si falta algún campo mandatorio.
- Botón de envío con estado de carga ("Enviando aporte...") que deshabilita doble clic accidental.

## 5. Accesibilidad (WCAG 2.1 AA)

- **Contraste de colores:** Todos los textos principales y secundarios superan la relación de contraste 4.5:1 exigida por la norma AA.
- **Navegación por teclado:** Todos los botones, enlaces y campos de formulario tienen un anillo de foco visible (`outline: 2px solid var(--color-primary); outline-offset: 2px`).
- **Semántica HTML5:** Uso estricto de elementos `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<button>` y atributos ARIA en componentes interactivos complejos.
