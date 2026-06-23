#!/usr/bin/env python3
"""
Genera la version HTML autocontenida del template "Marketing" (mismas 13 slides
que el .pptx), para inspeccionar en navegador y conectar a herramientas de diseno.
Armin Grotesk embebida en base64, logos SVG inline. Coordenadas = pulgadas x 96px.
"""
import os, base64

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "perpetual-pitch.html")

# --- fuentes OTF -> @font-face base64 ---
FONTS = [("Normal", 300), ("Regular", 400), ("Semi_Bold", 600), ("Black", 800)]
faces = []
for name, weight in FONTS:
    data = open(os.path.join(ASSETS, "fonts", f"ArminGrotesk_{name}.otf"), "rb").read()
    b64 = base64.b64encode(data).decode()
    faces.append("@font-face{font-family:'Armin Grotesk';font-weight:%d;font-display:swap;"
                 "src:url(data:font/otf;base64,%s) format('opentype');}" % (weight, b64))
FONT_FACES = "\n".join(faces)


def _svg(path):
    return open(os.path.join(ASSETS, "logo", path)).read().split("?>", 1)[-1].strip()
LOGO_COLOR, LOGO_DARK = _svg("perpetual-color.svg"), _svg("perpetual-dark.svg")

# --- tokens ---
ACCENT, ACCENT2, YELLOW = "#1a56db", "#f97316", "#fbb900"
BGD, TEXT, DIM, MUTED = "#0b1220", "#111827", "#374151", "#6b7280"
SURFACE, SURFACE2, BORDER, WHITE, DBE4FF = "#f8f9fc", "#eef1f8", "#dde1ef", "#ffffff", "#dbe4ff"
PXIN = 96


def _p(v):
    return f"{v * PXIN:.1f}px"


def box(x, y, w, h, fill=None, r=0, oval=False, shadow=False, line=None):
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
    st += "border-radius:50%;" if oval else (f"border-radius:{r}px;" if r else "")
    if fill: st += f"background:{fill};"
    if line: st += f"border:1px solid {line};"
    if shadow: st += "box-shadow:0 8px 26px rgba(20,40,90,.13);"
    return f'<div style="{st}"></div>'


def txt(x, y, w, h, content, size, color=TEXT, weight=400, align="left",
        valign="top", spacing=None, upper=False, lh=1.1):
    just = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}[valign]
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
          f"display:flex;flex-direction:column;justify-content:{just};overflow:hidden;"
          f"font-size:{size*1.333:.1f}px;color:{color};font-weight:{weight};"
          f"text-align:{align};line-height:{lh};")
    if align == "center": st += "align-items:center;"
    if spacing: st += f"letter-spacing:{spacing}px;"
    if upper: st += "text-transform:uppercase;"
    return f'<div style="{st}">{content}</div>'


def logo(x, y, w, dark=False):
    svg = LOGO_DARK if dark else LOGO_COLOR
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};"
    return f'<div class="lg" style="{st}">{svg}</div>'


def hexagon(x, y, size, fill):
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(size)};height:{_p(size)};"
          f"background:{fill};clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%);")
    return f'<div style="{st}"></div>'


def blob(x, y, d, fill):
    return box(x, y, d, d, fill=fill, oval=True)


def pill(x, y, w, label, fill=ACCENT, fg=WHITE, arrow=True):
    out = [box(x, y, w, 0.62, fill=fill, r=31, shadow=True),
           txt(x + 0.34, y, w - 1.0, 0.62, label, 11.5, fg, 600, "left", "middle",
               spacing=0.8, upper=True)]
    if arrow:
        out.append(box(x + w - 0.74, y + 0.1, 0.42, 0.42, fill=WHITE, oval=True))
        out.append(txt(x + w - 0.74, y + 0.02, 0.42, 0.42, "&rsaquo;", 17, fill, 800, "center", "middle"))
    return "".join(out)


def photo_ph(x, y, w, h, r=12, tint="#E3ECFB"):
    d = min(w, h) * 0.24
    cxp, cyp = x + w / 2, y + h / 2
    return (box(x, y, w, h, fill=tint, r=r)
            + box(cxp - d / 2, cyp - d / 2, d, d, fill=WHITE, oval=True)
            + box(cxp - d * 0.16, cyp - d * 0.16, d * 0.32, d * 0.32, fill=ACCENT, oval=True))


def graphic(x, y, w, h, tint="#DBE7FB", variant="abstract", r=12, shadow=False):
    """Grafico de marca (en vez de foto): composicion abstracta on-brand.
    En Perpetual no usamos fotos de personas salvo en la slide de equipo."""
    out = [box(x, y, w, h, fill=tint, r=r, shadow=shadow)]
    cx, cy = x + w / 2, y + h / 2
    if variant == "growth":
        n, bw, gap = 4, w * 0.13, w * 0.06
        total = n * bw + (n - 1) * gap
        bx, base = cx - total / 2, y + h * 0.8
        cols = [ACCENT, ACCENT2, YELLOW, ACCENT]
        for i in range(n):
            bh = h * (0.16 + 0.13 * i)
            out.append(box(bx + i * (bw + gap), base - bh, bw, bh, fill=cols[i], r=4))
        out.append(box(cx - w * 0.3, y + h * 0.16, h * 0.2, h * 0.2, fill=ACCENT, oval=True))
        out.append(box(cx + w * 0.16, y + h * 0.14, h * 0.16, h * 0.16, fill=YELLOW, oval=True))
    elif variant == "quote":
        out.append(txt(x, y + h * 0.06, w, h * 0.45, "&ldquo;", 92, ACCENT, 800, "center"))
        out.append(txt(x, y + h * 0.62, w, h * 0.2,
                       "&#9733; &#9733; &#9733; &#9733; &#9733;", 17, YELLOW, 700, "center"))
    else:  # abstract: circulos + hexagono de marca
        out.append(box(cx - w * 0.28, cy - h * 0.16, h * 0.34, h * 0.34, fill=ACCENT, oval=True))
        out.append(box(cx + w * 0.03, cy - h * 0.02, h * 0.22, h * 0.22, fill=ACCENT2, oval=True))
        out.append(box(cx - w * 0.02, cy + h * 0.16, h * 0.13, h * 0.13, fill=YELLOW, oval=True))
        out.append(box(cx + w * 0.12, cy - h * 0.26, h * 0.17, h * 0.17, fill=WHITE, oval=True))
    return "".join(out)


def title(runs, x=0.7, y=0.7, w=7.5, size=33, sub=None, sub_w=11.0, sub_color=MUTED, sub_size=12.5):
    """Logo arriba + titulo (2 lineas) + subtitulo opcional DEBAJO del bloque
    completo del titulo, con gap. El titulo ocupa hasta y+0.55+0.92 (~2 lineas);
    el subtitulo se coloca a y_sub para no pisarlo nunca."""
    out = logo(0.6, 0.5, 1.15) + txt(x, y + 0.55, w, 1.05, runs, size, TEXT, 800, lh=1.0)
    if sub is not None:
        y_sub = y + 0.55 + 0.98 + 0.16  # base titulo (2 lineas) + gap
        out += txt(x + 0.02, y_sub, sub_w, 0.45, sub, sub_size, sub_color, 400, lh=1.2)
    return out


def footer(page):
    return (txt(0.7, 7.0, 8, 0.3, "Confidencial &middot; Perpetual Technologies &copy; 2026",
                8.5, MUTED, 400, "left", "middle")
            + txt(11.7, 7.0, 1.1, 0.3, str(page).zfill(2), 8.5, MUTED, 400, "right", "middle"))


def AC(t):  # helper: envuelve en span de acento
    return f'<span style="color:{ACCENT}">{t}</span>'


# ===========================================================================
# Helpers de graficas simples (barras=divs; donut=svg; linea=svg polyline)
# ===========================================================================
DATA = [ACCENT, ACCENT2, "#059669", YELLOW, "#7e22ce", MUTED]


def donut(x, y, d, pct, color=ACCENT, track=SURFACE2, label=None,
          pct_size=None, label_color=MUTED, thick=None):
    """Donut SVG con % al centro. d en pulgadas."""
    px = d * PXIN
    r = px * 0.5 - (thick or px * 0.11) / 2
    cx = cy = px / 2
    circ = 2 * 3.141592653589793 * r
    dash = circ * pct / 100.0
    sw = thick or px * 0.13
    ps = pct_size or d * 26
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{px:.1f}px;height:{px:.1f}px;"
    pad = sw  # padding suficiente para que el linecap redondeado no se recorte
    vb = f"{-pad:.1f} {-pad:.1f} {px + 2 * pad:.1f} {px + 2 * pad:.1f}"
    svg = (f'<svg width="{px:.1f}" height="{px:.1f}" viewBox="{vb}" '
           f'style="position:absolute;left:0;top:0;overflow:visible;transform:rotate(-90deg)">'
           f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{track}" stroke-width="{sw:.1f}"/>'
           f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{color}" '
           f'stroke-width="{sw:.1f}" stroke-linecap="round" '
           f'stroke-dasharray="{dash:.1f} {circ:.1f}"/></svg>')
    out = f'<div style="{st}">{svg}</div>'
    out += txt(x, y, d, d, f"{pct}%", ps, TEXT, 800, "center", "middle")
    if label:
        out += txt(x - 0.3, y + d + 0.08, d + 0.6, 0.45, label, max(9.5, d * 9.5),
                   label_color, 600, "center", "top", lh=1.1)
    return out


def hbar(x, y, w, h, pct, color=ACCENT, track=SURFACE2):
    return (box(x, y, w, h, fill=track, r=int(h * PXIN / 2))
            + box(x, y, w * pct / 100.0, h, fill=color, r=int(h * PXIN / 2)))


def linechart(x, y, w, h, values, color=ACCENT, fill=True, dots=True):
    """Linea ascendente SVG. values normalizados a max."""
    pw, ph = w * PXIN, h * PXIN
    vmax = max(values) * 1.12
    n = len(values)
    pad = pw * 0.02
    pts = []
    for i, v in enumerate(values):
        px = pad + (pw - 2 * pad) * i / (n - 1)
        py = ph - (ph * 0.12) - (ph * 0.78) * (v / vmax)
        pts.append((px, py))
    poly = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    area = f"{pad:.1f},{ph:.1f} " + poly + f" {pw-pad:.1f},{ph:.1f}"
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{pw:.1f}px;height:{ph:.1f}px;"
    grid = "".join(
        f'<line x1="0" y1="{ph*g:.1f}" x2="{pw:.1f}" y2="{ph*g:.1f}" stroke="{BORDER}" stroke-width="1"/>'
        for g in (0.25, 0.5, 0.75, 1.0))
    svg = [f'<svg width="{pw:.1f}" height="{ph:.1f}" viewBox="0 0 {pw:.1f} {ph:.1f}">', grid]
    if fill:
        svg.append(f'<defs><linearGradient id="lg1" x1="0" y1="0" x2="0" y2="1">'
                   f'<stop offset="0" stop-color="{color}" stop-opacity="0.22"/>'
                   f'<stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>')
        svg.append(f'<polygon points="{area}" fill="url(#lg1)"/>')
    svg.append(f'<polyline points="{poly}" fill="none" stroke="{color}" '
               f'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    if dots:
        for p in pts:
            svg.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="4.5" fill="{WHITE}" '
                       f'stroke="{color}" stroke-width="3"/>')
    svg.append("</svg>")
    return f'<div style="{st}">{"".join(svg)}</div>'


# ===========================================================================
# Sistema de iconos de linea por concepto (reemplaza icono comodin generico)
# ===========================================================================
ICONS = {
 "estrategia": '<line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><circle cx="12" cy="12" r="7"/><polygon points="12,8 14.5,13.5 12,12.5 9.5,13.5" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/>',
 "crecimiento": '<polyline points="3,17 8,10 13,13 20,5"/><polyline points="15,5 20,5 20,10"/>',
 "analitica": '<rect x="3" y="12" width="4" height="9" rx="1"/><rect x="10" y="7" width="4" height="14" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/>',
 "inversion": '<circle cx="12" cy="12" r="9"/><path d="M9 14.5c0 1.1 1.3 2 3 2s3-.9 3-2-1.3-2-3-2-3-.9-3-2 1.3-2 3-2 3 .9 3 2"/><line x1="12" y1="7.5" x2="12" y2="9"/><line x1="12" y1="17" x2="12" y2="18.5"/>',
 "idea": '<path d="M9 21h6"/><path d="M10 17h4"/><path d="M12 3a6 6 0 0 1 6 6c0 2.2-1.2 4.1-3 5.2V17H9v-2.8A6 6 0 0 1 6 9a6 6 0 0 1 6-6z"/>',
 "equipo": '<circle cx="9" cy="7" r="3"/><path d="M3 21v-2a5 5 0 0 1 5-5h2"/><circle cx="17" cy="9" r="3"/><path d="M13 21v-2a5 5 0 0 1 5-5h1a5 5 0 0 1 5 5v2"/>',
 "objetivo": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>',
 "mercado": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18"/><path d="M12 3a15 15 0 0 0 0 18"/>',
 "producto": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27,6.96 12,12.01 20.73,6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
 "automatizacion": '<path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 6v6l4 2"/><polyline points="18,2 22,2 22,6"/>',
 "tiempo": '<rect x="3" y="4" width="18" height="17" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="7" y1="14" x2="11" y2="14"/><line x1="7" y1="17" x2="15" y2="17"/>',
 "seguridad": '<path d="M12 3l8 4v5c0 4.4-3.4 8.5-8 9.5C7.4 20.5 4 16.4 4 12V7z"/><polyline points="9,12 11,14 15,10"/>',
 "alcance": '<path d="M5.5 5.5A8.38 8.38 0 0 0 3 12a9 9 0 0 0 9 9 9 9 0 0 0 9-9 8.38 8.38 0 0 0-2.5-6.5"/><path d="M8.5 8.5A4.24 4.24 0 0 0 7 12a5 5 0 0 0 5 5 5 5 0 0 0 5-5 4.24 4.24 0 0 0-1.5-3.5"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>',
 "innovacion": '<circle cx="12" cy="12" r="2"/><ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/>',
}


def line_icon(x, y, size, color, name, circle=True):
    inner = ICONS[name]
    isz = size * 96 * 0.5
    svg = (f'<svg viewBox="0 0 24 24" width="{isz:.0f}" height="{isz:.0f}" fill="none" '
           f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')
    base = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(size)};height:{_p(size)};display:flex;align-items:center;justify-content:center;"
    if circle:
        base += f"border-radius:50%;background:{color}1f;"
    return f'<div style="{base}">{svg}</div>'


def bullet(x, y, w, head, body, color=ACCENT):
    """Bullet con viñeta circular pequeña + titulo + texto."""
    return (box(x, y + 0.04, 0.2, 0.2, fill=color, oval=True)
            + txt(x + 0.36, y - 0.04, w - 0.36, 0.34, head, 13, TEXT, 600)
            + txt(x + 0.36, y + 0.32, w - 0.36, 0.9, body, 11, MUTED, 400, lh=1.3))


def kicker(x, y, label, color=ACCENT):
    return txt(x, y, 6.0, 0.3, label, 10.5, color, 700, upper=True, spacing=1.4)


# ===========================================================================
# Slides — Pitch corporativo
# ===========================================================================
def s01():  # Portada ejecutiva
    return (logo(0.7, 0.65, 1.5)
            + box(8.5, 1.45, 4.0, 4.0, oval=True, fill=SURFACE2)      # disco suave
            + box(8.75, 1.7, 3.5, 3.5, oval=True, fill=ACCENT)        # disco azul
            + box(9.2, 2.15, 2.6, 2.6, oval=True, fill=WHITE)         # recorta -> anillo azul
            + box(9.95, 2.9, 1.1, 1.1, oval=True, fill=ACCENT)        # punto central azul
            + blob(12.1, 1.5, 0.42, ACCENT2)                          # acento naranja
            + blob(8.2, 5.0, 0.32, YELLOW)
            + kicker(0.72, 2.05, "Perpetual Technologies · Confidencial")
            + txt(0.7, 2.45, 7.6, 2.2, f"Plan de negocio<br>{AC('2026.')}", 56, TEXT, 800, lh=0.98)
            + txt(0.72, 4.55, 6.4, 0.4, "Estrategia, crecimiento y ejecucion", 14, DIM, 600)
            + txt(0.72, 5.0, 6.4, 0.9,
                  "Una hoja de ruta clara para escalar ingresos, eficiencia operativa y posicion de mercado.",
                  13, MUTED, 400, lh=1.35)
            + box(0.72, 6.15, 2.4, 0.05, fill=ACCENT, r=3)
            + txt(0.72, 6.4, 8.0, 0.3, "Preparado para el comite ejecutivo · Junio 2026", 11, MUTED, 400))


def s02():  # Roadmap — 5 fases en barras horizontales
    out = [title(f"Roadmap {AC('estrategico.')}",
                 sub="Cinco fases secuenciales para ejecutar el plan a lo largo del ano.")]
    phases = [("Fase 1", "Diagnostico y bases", 100, DATA[0], "Q1"),
              ("Fase 2", "Optimizacion comercial", 82, DATA[1], "Q2"),
              ("Fase 3", "Expansion de mercado", 60, DATA[2], "Q2-Q3"),
              ("Fase 4", "Escalamiento operativo", 40, DATA[4], "Q3-Q4"),
              ("Fase 5", "Consolidacion y rentabilidad", 22, DATA[3], "Q4")]
    y0 = 2.78
    for i, (ph, t, pct, col, q) in enumerate(phases):
        y = y0 + i * 0.78
        out += [box(0.72, y, 0.5, 0.5, fill=col, oval=True),
                txt(0.72, y, 0.5, 0.5, str(i + 1), 14, WHITE, 800, "center", "middle"),
                txt(1.5, y - 0.06, 3.4, 0.3, ph, 9.5, col, 700, upper=True, spacing=0.8),
                txt(1.5, y + 0.18, 3.6, 0.34, t, 13, TEXT, 600),
                hbar(5.4, y + 0.12, 6.0, 0.26, pct, color=col),
                txt(11.55, y, 1.1, 0.5, q, 11, MUTED, 600, "right", "middle")]
    out.append(footer(2))
    return "".join(out)


def s03():  # Timeline — linea horizontal con nodos (anos)
    out = [title(f"Linea de {AC('tiempo.')}", sub="Hitos clave del plan a tres anos.")]
    ly = 4.55
    out.append(box(1.55, ly, 10.25, 0.04, fill=BORDER, r=3))
    nodes = [("2024", "Validacion", "Producto y modelo de negocio validados con clientes ancla.", DATA[0]),
             ("2025", "Traccion", "Crecimiento sostenido de ingresos y base de clientes recurrentes.", DATA[1]),
             ("2026", "Escala", "Expansion regional y eficiencia operativa con margen creciente.", DATA[2]),
             ("2027", "Liderazgo", "Posicion de referencia en el segmento objetivo.", DATA[4])]
    n = len(nodes)
    cw = 2.55
    for i, (yr, t, d, col) in enumerate(nodes):
        cx = 1.85 + (9.65) * i / (n - 1)
        up = i % 2 == 0
        out.append(box(cx - 0.1, ly - 0.08, 0.2, 0.2, fill=col, oval=True))
        out.append(box(cx - 0.04, ly - 0.02, 0.08, 0.08, fill=WHITE, oval=True))
        cardy = ly - 1.55 if up else ly + 0.4
        out += [box(cx - cw / 2, cardy, cw, 1.15, fill=SURFACE, r=12, line=BORDER, shadow=True),
                txt(cx - cw / 2 + 0.2, cardy + 0.16, cw - 0.4, 0.4, yr, 18, col, 800),
                txt(cx - cw / 2 + 0.2, cardy + 0.55, cw - 0.4, 0.3, t, 11.5, TEXT, 600),
                txt(cx - cw / 2 + 0.2, cardy + 0.82, cw - 0.4, 0.3, d, 8.6, MUTED, 400, lh=1.2)]
    out.append(footer(3))
    return "".join(out)


def s04():  # Divisor de seccion
    return (box(0, 0, 13.333, 7.5, fill=SURFACE)
            + logo(0.7, 0.6, 1.4)
            + box(0.72, 3.05, 0.9, 0.06, fill=ACCENT, r=3)
            + kicker(0.72, 2.55, "Seccion 02")
            + txt(0.7, 3.25, 7.5, 1.6, f"Objetivos de<br>{AC('negocio.')}", 48, TEXT, 800, lh=1.0)
            + txt(0.72, 5.4, 6.5, 0.8,
                  "Las metas que guian la asignacion de recursos y la toma de decisiones en 2026.",
                  13, MUTED, 400, lh=1.35)
            + txt(8.2, 0.9, 5.0, 6.0, "02", 280, "#e7ebf6", 800, "right", "middle"))


def s05():  # Mision — 3 puntos con check hexagonal
    out = [title(f"Nuestra {AC('mision.')}"),
           txt(0.72, 2.55, 6.8, 1.4,
               "Impulsar el crecimiento de nuestros clientes con tecnologia, datos y ejecucion disciplinada, "
               "generando valor medible en cada etapa.",
               16, DIM, 400, lh=1.4)]
    points = [("Resultados medibles", "Cada iniciativa se ata a un indicador de negocio y un retorno esperado.", DATA[0]),
              ("Cliente en el centro", "Diseñamos soluciones a partir de necesidades reales del mercado.", DATA[1]),
              ("Mejora continua", "Iteramos con datos para optimizar costo, calidad y velocidad.", DATA[2])]
    for i, (h, b, col) in enumerate(points):
        y = 3.85 + i * 1.05
        out += [box(0.72, y, 0.52, 0.52, fill=col, oval=True),
                txt(0.72, y, 0.52, 0.52, "&check;", 16, WHITE, 800, "center", "middle"),
                txt(1.5, y - 0.02, 5.0, 0.34, h, 14, TEXT, 600),
                txt(1.5, y + 0.34, 5.4, 0.6, b, 11, MUTED, 400, lh=1.3)]
    out += [graphic(8.5, 2.4, 4.1, 3.9, tint="#DBE7FB", variant="abstract", shadow=True),
            footer(5)]
    return "".join(out)


def s06():  # Vision — fila de 3 iconos circulares
    out = [title(f"Nuestra {AC('vision.')}"),
           txt(0.72, 2.55, 11.0, 0.8,
               "Ser el socio de crecimiento de referencia en la region, reconocido por convertir estrategia en resultados.",
               16, DIM, 400, lh=1.4)]
    items = [("Alcance regional", "Presencia en los principales mercados de LatAm.", DATA[0], "alcance"),
             ("Excelencia operativa", "Procesos eficientes y escalables como ventaja.", DATA[2], "automatizacion"),
             ("Innovacion constante", "Adopcion temprana de tecnologia y datos.", DATA[4], "innovacion")]
    for i, (h, b, col, ic) in enumerate(items):
        x = 1.4 + i * 3.95
        out += [line_icon(x, 3.5, 1.35, col, ic),
                txt(x - 0.85, 5.1, 3.05, 0.4, h, 14, TEXT, 600, "center"),
                txt(x - 0.85, 5.5, 3.05, 0.7, b, 11, MUTED, 400, "center", lh=1.3)]
    out.append(footer(6))
    return "".join(out)


def s07():  # Objetivo de negocio — donut grande + 3 bullets
    out = [title(f"Objetivo de {AC('negocio.')}", sub="Meta principal para el ejercicio 2026."),
           donut(0.95, 2.85, 3.6, 38, color=ACCENT, pct_size=46),
           txt(0.55, 6.6, 4.4, 0.3, "Crecimiento de ingresos objetivo", 11.5, MUTED, 600, "center")]
    bl = [("Ingresos recurrentes", "Elevar la participacion de ingresos recurrentes del 52% al 68%.", DATA[0]),
          ("Margen operativo", "Mejorar el margen operativo en 6 puntos porcentuales.", DATA[1]),
          ("Retencion de clientes", "Sostener una retencion neta por encima del 110%.", DATA[2])]
    for i, (h, b, col) in enumerate(bl):
        out.append(bullet(6.2, 2.75 + i * 1.25, 6.2, h, b, color=col))
    out.append(footer(7))
    return "".join(out)


def s08():  # Approach — fila de iconos circulares con pasos
    out = [title(f"Nuestro {AC('enfoque.')}", sub="Seis pasos para llevar la estrategia a resultados.")]
    steps = [("01", "Descubrir", "objetivo"), ("02", "Diagnosticar", "analitica"),
             ("03", "Diseñar", "idea"), ("04", "Ejecutar", "automatizacion"),
             ("05", "Medir", "crecimiento"), ("06", "Optimizar", "seguridad")]
    d = 1.15
    for i, (n, t, ic) in enumerate(steps):
        x = 0.78 + i * 2.05
        col = DATA[i % len(DATA)]
        out += [line_icon(x, 3.1, d, col, ic),
                txt(x - 0.45, 4.45, d + 0.9, 0.35, t, 12.5, TEXT, 600, "center"),
                txt(x - 0.45, 4.85, d + 0.9, 0.3, "Paso " + n, 9.5, col, 700, "center", upper=True, spacing=0.6)]
        if i < len(steps) - 1:
            out.append(box(x + d, 3.1 + d / 2 - 0.02, 0.9, 0.04, fill=BORDER, r=2))
    out.append(footer(8))
    return "".join(out)


def s09():  # Market Size — 4 donuts pequenos en fila
    out = [title(f"Tamano de {AC('mercado.')}",
                 sub="Oportunidad de mercado por segmento (penetracion estimada).")]
    items = [("TAM", 100, DATA[5], "Mercado total direccionable"),
             ("SAM", 46, DATA[0], "Mercado servible disponible"),
             ("SOM", 18, DATA[2], "Mercado servible obtenible"),
             ("Cuota actual", 7, DATA[1], "Participacion lograda hoy")]
    for i, (lab, pct, col, sub) in enumerate(items):
        x = 0.95 + i * 3.05
        out += [donut(x, 2.7, 2.0, pct, color=col, pct_size=30),
                txt(x - 0.4, 4.95, 2.8, 0.34, lab, 13, TEXT, 700, "center"),
                txt(x - 0.4, 5.35, 2.8, 0.6, sub, 10, MUTED, 400, "center", lh=1.25)]
    out.append(footer(9))
    return "".join(out)


def s10():  # Competitor Analysis — venn + bullets
    out = [title(f"Analisis {AC('competitivo.')}")]
    # Venn: 3 circulos semitransparentes
    out += [box(7.3, 2.4, 2.6, 2.6, fill="rgba(26,86,219,0.42)", oval=True),
            box(9.0, 2.4, 2.6, 2.6, fill="rgba(11,18,32,0.42)", oval=True),
            box(8.15, 3.7, 2.6, 2.6, fill="rgba(96,165,250,0.45)", oval=True),
            txt(7.3, 2.95, 1.8, 0.6, "Precio", 11.5, WHITE, 700, "center", "middle"),
            txt(9.7, 2.95, 1.9, 0.6, "Tecnologia", 11.5, WHITE, 700, "center", "middle"),
            txt(8.15, 5.25, 2.6, 0.6, "Servicio", 11.5, WHITE, 700, "center", "middle"),
            txt(8.15, 3.95, 2.6, 0.6, "Perpetual", 12, WHITE, 800, "center", "middle")]
    out.append(txt(0.72, 2.42, 6.0, 0.3, "Donde ganamos", 11, ACCENT, 700, upper=True, spacing=1.2))
    pts = [("Propuesta integrada", "Unimos estrategia, tecnologia y ejecucion donde los rivales solo cubren una parte.", DATA[0]),
           ("Modelo orientado a resultados", "Cobramos por impacto, no por horas, alineando incentivos.", DATA[1]),
           ("Velocidad de implementacion", "Ciclos de entrega mas cortos que el promedio del sector.", DATA[2]),
           ("Conclusion", "Nuestra ventaja esta en la interseccion de servicio, tecnologia y precio competitivo.", DATA[4])]
    for i, (h, b, col) in enumerate(pts):
        out.append(bullet(0.72, 2.72 + i * 1.08, 6.0, h, b, color=col))
    out.append(footer(10))
    return "".join(out)


def s11():  # Traction — linea ascendente + 3 stats
    out = [title(f"Traccion del {AC('negocio.')}", sub="Evolucion de clientes activos por trimestre."),
           linechart(0.85, 2.85, 7.2, 3.15, [120, 165, 198, 236, 300, 369], color=ACCENT)]
    quarters = ["Q1", "Q2", "Q3", "Q4", "Q1", "Q2"]
    for i, q in enumerate(quarters):
        x = 0.85 + (7.2 * 0.02) + (7.2 * 0.96) * i / 5
        out.append(txt(x - 0.4, 6.0, 0.8, 0.3, q, 9.5, MUTED, 600, "center"))
    stats = [("236", "Clientes activos", DATA[0]),
             ("560", "Proyectos entregados", DATA[1]),
             ("369", "Crecimiento neto (%)", DATA[2])]
    for i, (n, lab, col) in enumerate(stats):
        y = 2.5 + i * 1.2
        out += [box(8.6, y, 4.0, 1.05, fill=SURFACE, r=12, line=BORDER),
                box(8.6, y, 0.09, 1.05, fill=col, r=2),
                txt(8.95, y + 0.12, 3.5, 0.6, n, 30, col, 800),
                txt(8.95, y + 0.66, 3.5, 0.3, lab, 11, MUTED, 600, upper=True, spacing=0.5)]
    out.append(footer(11))
    return "".join(out)


SLIDES = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11]
stages = "\n".join(f'<div class="slide">{fn()}</div>' for fn in SLIDES)

HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Perpetual &middot; Pitch corporativo</title>
<style>
{FONT_FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#c9ccd6;font-family:'Armin Grotesk',system-ui,sans-serif;padding:30px 0}}
.deck{{width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:24px}}
.slide{{position:relative;width:1280px;height:720px;background:#fff;overflow:hidden;
  border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.18)}}
.lg svg{{display:block;width:100%;height:auto}}
</style></head><body>
<div class="deck">
{stages}
</div>
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK:", OUT, "|", round(len(HTML) / 1024), "KB |", len(SLIDES), "slides")
