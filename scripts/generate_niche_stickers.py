import os, sys
from PIL import Image, ImageDraw, ImageFont

def get_font(name="arialbd.ttf", size=24):
    windir = os.environ.get("WINDIR", "C:\\Windows")
    font_path = os.path.join(windir, "Fonts", name)
    try:
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def create_badge(width, height, bg_colors, border_color, icon_text, main_text, sub_text=None, category="general"):
    # Render at 2x for antialiasing then resize down
    scale = 2
    W, H = width * scale, height * scale
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background gradient or solid
    c1, c2 = bg_colors
    for y in range(H):
        t = y / float(H)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        a = int(c1[3] + (c2[3] - c1[3]) * t)
        # horizontal line within rounded bounds handled by mask
    
    # We can create a mask for rounded rectangle
    mask = Image.new("L", (W, H), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=16 * scale, fill=255)

    # Fill base
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base_draw = ImageDraw.Draw(base)
    for y in range(H):
        t = y / float(H)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        a = int(c1[3] + (c2[3] - c1[3]) * t)
        base_draw.line([(0, y), (W, y)], fill=(r, g, b, a))

    # Apply mask
    base.putalpha(mask)

    # Border glow
    border_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_img)
    border_draw.rounded_rectangle([2, 2, W - 3, H - 3], radius=16 * scale, outline=border_color, width=3 * scale)

    # Composite base and border
    img = Image.alpha_composite(base, border_img)
    draw = ImageDraw.Draw(img)

    # Fonts
    font_main = get_font("arialbd.ttf", 20 * scale)
    font_sub = get_font("arialbd.ttf", 12 * scale)
    font_icon = get_font("segoeui.ttf", 28 * scale)

    # Draw icon on left if provided
    left_offset = 20 * scale
    if icon_text:
        # draw circular/pill container for icon
        icon_box_w = 48 * scale
        icon_box_h = 48 * scale
        icon_y = (H - icon_box_h) // 2
        draw.rounded_rectangle([left_offset, icon_y, left_offset + icon_box_w, icon_y + icon_box_h],
                               radius=12 * scale, fill=(255, 255, 255, 40), outline=(255, 255, 255, 90), width=scale)
        
        # Center icon text
        try:
            bbox = font_icon.getbbox(icon_text)
            iw, ih = bbox[2] - bbox[0], bbox[3] - bbox[1]
            ix = left_offset + (icon_box_w - iw) // 2 - bbox[0]
            iy = icon_y + (icon_box_h - ih) // 2 - bbox[1]
            draw.text((ix, iy), icon_text, fill=(255, 255, 255, 255), font=font_icon)
        except Exception:
            draw.text((left_offset + 8 * scale, icon_y + 8 * scale), icon_text, fill=(255, 255, 255, 255), font=font_icon)
        
        left_offset += icon_box_w + 14 * scale

    # Text positioning
    if sub_text:
        # Two lines
        main_y = (H // 2) - 18 * scale
        sub_y = (H // 2) + 4 * scale
        draw.text((left_offset, main_y), main_text, fill=(255, 255, 255, 255), font=font_main)
        draw.text((left_offset, sub_y), sub_text, fill=(220, 235, 255, 230), font=font_sub)
    else:
        # Single line centered vertically
        bbox = font_main.getbbox(main_text)
        th = bbox[3] - bbox[1]
        main_y = (H - th) // 2 - bbox[1]
        draw.text((left_offset, main_y), main_text, fill=(255, 255, 255, 255), font=font_main)

    # Downsample back to original size for smooth anti-aliased finish
    final_img = img.resize((width, height), Image.Resampling.LANCZOS)
    return final_img

def main():
    root_paths = [
        "c:/Users/Admin/Desktop/chenyz.app/panel_stream/uploads/stickers",
        "c:/Users/Admin/Desktop/chenyz.app/web y app/uploads/stickers"
    ]
    for p in root_paths:
        os.makedirs(p, exist_ok=True)

    badges_defs = [
        # ✝️ FE & ORACIÓN
        {
            "name": "fe_oracion_en_vivo.png",
            "w": 320, "h": 70,
            "c1": (76, 29, 149, 235), "c2": (124, 58, 237, 235), # Purple/Gold
            "border": (245, 158, 11, 230), # Gold
            "icon": "✝", "main": "ORACIÓN EN VIVO", "sub": "MOMENTO DE FE & ESPERANZA"
        },
        {
            "name": "fe_dios_te_bendiga.png",
            "w": 300, "h": 64,
            "c1": (30, 58, 138, 235), "c2": (2, 132, 199, 235),
            "border": (56, 189, 248, 230),
            "icon": "✨", "main": "DIOS TE BENDIGA", "sub": "ÚNETE Y COMPARTE ESTE AMÉN"
        },
        {
            "name": "fe_cruz_dorada.png",
            "w": 280, "h": 64,
            "c1": (180, 83, 9, 240), "c2": (245, 158, 11, 240),
            "border": (254, 240, 138, 255),
            "icon": "🙏", "main": "CADENA DE ORACIÓN", "sub": "DEJA TU PETICIÓN EN EL CHAT"
        },

        # 🎵 MÚSICA & LOFI / CHILL
        {
            "name": "musica_lofi_chill.png",
            "w": 320, "h": 68,
            "c1": (15, 23, 42, 240), "c2": (88, 28, 135, 240),
            "border": (192, 132, 252, 230),
            "icon": "🎧", "main": "LOFI CHILL BEATS 24/7", "sub": "MÚSICA PARA ESTUDIAR Y RELAJAR"
        },
        {
            "name": "musica_dj_live.png",
            "w": 290, "h": 64,
            "c1": (190, 18, 60, 240), "c2": (234, 88, 12, 240),
            "border": (251, 146, 60, 240),
            "icon": "🔥", "main": "DJ LIVE SESSION", "sub": "SET EXCLUSIVO EN VIVO"
        },
        {
            "name": "musica_ondas_neon.png",
            "w": 280, "h": 60,
            "c1": (3, 105, 161, 240), "c2": (13, 148, 136, 240),
            "border": (45, 212, 191, 240),
            "icon": "🎵", "main": "VIBRAS POSITIVAS", "sub": "STREAM DE MÚSICA CONTINUA"
        },

        # 🎮 GAMING & STREAMING
        {
            "name": "game_en_vivo.png",
            "w": 300, "h": 64,
            "c1": (6, 78, 59, 240), "c2": (5, 150, 105, 240),
            "border": (52, 211, 153, 240),
            "icon": "🎮", "main": "GAMEPLAY EN DIRECTO", "sub": "PRO GAMER TRANSMITIENDO"
        },
        {
            "name": "game_victoria_epica.png",
            "w": 280, "h": 64,
            "c1": (120, 53, 15, 240), "c2": (202, 138, 4, 240),
            "border": (250, 204, 21, 240),
            "icon": "🏆", "main": "VICTORIA ÉPICA", "sub": "RUMBO AL RANKING #1"
        },

        # 🚨 NOTICIAS & URGENTE
        {
            "name": "noticia_ultima_hora.png",
            "w": 310, "h": 68,
            "c1": (153, 27, 27, 250), "c2": (220, 38, 38, 250),
            "border": (254, 202, 202, 250),
            "icon": "🔴", "main": "ÚLTIMA HORA - EN VIVO", "sub": "COBERTURA ESPECIAL EN DIRECTO"
        },
        {
            "name": "noticia_breaking_news.png",
            "w": 290, "h": 64,
            "c1": (24, 24, 27, 250), "c2": (217, 119, 6, 250),
            "border": (252, 211, 77, 250),
            "icon": "⚡", "main": "BREAKING NEWS", "sub": "INFORMACIÓN AL INSTANTE"
        },

        # 💼 FINANZAS & ÉXITO
        {
            "name": "exito_mentalidad.png",
            "w": 310, "h": 64,
            "c1": (15, 23, 42, 245), "c2": (30, 58, 138, 245),
            "border": (234, 179, 8, 240),
            "icon": "💎", "main": "MENTALIDAD DE ÉXITO", "sub": "CRECIMIENTO & MOTIVACIÓN"
        },
        {
            "name": "finanzas_trading.png",
            "w": 300, "h": 64,
            "c1": (20, 83, 45, 245), "c2": (22, 163, 74, 245),
            "border": (134, 239, 172, 240),
            "icon": "📈", "main": "TRADING & FINANZAS", "sub": "ANÁLISIS DE MERCADO EN VIVO"
        },

        # 🛍️ VENTAS & OFERTAS
        {
            "name": "venta_super_oferta.png",
            "w": 290, "h": 64,
            "c1": (185, 28, 28, 245), "c2": (234, 88, 12, 245),
            "border": (253, 186, 116, 240),
            "icon": "🔥", "main": "50% OFF - OFERTA HOY", "sub": "PROMOCIÓN POR TIEMPO LIMITADO"
        },
        {
            "name": "venta_haz_clic.png",
            "w": 270, "h": 60,
            "c1": (2, 132, 199, 245), "c2": (37, 99, 235, 245),
            "border": (147, 197, 253, 240),
            "icon": "👉", "main": "PIDE AQUÍ TU PEDIDO", "sub": "LINK EN DESCRIPCIÓN"
        },

        # 🔔 INTERACCIÓN & LLAMADO A LA ACCIÓN
        {
            "name": "cta_suscribete_canal.png",
            "w": 320, "h": 68,
            "c1": (220, 38, 38, 245), "c2": (185, 28, 28, 245),
            "border": (255, 255, 255, 230),
            "icon": "🔔", "main": "SUSCRÍBETE AL CANAL", "sub": "ACTIVA TODAS LAS NOTIFICACIONES"
        },
        {
            "name": "cta_deja_tu_like.png",
            "w": 290, "h": 64,
            "c1": (30, 64, 175, 245), "c2": (2, 132, 199, 245),
            "border": (125, 211, 252, 240),
            "icon": "👍", "main": "DALE LIKE AL EN VIVO", "sub": "APOYA NUESTRA TRANSMISIÓN"
        },
        {
            "name": "cta_comparte_live.png",
            "w": 290, "h": 64,
            "c1": (107, 33, 168, 245), "c2": (147, 51, 234, 245),
            "border": (216, 180, 254, 240),
            "icon": "📲", "main": "COMPARTE EL DIRECTO", "sub": "CON TUS AMIGOS Y GRUPOS"
        },

        # 🎵 TIKTOK ESPECIAL
        {
            "name": "tiktok_siguenos.png",
            "w": 300, "h": 68,
            "c1": (1, 1, 1, 250), "c2": (15, 23, 42, 250),
            "border": (37, 244, 238, 240), # TikTok Cyan
            "icon": "🎵", "main": "SÍGUENOS EN TIKTOK", "sub": "NUEVO CONTENIDO CADA DÍA"
        },
        {
            "name": "tiktok_live_badge.png",
            "w": 280, "h": 64,
            "c1": (1, 1, 1, 250), "c2": (254, 44, 85, 230), # TikTok Pink
            "border": (254, 44, 85, 255),
            "icon": "🔴", "main": "TIKTOK LIVE", "sub": "EMISIÓN CONTINUA 24/7"
        }
    ]

    for b in badges_defs:
        img = create_badge(
            b["w"], b["h"], (b["c1"], b["c2"]), b["border"],
            b["icon"], b["main"], b["sub"]
        )
        for root in root_paths:
            out_file = os.path.join(root, b["name"])
            img.save(out_file, "PNG")
            print(f"Guardado: {out_file}")

    print(f"\n¡{len(badges_defs)} Stickers de nichos profesionales creados exitosamente!")

if __name__ == "__main__":
    main()
