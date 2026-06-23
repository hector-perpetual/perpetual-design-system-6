# Perpetual Design System 6 — Pitch corporativo

Plantilla de presentacion ejecutiva de **Perpetual Technologies** en HTML autocontenido.
Estilo formal tipo BCG/McKinsey, 100% on-brand: tipografia Armin Grotesk embebida en
base64, logos SVG inline y formas de marca (donuts, barras, hexagonos, paneles tintados).
Sin fotos, sin emojis, sin dependencias externas.

## Contenido

El template "Pitch corporativo" incluye 11 slides (1280x720):

1. **Portada ejecutiva** — H1 "Plan de negocio 2026" + composicion de marca (hexagono y circulos).
2. **Roadmap** — 5 fases en barras horizontales con nodo y etiqueta por fase.
3. **Timeline** — linea horizontal con 4 nodos (anos) y tarjetas alternadas.
4. **Divisor de seccion** — "Objetivos de negocio" con numero grande tenue "02".
5. **Mision** — 3 puntos con vineta hexagonal y check.
6. **Vision** — fila de 3 iconos circulares con hexagono de marca y labels.
7. **Objetivo de negocio** — donut grande con % al centro + 3 bullets.
8. **Approach** — fila de 6 iconos circulares etiquetados (pasos del enfoque).
9. **Market Size** — 4 donuts (TAM / SAM / SOM / cuota) con % y label.
10. **Competitor Analysis** — diagrama de Venn semitransparente + bullets de conclusion.
11. **Traction** — grafica de linea ascendente (SVG) + 3 stats grandes.

## Como generar

```bash
python3 build_html.py
# -> perpetual-pitch.html
```

Abre `perpetual-pitch.html` en cualquier navegador. Es un unico archivo autocontenido
(fuentes y logos embebidos), ideal para inspeccionar y conectar a herramientas de diseno.

## Estructura

```
build_html.py            Framework + slides (coordenadas en pulgadas x 96)
assets/fonts/            Armin Grotesk (.otf) embebidas en base64
assets/logo/             Logos Perpetual (SVG/PNG, color y dark)
perpetual-pitch.html     Salida generada
```

## Tokens de marca

`ACCENT #1a56db` · `ACCENT2 #f97316` · `YELLOW #fbb900` · `BGD #0b1220`
`TEXT #111827` · `DIM #374151` · `MUTED #6b7280` · superficies claras y bordes suaves.
Paleta de datos: azul, naranja, verde `#059669`, amarillo, morado `#7e22ce`, gris.

---

Confidencial · Perpetual Technologies © 2026
