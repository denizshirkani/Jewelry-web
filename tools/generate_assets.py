#!/usr/bin/env python3
"""
CHICC Jewellery — original vector artwork + product data generator.

Real photographic stock could not be downloaded inside this sandbox (the
network proxy only allows package registries, not image CDNs), so this
script procedurally renders on-brand, high-resolution SVG "catalogue"
artwork for every product, collection and editorial slot, and emits the
matching products.js data file so imagery and data can never drift apart.

Every image is vector (SVG), so it is always sharp at any zoom, never
blurry, never a broken raster crop, and file-size tiny.
"""
import json
import math
import random
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# ----------------------------------------------------------------------
# Brand palette
# ----------------------------------------------------------------------
IVORY_1 = "#FBF9F4"
IVORY_2 = "#F4EFE4"
IVORY_3 = "#EDE6D6"
CHARCOAL = "#1C1B18"
CHARCOAL_SOFT = "#2B2A26"
GOLD = "#A98A55"
GOLD_LIGHT = "#C9AF80"
WARM_GREY = "#8A8477"

METALS = {
    "White Gold": {"a": "#F2F1EC", "b": "#C9C5B8", "c": "#EAE7DD", "line": "#B9B4A5"},
    "Yellow Gold": {"a": "#E7C88A", "b": "#A9834A", "c": "#D9B876", "line": "#8F6D3C"},
    "Rose Gold": {"a": "#E7BEB0", "b": "#B87D6E", "c": "#DDA898", "line": "#9C6656"},
    "Platinum": {"a": "#F5F4F0", "b": "#CFCCC3", "c": "#E9E7E0", "line": "#B4B0A4"},
}

GEMS = {
    "Diamond": {"a": "#FFFFFF", "b": "#EDEEEA", "c": "#C7C6BC", "spark": "#FFFFFF"},
    "Sapphire": {"a": "#5E86C4", "b": "#1F3E7A", "c": "#0F2350", "spark": "#BFD3F5"},
    "Emerald": {"a": "#5F9E78", "b": "#276245", "c": "#123826", "spark": "#BFE7CE"},
    "Ruby": {"a": "#C4495B", "b": "#7E1626", "c": "#4E0C17", "spark": "#F2B9C1"},
    "Pearl": {"a": "#FBF3E6", "b": "#E7D8BE", "c": "#D3BE9B", "spark": "#FFFFFF"},
    "Onyx": {"a": "#3B3A37", "b": "#131210", "c": "#000000", "spark": "#8B8880"},
    "Morganite": {"a": "#F1C6C0", "b": "#DE9C93", "c": "#C97869", "spark": "#FBE6E2"},
    None: {"a": "#E7C88A", "b": "#A9834A", "c": "#8F6D3C", "spark": "#FBE6C4"},
}

random.seed(7)

def _uid(prefix, n=[0]):
    n[0] += 1
    return f"{prefix}{n[0]}"


def svg_open(w, h, vb=None):
    vb = vb or f"0 0 {w} {h}"
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}" role="img">'


def bg_defs(seed_id, w, h, tone="ivory"):
    """Soft studio-backdrop gradient + vignette used behind every piece."""
    top = IVORY_1 if tone == "ivory" else "#20201C"
    bottom = IVORY_3 if tone == "ivory" else "#0F0F0D"
    return f'''
  <defs>
    <radialGradient id="bg{seed_id}" cx="50%" cy="38%" r="75%">
      <stop offset="0%" stop-color="{top}"/>
      <stop offset="100%" stop-color="{bottom}"/>
    </radialGradient>
    <radialGradient id="shadow{seed_id}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg{seed_id})"/>
'''


def metal_gradient(uid, metal):
    m = METALS.get(metal, METALS["Yellow Gold"])
    return f'''<linearGradient id="{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{m['a']}"/>
      <stop offset="45%" stop-color="{m['c']}"/>
      <stop offset="100%" stop-color="{m['b']}"/>
    </linearGradient>'''


def gem_gradient(uid, gem):
    g = GEMS.get(gem, GEMS[None])
    return f'''<radialGradient id="{uid}" cx="35%" cy="30%" r="75%">
      <stop offset="0%" stop-color="{g['a']}"/>
      <stop offset="55%" stop-color="{g['b']}"/>
      <stop offset="100%" stop-color="{g['c']}"/>
    </radialGradient>'''


def sparkle(cx, cy, s, color="#FFFFFF", op=0.9):
    return (f'<path d="M{cx} {cy-s} L{cx+s*0.22} {cy-s*0.22} L{cx+s} {cy} '
            f'L{cx+s*0.22} {cy+s*0.22} L{cx} {cy+s} L{cx-s*0.22} {cy+s*0.22} '
            f'L{cx-s} {cy} L{cx-s*0.22} {cy-s*0.22} Z" fill="{color}" opacity="{op}"/>')


def gem_stone(cx, cy, r, gem, uid, facets=True):
    g = GEMS.get(gem, GEMS[None])
    out = gem_gradient(uid, gem)
    shape = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{uid})" stroke="{g["c"]}" stroke-width="{max(1,r*0.04)}"/>'
    fac = ""
    if facets:
        for i in range(6):
            ang = math.radians(i * 60 + 15)
            x2 = cx + math.cos(ang) * r * 0.85
            y2 = cy + math.sin(ang) * r * 0.85
            fac += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{g["spark"]}" stroke-opacity="0.35" stroke-width="{max(1,r*0.03)}"/>'
    spark = sparkle(cx - r * 0.32, cy - r * 0.32, max(3, r * 0.28), g["spark"])
    return out, shape + fac + spark


def ring_svg(w, h, metal, gem, seed_tag, angle=-18, scale=1.0):
    uid_bg = _uid("bg")
    uid_m = _uid("m")
    uid_g = _uid("g")
    cx, cy = w * 0.5, h * 0.56
    rx, ry = 220 * scale, 150 * scale
    inner_rx, inner_ry = rx * 0.72, ry * 0.72
    m = METALS.get(metal, METALS["Yellow Gold"])
    gem_uid = _uid("gs")
    gem_defs, gem_shape = gem_stone(cx, cy - ry * 1.02, 46 * scale, gem, gem_uid)
    band = (f'<g transform="rotate({angle} {cx} {cy})">'
            f'<path d="M {cx-rx} {cy} A {rx} {ry} 0 1 0 {cx+rx} {cy} A {rx} {ry} 0 1 0 {cx-rx} {cy} Z '
            f'M {cx-inner_rx} {cy} A {inner_rx} {inner_ry} 0 1 0 {cx+inner_rx} {cy} A {inner_rx} {inner_ry} 0 1 0 {cx-inner_rx} {cy} Z" '
            f'fill="url(#{uid_m})" fill-rule="evenodd" stroke="{m["line"]}" stroke-width="1.5"/></g>')
    prongs = ""
    for dx in (-1, 1):
        px = cx + dx * 30 * scale
        prongs += f'<rect x="{px-6}" y="{cy-ry*1.05}" width="12" height="34" rx="4" fill="url(#{uid_m})" transform="rotate({angle*0.15} {px} {cy})"/>'
    svg = svg_open(w, h)
    svg += bg_defs(uid_bg, w, h)
    svg += f'<defs>{metal_gradient(uid_m, metal)}{gem_defs}</defs>'
    svg += f'<ellipse cx="{cx}" cy="{cy+ry*0.92}" rx="{rx*1.15}" ry="{ry*0.28}" fill="url(#shadow{uid_bg})"/>'
    svg += band + prongs + gem_shape
    svg += f'<text x="{w-28}" y="{h-28}" text-anchor="end" font-family="Georgia, serif" font-size="15" letter-spacing="2" fill="{WARM_GREY}" opacity="0.55">CHICC</text>'
    svg += '</svg>'
    return svg


def bracelet_svg(w, h, metal, gem, seed_tag, tennis=False, scale=1.0):
    uid_bg = _uid("bg")
    uid_m = _uid("m")
    cx, cy = w * 0.5, h * 0.5
    rx, ry = 300 * scale, 190 * scale
    inner_rx, inner_ry = rx * 0.85, ry * 0.8
    m = METALS.get(metal, METALS["Yellow Gold"])
    svg = svg_open(w, h)
    svg += bg_defs(uid_bg, w, h)
    svg += f'<defs>{metal_gradient(uid_m, metal)}</defs>'
    svg += f'<ellipse cx="{cx}" cy="{cy+ry*1.05}" rx="{rx*1.05}" ry="{ry*0.22}" fill="url(#shadow{uid_bg})"/>'
    svg += (f'<path d="M {cx-rx} {cy} A {rx} {ry} 0 1 0 {cx+rx} {cy} A {rx} {ry} 0 1 0 {cx-rx} {cy} Z '
            f'M {cx-inner_rx} {cy} A {inner_rx} {inner_ry} 0 1 0 {cx+inner_rx} {cy} A {inner_rx} {inner_ry} 0 1 0 {cx-inner_rx} {cy} Z" '
            f'fill="url(#{uid_m})" fill-rule="evenodd" stroke="{m["line"]}" stroke-width="1.5"/>')
    if gem:
        n = 9
        for i in range(n):
            t = math.pi * (0.15 + 0.7 * i / (n - 1))
            gx = cx - math.cos(t) * rx * 0.925
            gy = cy - math.sin(t) * ry * 0.925 * -1 + 0  # top arc
            gx = cx + math.cos(math.pi - t) * rx * 0.0  # unused
        # place gems along the top arc
        for i in range(9):
            frac = i / 8
            ang = math.pi * (1.0 - frac)  # 0..pi across top
            gx = cx + math.cos(ang) * rx * 0.93
            gy = cy - math.sin(ang) * ry * 0.93
            gem_uid = _uid("gs")
            gd, gs = gem_stone(gx, gy, 15 * scale, gem, gem_uid, facets=False)
            svg += f'<defs>{gd}</defs>{gs}'
    svg += f'<text x="{w-28}" y="{h-28}" text-anchor="end" font-family="Georgia, serif" font-size="15" letter-spacing="2" fill="{WARM_GREY}" opacity="0.55">CHICC</text>'
    svg += '</svg>'
    return svg


def necklace_svg(w, h, metal, gem, seed_tag, medallion=False, scale=1.0):
    uid_bg = _uid("bg")
    uid_m = _uid("m")
    m = METALS.get(metal, METALS["Yellow Gold"])
    left = (w * 0.30, h * 0.16)
    right = (w * 0.70, h * 0.16)
    bottom = (w * 0.5, h * 0.66)
    svg = svg_open(w, h)
    svg += bg_defs(uid_bg, w, h)
    svg += f'<defs>{metal_gradient(uid_m, metal)}</defs>'
    path = f'M {left[0]} {left[1]} Q {w*0.5} {h*0.72} {right[0]} {right[1]}'
    svg += f'<path d="{path}" fill="none" stroke="url(#{uid_m})" stroke-width="6" opacity="0.95"/>'
    # chain dots
    steps = 46
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * left[0] + 2 * (1 - t) * t * (w * 0.5) + t ** 2 * right[0]
        y = (1 - t) ** 2 * left[1] + 2 * (1 - t) * t * (h * 0.72) + t ** 2 * right[1]
        if i % 2 == 0:
            svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="url(#{uid_m})"/>'
    svg += f'<ellipse cx="{bottom[0]}" cy="{h*0.7}" rx="120" ry="20" fill="url(#shadow{uid_bg})"/>'
    if medallion:
        r = 58 * scale
        med_uid = _uid("m2")
        svg += f'<defs>{metal_gradient(med_uid, metal)}</defs>'
        svg += f'<circle cx="{bottom[0]}" cy="{bottom[1]}" r="{r}" fill="url(#{med_uid})" stroke="{m["line"]}" stroke-width="2"/>'
        svg += f'<circle cx="{bottom[0]}" cy="{bottom[1]}" r="{r*0.62}" fill="none" stroke="{IVORY_1}" stroke-width="2" opacity="0.55"/>'
        svg += f'<text x="{bottom[0]}" y="{bottom[1]+8}" text-anchor="middle" font-family="Georgia, serif" font-size="{r*0.5}" fill="{IVORY_1}" opacity="0.85">C</text>'
    else:
        gem_uid = _uid("gs")
        gd, gs = gem_stone(bottom[0], bottom[1], 34 * scale, gem, gem_uid)
        svg += f'<defs>{gd}</defs>{gs}'
    svg += f'<text x="{w-28}" y="{h-28}" text-anchor="end" font-family="Georgia, serif" font-size="15" letter-spacing="2" fill="{WARM_GREY}" opacity="0.55">CHICC</text>'
    svg += '</svg>'
    return svg


def earrings_svg(w, h, metal, gem, seed_tag, style="stud", scale=1.0):
    uid_bg = _uid("bg")
    uid_m = _uid("m")
    m = METALS.get(metal, METALS["Yellow Gold"])
    svg = svg_open(w, h)
    svg += bg_defs(uid_bg, w, h)
    svg += f'<defs>{metal_gradient(uid_m, metal)}</defs>'
    cy = h * 0.42
    for dx in (-1, 1):
        cx = w * 0.5 + dx * w * 0.16
        svg += f'<ellipse cx="{cx}" cy="{h*0.78}" rx="34" ry="9" fill="url(#shadow{uid_bg})"/>'
        if style == "hoop":
            r = 90 * scale
            svg += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#{uid_m})" stroke-width="10"/>'
        elif style == "drop":
            svg += f'<circle cx="{cx}" cy="{cy-40}" r="9" fill="url(#{uid_m})"/>'
            svg += f'<line x1="{cx}" y1="{cy-33}" x2="{cx}" y2="{cy+18}" stroke="url(#{uid_m})" stroke-width="3"/>'
            gem_uid = _uid("gs")
            gd, gs = gem_stone(cx, cy + 46, 30 * scale, gem, gem_uid)
            svg += f'<defs>{gd}</defs>{gs}'
        else:  # stud / star
            gem_uid = _uid("gs")
            r = 32 * scale
            gd, gs = gem_stone(cx, cy, r, gem, gem_uid)
            svg += f'<defs>{gd}</defs>{gs}'
    svg += f'<text x="{w-28}" y="{h-28}" text-anchor="end" font-family="Georgia, serif" font-size="15" letter-spacing="2" fill="{WARM_GREY}" opacity="0.55">CHICC</text>'
    svg += '</svg>'
    return svg


def collection_svg(w, h, name, accent_gem, tone="ivory"):
    uid_bg = _uid("bg")
    uid_m = _uid("m")
    svg = svg_open(w, h)
    svg += bg_defs(uid_bg, w, h, tone=tone)
    svg += f'<defs>{metal_gradient(uid_m, "Yellow Gold" if accent_gem!="Diamond" else "White Gold")}</defs>'
    cx, cy = w * 0.42, h * 0.5
    rx, ry = w * 0.22, h * 0.12
    inner_rx, inner_ry = rx * 0.72, ry * 0.72
    svg += (f'<g transform="rotate(-16 {cx} {cy})"><path d="M {cx-rx} {cy} A {rx} {ry} 0 1 0 {cx+rx} {cy} A {rx} {ry} 0 1 0 {cx-rx} {cy} Z '
            f'M {cx-inner_rx} {cy} A {inner_rx} {inner_ry} 0 1 0 {cx+inner_rx} {cy} A {inner_rx} {inner_ry} 0 1 0 {cx-inner_rx} {cy} Z" '
            f'fill="url(#{uid_m})" fill-rule="evenodd"/></g>')
    gem_uid = _uid("gs")
    gd, gs = gem_stone(cx, cy - ry * 1.05, w * 0.028, accent_gem, gem_uid)
    svg += f'<defs>{gd}</defs>{gs}'
    ex = w * 0.72
    for i, dx in enumerate((-1, 1)):
        gx = ex + dx * w * 0.045
        gem_uid2 = _uid("gs")
        gd2, gs2 = gem_stone(gx, h * 0.62, w * 0.016, accent_gem, gem_uid2, facets=False)
        svg += f'<defs>{gd2}</defs>{gs2}'
    color = IVORY_1 if tone == "ivory" else CHARCOAL
    txt = CHARCOAL if tone == "ivory" else IVORY_1
    svg += f'<text x="{w*0.08}" y="{h*0.88}" font-family="Georgia, serif" font-size="{w*0.06}" letter-spacing="3" fill="{txt}" opacity="0.82">{name}</text>'
    svg += '</svg>'
    return svg


def editorial_svg(w, h, mode="hero", variant=0):
    """Editorial split composition (no literal figure — see README on
    photography substitution): a clean pale-ivory field on the left third
    for headline/CTA overlay, and a deep charcoal-to-gold panel on the
    right two-thirds holding one large, precisely rendered jewellery
    motif lit against the dark ground for maximum contrast and polish."""
    uid_bg = _uid("bg")
    uid_m = _uid("m")
    split = w * 0.40
    metal_name = ["White Gold", "Yellow Gold", "Rose Gold"][variant % 3]
    svg = svg_open(w, h)
    svg += f'''<defs>
      <linearGradient id="left{uid_bg}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="{IVORY_1}"/>
        <stop offset="100%" stop-color="{IVORY_3}"/>
      </linearGradient>
      <linearGradient id="right{uid_bg}" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#312F29"/>
        <stop offset="55%" stop-color="{CHARCOAL}"/>
        <stop offset="100%" stop-color="#0C0C0B"/>
      </linearGradient>
      <radialGradient id="glow{uid_bg}" cx="60%" cy="38%" r="60%">
        <stop offset="0%" stop-color="{GOLD_LIGHT}" stop-opacity="0.28"/>
        <stop offset="100%" stop-color="{GOLD_LIGHT}" stop-opacity="0"/>
      </radialGradient>
      <linearGradient id="seam{uid_bg}" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="{CHARCOAL}" stop-opacity="0"/>
        <stop offset="100%" stop-color="{CHARCOAL}" stop-opacity="0.35"/>
      </linearGradient>
      {metal_gradient(uid_m, metal_name)}
    </defs>'''
    svg += f'<rect width="{w}" height="{h}" fill="url(#left{uid_bg})"/>'
    svg += f'<rect x="{split}" width="{w-split}" height="{h}" fill="url(#right{uid_bg})"/>'
    svg += f'<rect x="{split}" width="{w-split}" height="{h}" fill="url(#glow{uid_bg})"/>'
    svg += f'<rect x="{split-w*0.06}" width="{w*0.09}" height="{h}" fill="url(#seam{uid_bg})"/>'
    # large, clearly defined ring motif centred in the dark panel
    cx = split + (w - split) * 0.52
    cy = h * 0.52
    rx, ry = (w - split) * 0.30, (w - split) * 0.30
    inner = 0.64
    svg += (f'<g transform="rotate(-14 {cx} {cy})">'
            f'<ellipse cx="{cx}" cy="{cy+ry*1.02}" rx="{rx*1.1}" ry="{ry*0.16}" fill="#000000" opacity="0.35"/>'
            f'<path d="M {cx-rx} {cy} A {rx} {ry} 0 1 0 {cx+rx} {cy} A {rx} {ry} 0 1 0 {cx-rx} {cy} Z '
            f'M {cx-rx*inner} {cy} A {rx*inner} {ry*inner} 0 1 0 {cx+rx*inner} {cy} A {rx*inner} {ry*inner} 0 1 0 {cx-rx*inner} {cy} Z" '
            f'fill="url(#{uid_m})" fill-rule="evenodd" stroke="#00000022" stroke-width="1"/></g>')
    gem_uid = _uid("gs")
    gd, gs = gem_stone(cx, cy - ry * 1.04, rx * 0.16, "Diamond", gem_uid)
    svg += f'<defs>{gd}</defs>{gs}'
    random.seed(200 + variant)
    for i in range(22):
        rx2 = random.uniform(split + (w - split) * 0.05, w * 0.97)
        ry2 = random.uniform(h * 0.06, h * 0.94)
        s = random.uniform(2.5, 7)
        op = random.uniform(0.18, 0.55)
        svg += sparkle(rx2, ry2, s, IVORY_1, op)
    svg += f'<text x="{w*0.06}" y="{h*0.90}" font-family="\'Cormorant Garamond\', Georgia, serif" font-size="{w*0.018}" letter-spacing="4" fill="{WARM_GREY}" opacity="0.7">FINE JEWELLERY &#183; CHICC</text>'
    svg += '</svg>'
    return svg


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


# ----------------------------------------------------------------------
# Product catalogue (single source of truth)
# ----------------------------------------------------------------------
PRODUCTS = [
    # RINGS
    dict(id="r001", name="Éclat Solitaire Ring", category="rings", collection="Éclat",
         material="White Gold", gemstone=["Diamond"], featured=True, new=True, style="solitaire",
         desc="A timeless solitaire designed to capture the light from every angle. Elegant, refined and made to be cherished forever."),
    dict(id="r002", name="Azure Sapphire Ring", category="rings", collection="Azure",
         material="White Gold", gemstone=["Sapphire"], featured=False, new=False, style="solitaire",
         desc="A regal cornflower-blue sapphire set within a fine white gold band, for those drawn to colour with quiet confidence."),
    dict(id="r003", name="Muse Emerald Ring", category="rings", collection="Muse",
         material="Yellow Gold", gemstone=["Emerald"], featured=False, new=False, style="solitaire",
         desc="A deep emerald of exceptional clarity, framed in warm yellow gold. Bold, feminine and entirely iconic."),
    dict(id="r004", name="Lumière Pavé Band", category="rings", collection="Lumière",
         material="White Gold", gemstone=["Diamond"], featured=True, new=False, style="band",
         desc="A slender band paved with brilliant-cut diamonds, designed to be worn alone or layered as an everyday essential."),
    dict(id="r005", name="Rosée Gemstone Ring", category="rings", collection="Rosée",
         material="Rose Gold", gemstone=["Morganite"], featured=False, new=False, style="solitaire",
         desc="A soft blush morganite cradled in rose gold — a gentle, romantic silhouette designed for everyday wear."),
    dict(id="r006", name="Nocturne Onyx Ring", category="rings", collection="Nocturne",
         material="Yellow Gold", gemstone=["Onyx"], featured=False, new=False, style="solitaire",
         desc="Polished black onyx set in warm gold, striking a graphic, after-dark note against the skin."),
    dict(id="r007", name="Muse Ruby Eternity Ring", category="rings", collection="Muse",
         material="Yellow Gold", gemstone=["Ruby"], featured=False, new=False, style="band",
         desc="A continuous line of vivid rubies, symbolising a love without end. Confident, warm and unmistakably CHICC."),
    dict(id="r008", name="Éclat Star Ring", category="rings", collection="Éclat",
         material="White Gold", gemstone=["Diamond"], featured=False, new=False, style="solitaire",
         desc="A sculptural star silhouette set with diamonds, catching the light with every movement of the hand."),
    dict(id="r009", name="Éclat Eternity Band", category="rings", collection="Éclat",
         material="Platinum", gemstone=["Diamond"], featured=True, new=False, style="band",
         desc="An unbroken circle of diamonds in platinum — the quintessential symbol of enduring devotion."),

    # NECKLACES
    dict(id="n001", name="Éclat Solitaire Necklace", category="necklaces", collection="Éclat",
         material="White Gold", gemstone=["Diamond"], featured=True, new=False, style="pendant",
         desc="A single brilliant-cut diamond suspended on a fine white gold chain. Understated, precise, unforgettable."),
    dict(id="n002", name="Azure Sapphire Pendant", category="necklaces", collection="Azure",
         material="White Gold", gemstone=["Sapphire"], featured=True, new=True, style="pendant",
         desc="A luminous sapphire drop that moves gently with the wearer, for colour with quiet drama."),
    dict(id="n003", name="Muse Emerald Necklace", category="necklaces", collection="Muse",
         material="Yellow Gold", gemstone=["Emerald"], featured=False, new=False, style="pendant",
         desc="An emerald of striking depth set in warm gold — a statement piece for the woman who leads."),
    dict(id="n004", name="Rosée Morganite Necklace", category="necklaces", collection="Rosée",
         material="Rose Gold", gemstone=["Morganite"], featured=False, new=False, style="pendant",
         desc="A soft-hued morganite on a delicate rose gold chain, designed to be lived in daily."),
    dict(id="n005", name="Nocturne Onyx Necklace", category="necklaces", collection="Nocturne",
         material="Yellow Gold", gemstone=["Onyx"], featured=False, new=False, style="pendant",
         desc="Sleek onyx in warm gold, a graphic accent for evening dressing and beyond."),
    dict(id="n006", name="Lumière Y Necklace", category="necklaces", collection="Lumière",
         material="White Gold", gemstone=["Diamond"], featured=False, new=False, style="pendant",
         desc="A refined Y-drop silhouette finished with a single diamond, effortless enough for everyday layering."),
    dict(id="n007", name="Muse Ruby Necklace", category="necklaces", collection="Muse",
         material="Yellow Gold", gemstone=["Ruby"], featured=False, new=False, style="pendant",
         desc="A vivid ruby pendant designed to command attention with quiet, confident colour."),
    dict(id="n008", name="Éclat Tennis Necklace", category="necklaces", collection="Éclat",
         material="White Gold", gemstone=["Diamond"], featured=True, new=False, style="pendant",
         desc="A continuous line of matched diamonds worn close to the collarbone — luminous from every angle."),
    dict(id="n009", name="Lumière Gold Medallion", category="necklaces", collection="Lumière",
         material="Yellow Gold", gemstone=[], featured=False, new=False, style="medallion",
         desc="A sculpted gold medallion engraved with the CHICC monogram, worn as a modern heirloom."),

    # EARRINGS
    dict(id="e001", name="Éclat Diamond Studs", category="earrings", collection="Éclat",
         material="White Gold", gemstone=["Diamond"], featured=True, new=False, style="stud",
         desc="Brilliant-cut diamond studs designed for everyday radiance — the CHICC signature essential."),
    dict(id="e002", name="Lumière Diamond Hoops", category="earrings", collection="Lumière",
         material="Yellow Gold", gemstone=["Diamond"], featured=True, new=True, style="hoop",
         desc="Diamond-set hoops in warm gold, light enough for daily wear and polished enough for evening."),
    dict(id="e003", name="Azure Sapphire Drops", category="earrings", collection="Azure",
         material="White Gold", gemstone=["Sapphire"], featured=False, new=False, style="drop",
         desc="Sapphire drops that move gently with every gesture, for colour with understated drama."),
    dict(id="e004", name="Muse Emerald Earrings", category="earrings", collection="Muse",
         material="Yellow Gold", gemstone=["Emerald"], featured=False, new=False, style="drop",
         desc="Emerald drops of exceptional depth, framed in warm gold for a bold, feminine finish."),
    dict(id="e005", name="Rosée Morganite Earrings", category="earrings", collection="Rosée",
         material="Rose Gold", gemstone=["Morganite"], featured=False, new=False, style="stud",
         desc="Soft blush morganite studs in rose gold, a gentle everyday note of colour."),
    dict(id="e006", name="Nocturne Onyx Hoops", category="earrings", collection="Nocturne",
         material="Yellow Gold", gemstone=["Onyx"], featured=False, new=False, style="hoop",
         desc="Polished onyx hoops in warm gold — a graphic, after-dark silhouette."),
    dict(id="e007", name="Éclat Star Earrings", category="earrings", collection="Éclat",
         material="White Gold", gemstone=["Diamond"], featured=False, new=False, style="stud",
         desc="Sculptural diamond stars, catching the light with every turn of the head."),
    dict(id="e008", name="Muse Ruby Earrings", category="earrings", collection="Muse",
         material="Yellow Gold", gemstone=["Ruby"], featured=False, new=False, style="stud",
         desc="Vivid ruby studs in warm gold, designed for the woman who dresses with conviction."),
    dict(id="e009", name="Lumière Pearl Earrings", category="earrings", collection="Lumière",
         material="White Gold", gemstone=["Pearl"], featured=False, new=False, style="drop",
         desc="Lustrous pearl drops in white gold — a modern take on a timeless heirloom silhouette."),

    # BRACELETS
    dict(id="b001", name="Rivière Tennis Bracelet", category="bracelets", collection="Éclat",
         material="White Gold", gemstone=["Diamond"], featured=True, new=True, style="tennis",
         desc="A continuous line of brilliant-cut diamonds in white gold — the ultimate everyday luxury."),
    dict(id="b002", name="Lumière Chain Bracelet", category="bracelets", collection="Lumière",
         material="Yellow Gold", gemstone=[], featured=False, new=False, style="chain",
         desc="A refined gold chain bracelet, designed for effortless layering and daily wear."),
    dict(id="b003", name="Azure Sapphire Bracelet", category="bracelets", collection="Azure",
         material="White Gold", gemstone=["Sapphire"], featured=False, new=False, style="tennis",
         desc="Matched sapphires set in white gold, for colour that catches the light with every gesture."),
    dict(id="b004", name="Rosée Gold Bracelet", category="bracelets", collection="Rosée",
         material="Rose Gold", gemstone=["Morganite"], featured=False, new=False, style="chain",
         desc="A soft rose gold bracelet finished with a single morganite — gentle, modern, wearable daily."),
    dict(id="b005", name="Éclat Diamond Bangle", category="bracelets", collection="Éclat",
         material="Platinum", gemstone=["Diamond"], featured=True, new=False, style="bangle",
         desc="A sculptural diamond bangle in platinum, designed to be worn alone and admired closely."),
    dict(id="b006", name="Nocturne Onyx Bracelet", category="bracelets", collection="Nocturne",
         material="Yellow Gold", gemstone=["Onyx"], featured=False, new=False, style="tennis",
         desc="Polished onyx links in warm gold — a graphic, confident everyday accent."),
    dict(id="b007", name="Muse Celestial Bracelet", category="bracelets", collection="Muse",
         material="Yellow Gold", gemstone=["Diamond"], featured=False, new=True, style="chain",
         desc="Star and moon motifs finished with diamond accents — bold, feminine and entirely iconic."),
    dict(id="b008", name="Muse Ruby Bracelet", category="bracelets", collection="Muse",
         material="Yellow Gold", gemstone=["Ruby"], featured=False, new=False, style="tennis",
         desc="A vivid line of matched rubies in warm gold, designed to command attention."),
    dict(id="b009", name="Lumière Emerald Bracelet", category="bracelets", collection="Lumière",
         material="White Gold", gemstone=["Emerald"], featured=False, new=False, style="tennis",
         desc="Fine emeralds set in white gold, light enough for everyday, striking enough for evening."),
]

for i, p in enumerate(PRODUCTS):
    p["sortOrder"] = i + 1

# ----------------------------------------------------------------------
# Render product imagery
# ----------------------------------------------------------------------
CARD_W, CARD_H = 1000, 1250

for p in PRODUCTS:
    cat = p["category"]
    gem = p["gemstone"][0] if p["gemstone"] else None
    metal = p["material"]
    style = p["style"]
    images = []
    for variant in (1, 2):
        seed_tag = f"{p['id']}-{variant}"
        random.seed(hash(seed_tag) % 9999)
        if cat == "rings":
            angle = -18 if variant == 1 else 8
            svg = ring_svg(CARD_W, CARD_H, metal, gem, seed_tag, angle=angle, scale=1.0 if variant == 1 else 0.92)
        elif cat == "necklaces":
            svg = necklace_svg(CARD_W, CARD_H, metal, gem, seed_tag, medallion=(style == "medallion"), scale=1.0 if variant == 1 else 0.94)
        elif cat == "earrings":
            svg = earrings_svg(CARD_W, CARD_H, metal, gem, seed_tag, style=style, scale=1.0 if variant == 1 else 0.94)
        else:  # bracelets
            svg = bracelet_svg(CARD_W, CARD_H, metal, gem, seed_tag, tennis=(style in ("tennis",)), scale=1.0 if variant == 1 else 0.94)
        fname = f"{p['id']}-{variant}.svg"
        write(os.path.join(ASSETS, "products", cat, fname), svg)
        images.append(f"assets/products/{cat}/{fname}")
    p["images"] = images
    del p["style"]

# ----------------------------------------------------------------------
# Collections artwork
# ----------------------------------------------------------------------
COLLECTIONS = [
    dict(id="eclat", name="ÉCLAT", tagline="Timeless diamonds", gem="Diamond", desc="Éclat celebrates the diamond in its purest form — brilliant, precise and endlessly wearable."),
    dict(id="azure", name="AZURE", tagline="Sapphires & beyond", gem="Sapphire", desc="Azure explores colour through rare sapphires, set to catch the light with every movement."),
    dict(id="lumiere", name="LUMIÈRE", tagline="Everyday essentials", gem="Diamond", desc="Lumière is the art of quiet luxury — fine pieces designed to be worn every single day."),
    dict(id="muse", name="MUSE", tagline="Bold. Feminine. Iconic.", gem="Ruby", desc="Muse is CHICC at its most confident — bold colour and sculptural silhouettes for the modern woman."),
]
for i, c in enumerate(COLLECTIONS):
    svg = collection_svg(900, 1100, c["name"], c["gem"], tone="ivory")
    fname = f"{c['id']}.svg"
    write(os.path.join(ASSETS, "collections", fname), svg)
    c["image"] = f"assets/collections/{fname}"

# ----------------------------------------------------------------------
# Hero + editorial artwork
# ----------------------------------------------------------------------
for i in range(3):
    svg = editorial_svg(1800, 1250, mode="hero", variant=i)
    write(os.path.join(ASSETS, "hero", f"hero-{i+1}.svg"), svg)

for i in range(2):
    svg = editorial_svg(1400, 1700, mode="maison", variant=i + 1)
    write(os.path.join(ASSETS, "editorial", f"maison-{i+1}.svg"), svg)

# ----------------------------------------------------------------------
# Branding: wordmark diamond motif (small, used in nav / favicon)
# ----------------------------------------------------------------------
def brand_mark_svg(w=120, h=120, color=CHARCOAL):
    cx, cy = w / 2, h / 2
    r = w * 0.30
    pts_top = f"{cx},{cy-r} {cx-r*0.62},{cy-r*0.18} {cx+r*0.62},{cy-r*0.18}"
    svg = svg_open(w, h)
    svg += f'<polygon points="{cx-r*0.62},{cy-r*0.18} {cx+r*0.62},{cy-r*0.18} {cx},{cy+r} " fill="none" stroke="{color}" stroke-width="2.5"/>'
    svg += f'<polygon points="{pts_top}" fill="none" stroke="{color}" stroke-width="2.5"/>'
    svg += f'<line x1="{cx-r*0.62}" y1="{cy-r*0.18}" x2="{cx+r*0.62}" y2="{cy-r*0.18}" stroke="{color}" stroke-width="2.5"/>'
    svg += f'<line x1="{cx-r*0.31}" y1="{cy-r*0.18}" x2="{cx}" y2="{cy+r}" stroke="{color}" stroke-width="1.4" opacity="0.7"/>'
    svg += f'<line x1="{cx+r*0.31}" y1="{cy-r*0.18}" x2="{cx}" y2="{cy+r}" stroke="{color}" stroke-width="1.4" opacity="0.7"/>'
    svg += f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy-r*0.18}" stroke="{color}" stroke-width="1.4" opacity="0.7"/>'
    svg += '</svg>'
    return svg

write(os.path.join(ASSETS, "branding", "mark.svg"), brand_mark_svg(color=CHARCOAL))
write(os.path.join(ASSETS, "branding", "mark-ivory.svg"), brand_mark_svg(color=IVORY_1))
write(os.path.join(ASSETS, "branding", "mark-gold.svg"), brand_mark_svg(color=GOLD))

# simple favicon (PIL, drawn — no external assets)
from PIL import Image, ImageDraw
im = Image.new("RGBA", (256, 256), (251, 249, 244, 255))
d = ImageDraw.Draw(im)
cx, cy, r = 128, 118, 78
d.polygon([(cx - r * 0.62, cy - r * 0.18), (cx + r * 0.62, cy - r * 0.18), (cx, cy + r)], outline=(28, 27, 24, 255), width=6)
d.polygon([(cx, cy - r), (cx - r * 0.62, cy - r * 0.18), (cx + r * 0.62, cy - r * 0.18)], outline=(169, 138, 85, 255), width=6)
im.save(os.path.join(ASSETS, "branding", "favicon.png"))
im.resize((32, 32)).save(os.path.join(ASSETS, "branding", "favicon-32.png"))

# ----------------------------------------------------------------------
# Emit products.js
# ----------------------------------------------------------------------
js = "// CHICC JEWELLERY — central product catalogue\n"
js += "// Auto-generated single source of truth consumed by every page.\n"
js += "const CHICC_COLLECTIONS = " + json.dumps(COLLECTIONS, indent=2, ensure_ascii=False) + ";\n\n"
js += "const CHICC_PRODUCTS = " + json.dumps(PRODUCTS, indent=2, ensure_ascii=False) + ";\n"
write(os.path.join(ROOT, "products.js"), js)

print(f"Generated {len(PRODUCTS)} products, {len(COLLECTIONS)} collections.")
print("Rings:", sum(1 for p in PRODUCTS if p["category"] == "rings"))
print("Necklaces:", sum(1 for p in PRODUCTS if p["category"] == "necklaces"))
print("Earrings:", sum(1 for p in PRODUCTS if p["category"] == "earrings"))
print("Bracelets:", sum(1 for p in PRODUCTS if p["category"] == "bracelets"))
