# Sistema de Diseño: Evaluación de Élite

Este documento define la base visual y estructural para la plataforma de evaluación de candidatos. El objetivo no es simplemente construir una interfaz funcional, sino crear una experiencia editorial de alta gama que destile autoridad, precisión y sofisticación técnica.

---

## 1. El Norte Creativo: "El Observatorio de Datos"

Nuestra estrella polar es la precisión analítica envuelta en una estética de lujo. A diferencia de los tableros de gestión genéricos, este sistema de diseño se aleja de las estructuras rígidas de "cajas sobre fondos" para adoptar una jerarquía basada en la profundidad tonal y el espacio negativo. 

Utilizamos el concepto de **Bento Grid Editorial**: los datos no se "encierran", se presentan en superficies que parecen flotar en un vacío oscuro y controlado. La asimetría intencionada en la distribución de las tarjetas y el uso de tipografía de gran escala rompen la monotonía, transformando la evaluación de un candidato en una narrativa visual.

---

## 2. Paleta de Colores y Jerarquía de Superficies

La base del sistema es la oscuridad absoluta (`surface: #0b1326`). La profundidad se construye mediante la estratificación de grises pizarra y azules profundos, no mediante líneas.

### La Regla del "No-Line"
Queda estrictamente prohibido el uso de bordes sólidos de 1px para delimitar secciones. La estructura se define exclusivamente a través de:
1.  **Cambios de Tono:** Una tarjeta en `surface_container_low` situada sobre un fondo `surface`.
2.  **Sombras Ambientales:** El uso de elevación tonal para sugerir proximidad.

### Estratificación de Superficies (Nesting)
Tratamos la UI como capas de cristal esmerilado.
- **Base:** `surface` (#0b1326)
- **Secciones Secundarias:** `surface_container_low` (#131b2e)
- **Tarjetas Interactivas:** `surface_container` (#171f33)
- **Elementos Destacados/Pop-overs:** `surface_container_highest` (#2d3449)

### Acentos de Energía
El color `primary` (#b8c3ff) y su variante vibrante `primary_container` (#2e5bff) deben usarse con parsimonia. Representan el "insight" o el dato clave (ej. una puntuación sobresaliente). Para botones de acción principal, aplicamos el **Efecto de Alma Visual**: un degradado sutil de `primary_container` a `inverse_primary` para evitar la planitud cromática.

---

## 3. Tipografía: Claridad Editorial

Utilizamos **Inter** como nuestro motor tipográfico por su legibilidad técnica y neutralidad moderna.

- **Display (Lg/Md):** Reservado para KPIs numéricos (ej. puntuación total del candidato). Se aplica con un `letter-spacing` negativo (-0.02em) para una apariencia más compacta y premium.
- **Headline (Sm):** Para los nombres de los candidatos y títulos de secciones principales.
- **Title (Md/Sm):** Categorías de evaluación (Soft Skills, Experiencia Técnica).
- **Body (Md):** Toda la lectura de reportes y retroalimentación.
- **Label (Sm):** Etiquetas de estado y metadatos pequeños.

**Jerarquía Visual:** El contraste entre un `display-lg` en `primary` y un `label-sm` en `on_surface_variant` crea una tensión visual que guía el ojo del reclutador hacia lo que realmente importa: el talento.

---

## 4. Elevación, Profundidad y "Ghost Borders"

En este sistema, el diseño es líquido y profundo.

- **Principio de Capas:** Para crear "lift" sin sombras pesadas, coloca un contenedor `surface_container_lowest` sobre una sección `surface_container_low`. La diferencia de luminancia es suficiente para el ojo humano.
- **Sombras Ambientales:** Si un elemento debe "flotar" (como un modal de perfil), usa sombras con un blur de `40px` y una opacidad del 6% usando el color `on_secondary_fixed_variant`.
- **El Fallback del "Ghost Border":** Si la accesibilidad requiere un borde, usa `outline_variant` con una opacidad reducida al 15%. Nunca uses el token al 100%.
- **Glassmorphism:** Para elementos de navegación lateral o filtros persistentes, aplica un `backdrop-blur` de `12px` sobre un color de superficie semi-transparente. Esto integra el contenido que se desplaza por debajo, eliminando cortes visuales bruscos.

---

## 5. Componentes Clave

### Tarjetas Bento (Bento Cards)
Las tarjetas son el alma del sistema. 
- **Radio de Esquina:** `xl` (3rem) para contenedores grandes; `lg` (2rem) para tarjetas internas.
- **Separación:** Prohibido el uso de divisores (`hr`). La separación se logra con el `spacing-8` (2rem) de aire o cambios tonales.

### Visualización de Datos (Data Viz)
- **Gráficos de Puntuación:** No uses bordes. Usa formas rellenas con degradados de `primary` a `tertiary`. 
- **Listas de Candidatos:** Cada fila debe tener un estado de `hover` que eleve el tono de la superficie a `surface_bright` y suavice las esquinas.

### Botones y Chips
- **Botón Primario:** Bordes redondeados `full`. Sin borde, solo relleno con el degradado de acento. Texto en `on_primary_fixed`.
- **Chips de Habilidades:** Fondo `secondary_container` con texto en `on_secondary_container`. Radio `md`.

### Campos de Entrada (Inputs)
- **Estado Reposo:** Fondo `surface_container_low`, sin borde visible.
- **Estado Focus:** Un "Ghost Border" en `primary` al 40% y un sutil resplandor (glow) exterior.

---

## 6. Do’s and Don’ts (Prácticas Recomendadas)

**SÍ (Do):**
- **Usa el espacio:** Deja que los datos respiren. El espacio en blanco (u oscuro, en este caso) es una herramienta de lujo.
- **Micro-interacciones:** Las transiciones entre estados de tarjetas deben ser suaves (300ms, cubic-bezier).
- **Consistencia de Radio:** Mantén los radios grandes (`xl`) para los contenedores principales para mantener la suavidad visual.

**NO (Don't):**
- **No uses blanco puro:** Para el texto, usa siempre `on_surface` o `on_surface_variant` para evitar la fatiga visual en entornos oscuros.
- **No uses sombras negras:** Las sombras deben estar tintadas con azul profundo para mantener la cohesión cromática.
- **No amontones información:** Si un módulo bento tiene demasiada información, divídelo en dos con diferentes pesos visuales (uno de 2/3 de ancho y otro de 1/3).

---

## 7. Escala de Espaciado y Redondez

| Token | Valor (Rem/Px) | Uso Típico |
| :--- | :--- | :--- |
| **Radius XL** | 3rem | Contenedores de tarjetas principales |
| **Radius LG** | 2rem | Tarjetas internas y secciones |
| **Spacing 8** | 2rem | Margen entre tarjetas Bento |
| **Spacing 4** | 1rem | Padding interno de tarjetas |
| **Spacing 12** | 3rem | Margen superior de secciones/headliners |

Este sistema no es estático; es un organismo vivo diseñado para mutar según la complejidad de los datos, manteniendo siempre una elegancia impecable y una legibilidad absoluta en el idioma de la precisión.