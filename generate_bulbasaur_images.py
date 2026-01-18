<<<<<<< HEAD
from PIL import Image, ImageDraw, ImageFont
import os
import random
import textwrap

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1080, 1920
BOTTOM_MARGIN = 6
PANEL_HEIGHT = 520
PANEL_Y_OFFSET = -32

POKEMON_Y_OFFSET = 30

FONT_PATH = "fonts/Montserrat-Regular.ttf"
NAME_FONT_PATH = "fonts/Roboto-VariableFont_wdth,wght.ttf"

OUTPUT_DIR = "output"
POKEMON_DIR = "images/pokemon"
BACKGROUND_DIR = r"D:\Proyectos\Youtube\PokemonGO\backgrounds"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- TYPE → BACKGROUND ----------------
TYPE_BACKGROUND_MAP = {
    "bug": "bug.png",
    "dark": "dark.png",
    "dragon": "dragon.png",
    "electric": "electric.png",
    "fairy": "fairy.png",
    "fighting": "fighting.png",
    "fire": "fire.png",
    "flying": "flying.png",
    "ghost": "ghost.png",
    "grass": "grass.png",
    "ground": "ground.png",
    "ice": "ice.png",
    "normal": "normal.png",
    "poison": "poison.png",
    "psychic": "psychic.png",
    "rock": "rock.png",
    "steel": "steel.png",
    "water": "water.png",
}

STAT_LABELS = ["HP", "ATQ", "DEF", "AES", "DES", "VEL"]
STAT_COLORS = [
    (120, 200, 160),
    (120, 170, 210),
    (200, 160, 120),
    (190, 140, 200),
    (220, 180, 120),
    (160, 210, 180),
]
STAT_BG_GRAY = (180, 180, 180, 77)

# ---------------- DATA ----------------
POKEMONS = {
    "bulbasaur": {"type": "Grass, Poison", "stats": [45, 49, 49, 65, 65, 45]},
    "charmander": {"type": "Fire", "stats": [39, 52, 43, 60, 50, 65]},
    "squirtle": {"type": "Water", "stats": [44, 48, 65, 50, 64, 43]},
    "pikachu": {"type": "Electric", "stats": [35, 55, 40, 50, 50, 90]},
    "gastly": {"type": "Ghost, Poison", "stats": [30, 35, 30, 100, 35, 80]},
    "machop": {"type": "Fighting", "stats": [70, 80, 50, 35, 35, 35]},
}

# ---------------- FONTS ----------------
font_title = ImageFont.truetype(FONT_PATH, 54)
font_total = ImageFont.truetype(FONT_PATH, 54)
font_value = ImageFont.truetype(FONT_PATH, 43)
font_label = ImageFont.truetype(FONT_PATH, 38)

# ↓ Cambio 2: font de descripción 5 px más chico (43 → 38)
font_description = ImageFont.truetype(FONT_PATH, 38)

BASE_NAME_SIZE = 150
TOP_NAME_MARGIN = 60
MIN_SIDE_MARGIN = 10

LINE_MARGIN_X = 70
LINE_THICKNESS = 5
LINE_GAP_FROM_NAME = 20
TYPE_TEXT_GAP = 20

# ↓ Cambio 3: márgenes laterales 80 px
DESCRIPTION_MARGIN = 80

DESCRIPTION_GAP_FROM_POKEMON = 20

DESCRIPTION_TEXT = (
    "Un Pokémon conocido por su equilibrio entre fuerza y estrategia. "
    "Su naturaleza lo convierte en una opción versátil tanto en combate "
    "como en exploración."
)

# ---------------- MAIN ----------------
selected = random.sample(list(POKEMONS.items()), 6)

for i, (name, data) in enumerate(selected):

    main_type = data["type"].split(",")[0].strip().lower()
    bg_path = os.path.join(BACKGROUND_DIR, TYPE_BACKGROUND_MAP[main_type])
    base = Image.open(bg_path).convert("RGBA").resize((WIDTH, HEIGHT), Image.LANCZOS)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    o_draw = ImageDraw.Draw(overlay)

    # ---------- Nombre Pokémon ----------
    size = BASE_NAME_SIZE
    display = name.upper()

    while True:
        font_name = ImageFont.truetype(NAME_FONT_PATH, size)
        font_name.set_variation_by_name("Bold")
        if draw.textlength(display, font_name) <= WIDTH - MIN_SIDE_MARGIN * 2:
            break
        size -= 1

    draw.text(
        ((WIDTH - draw.textlength(display, font_name)) // 2, TOP_NAME_MARGIN),
        display,
        font=font_name,
        fill="white",
        stroke_width=3,
        stroke_fill="black"
    )

    # ---------- Línea ----------
    line_y = TOP_NAME_MARGIN + font_name.size + LINE_GAP_FROM_NAME
    draw.rectangle(
        [LINE_MARGIN_X, line_y, WIDTH - LINE_MARGIN_X, line_y + LINE_THICKNESS],
        fill="white"
    )

    # ---------- Tipo ----------
    draw.text(
        (60, line_y + LINE_THICKNESS + TYPE_TEXT_GAP),
        f"Tipo : {data['type']}",
        font=font_title,
        fill="white",
        stroke_width=2,
        stroke_fill="black"
    )

    # ---------- Pokémon ----------
    sprite = Image.open(os.path.join(POKEMON_DIR, f"{name}.png")).convert("RGBA")
    size_p = int(WIDTH * 0.7668)
    sprite = sprite.resize((size_p, size_p), Image.LANCZOS)

    pokemon_y = int(HEIGHT * 0.15) + 80 + POKEMON_Y_OFFSET
    base.paste(sprite, ((WIDTH - size_p) // 2, pokemon_y), sprite)

    # ---------- Descripción ----------
    # ↓ Cambio 1: empezar 10 px más arriba
    desc_y = pokemon_y + size_p + DESCRIPTION_GAP_FROM_POKEMON - 10

    wrapped = textwrap.fill(DESCRIPTION_TEXT, width=60)

    draw.multiline_text(
        (DESCRIPTION_MARGIN, desc_y),
        wrapped,
        font=font_description,
        fill="white",
        align="left",
        spacing=6,
        stroke_width=2,
        stroke_fill="black"
    )

    # ---------- Panel Stats ----------
    panel_bottom = HEIGHT - BOTTOM_MARGIN - 4 + PANEL_Y_OFFSET
    panel_top = panel_bottom - PANEL_HEIGHT
    panel_left, panel_right = 60, WIDTH - 60

    draw.rectangle([panel_left, panel_top, panel_right, panel_bottom], outline="white", width=2)
    draw.text((panel_left + 20, panel_top + 14), "Estadísticas", font=font_title, fill="white")

    total = sum(data["stats"])
    draw.text(
        (panel_right - draw.textlength(f"Total: {total}", font_total) - 20, panel_top + 14),
        f"Total: {total}",
        font=font_total,
        fill="white"
    )

    bars_top = panel_top + 102
    bars_bottom = panel_bottom - 58
    bars_height = bars_bottom - bars_top

    bar_width = 120
    gap = 24
    max_stat = 120
    num_bars = len(data["stats"])

    usable_width = (panel_right - panel_left) - 40  # 20 px por lado
    total_bars_width = num_bars * bar_width + (num_bars - 1) * gap
    container_left = panel_left + 20 + (usable_width - total_bars_width) // 2

    for idx, v in enumerate(data["stats"]):
        x = int(container_left + idx * (bar_width + gap))

        o_draw.rectangle([x, bars_top, x + bar_width, bars_bottom], fill=STAT_BG_GRAY)

        h = int((v / max_stat) * bars_height)
        y_top = bars_bottom - h

        draw.rectangle([x, y_top, x + bar_width, bars_bottom], fill=STAT_COLORS[idx])
        draw.rectangle([x, bars_top, x + bar_width, bars_bottom], outline="black", width=2)

        val_text = str(v)
        vw = draw.textlength(val_text, font_value)
        value_y = y_top + 4 if v >= 90 else y_top - 56

        draw.text(
            (x + (bar_width - vw) // 2, value_y),
            val_text,
            font=font_value,
            fill="white",
            stroke_width=1,
            stroke_fill="black"
        )

        draw.text(
            (x + bar_width // 2, bars_bottom + 28),
            STAT_LABELS[idx],
            font=font_label,
            fill="white",
            anchor="mm"
        )

    final = Image.alpha_composite(base, overlay)
    final.save(os.path.join(OUTPUT_DIR, f"sample_{i+1}_{name}.png"))

print("✅ Descripción ajustada: posición, tamaño y márgenes.")
=======
from PIL import Image, ImageDraw, ImageFont
import os
import random
import textwrap

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 1080, 1920
BOTTOM_MARGIN = 6
PANEL_HEIGHT = 520
PANEL_Y_OFFSET = -32

POKEMON_Y_OFFSET = 30

FONT_PATH = "fonts/Montserrat-Regular.ttf"
NAME_FONT_PATH = "fonts/Roboto-VariableFont_wdth,wght.ttf"

OUTPUT_DIR = "output"
POKEMON_DIR = "images/pokemon"
BACKGROUND_DIR = r"D:\Proyectos\Youtube\PokemonGO\backgrounds"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- TYPE → BACKGROUND ----------------
TYPE_BACKGROUND_MAP = {
    "bug": "bug.png",
    "dark": "dark.png",
    "dragon": "dragon.png",
    "electric": "electric.png",
    "fairy": "fairy.png",
    "fighting": "fighting.png",
    "fire": "fire.png",
    "flying": "flying.png",
    "ghost": "ghost.png",
    "grass": "grass.png",
    "ground": "ground.png",
    "ice": "ice.png",
    "normal": "normal.png",
    "poison": "poison.png",
    "psychic": "psychic.png",
    "rock": "rock.png",
    "steel": "steel.png",
    "water": "water.png",
}

STAT_LABELS = ["HP", "ATQ", "DEF", "AES", "DES", "VEL"]
STAT_COLORS = [
    (120, 200, 160),
    (120, 170, 210),
    (200, 160, 120),
    (190, 140, 200),
    (220, 180, 120),
    (160, 210, 180),
]
STAT_BG_GRAY = (180, 180, 180, 77)

# ---------------- DATA ----------------
POKEMONS = {
    "bulbasaur": {"type": "Grass, Poison", "stats": [45, 49, 49, 65, 65, 45]},
    "charmander": {"type": "Fire", "stats": [39, 52, 43, 60, 50, 65]},
    "squirtle": {"type": "Water", "stats": [44, 48, 65, 50, 64, 43]},
    "pikachu": {"type": "Electric", "stats": [35, 55, 40, 50, 50, 90]},
    "gastly": {"type": "Ghost, Poison", "stats": [30, 35, 30, 100, 35, 80]},
    "machop": {"type": "Fighting", "stats": [70, 80, 50, 35, 35, 35]},
}

# ---------------- FONTS ----------------
font_title = ImageFont.truetype(FONT_PATH, 54)
font_total = ImageFont.truetype(FONT_PATH, 54)
font_value = ImageFont.truetype(FONT_PATH, 43)
font_label = ImageFont.truetype(FONT_PATH, 38)

# ↓ Cambio 2: font de descripción 5 px más chico (43 → 38)
font_description = ImageFont.truetype(FONT_PATH, 38)

BASE_NAME_SIZE = 150
TOP_NAME_MARGIN = 40
MIN_SIDE_MARGIN = 10

LINE_MARGIN_X = 70
LINE_THICKNESS = 5
LINE_GAP_FROM_NAME = 20
TYPE_TEXT_GAP = 20

# ↓ Cambio 3: márgenes laterales 80 px
DESCRIPTION_MARGIN = 60

DESCRIPTION_GAP_FROM_POKEMON = 20

DESCRIPTION_TEXT = (
    "Un Pokémon conocido por su equilibrio entre fuerza y estrategia. "
    "Su naturaleza lo convierte en una opción versátil tanto en combate "
    "como en exploración."
)

# ---------------- MAIN ----------------
selected = random.sample(list(POKEMONS.items()), 6)

for i, (name, data) in enumerate(selected):

    main_type = data["type"].split(",")[0].strip().lower()
    bg_path = os.path.join(BACKGROUND_DIR, TYPE_BACKGROUND_MAP[main_type])
    base = Image.open(bg_path).convert("RGBA").resize((WIDTH, HEIGHT), Image.LANCZOS)

    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    o_draw = ImageDraw.Draw(overlay)

    # ---------- Nombre Pokémon ----------
    size = BASE_NAME_SIZE
    display = name.upper()

    while True:
        font_name = ImageFont.truetype(NAME_FONT_PATH, size)
        font_name.set_variation_by_name("Bold")
        if draw.textlength(display, font_name) <= WIDTH - MIN_SIDE_MARGIN * 2:
            break
        size -= 1

    draw.text(
        ((WIDTH - draw.textlength(display, font_name)) // 2, TOP_NAME_MARGIN),
        display,
        font=font_name,
        fill="white",
        stroke_width=3,
        stroke_fill="black"
    )

    # ---------- Línea ----------
    line_y = TOP_NAME_MARGIN + font_name.size + LINE_GAP_FROM_NAME
    draw.rectangle(
        [LINE_MARGIN_X, line_y, WIDTH - LINE_MARGIN_X, line_y + LINE_THICKNESS],
        fill="white"
    )

    # ---------- Tipo ----------
    draw.text(
        (60, line_y + LINE_THICKNESS + TYPE_TEXT_GAP),
        f"Tipo : {data['type']}",
        font=font_title,
        fill="white",
        stroke_width=2,
        stroke_fill="black"
    )

    # ---------- Pokémon ----------
    sprite = Image.open(os.path.join(POKEMON_DIR, f"{name}.png")).convert("RGBA")
    size_p = int(WIDTH * 0.7668)
    sprite = sprite.resize((size_p, size_p), Image.LANCZOS)

    pokemon_y = int(HEIGHT * 0.15) + 80 + POKEMON_Y_OFFSET
    base.paste(sprite, ((WIDTH - size_p) // 2, pokemon_y), sprite)

    # ---------- Descripción ----------
    # ↓ Cambio 1: empezar 10 px más arriba
    desc_y = pokemon_y + size_p + DESCRIPTION_GAP_FROM_POKEMON - 10

    wrapped = textwrap.fill(DESCRIPTION_TEXT, width=60)

    draw.multiline_text(
        (DESCRIPTION_MARGIN, desc_y),
        wrapped,
        font=font_description,
        fill="white",
        align="left",
        spacing=6,
        stroke_width=2,
        stroke_fill="black"
    )

    # ---------- Panel Stats ----------
    panel_bottom = HEIGHT - BOTTOM_MARGIN - 4 + PANEL_Y_OFFSET
    panel_top = panel_bottom - PANEL_HEIGHT
    panel_left, panel_right = 60, WIDTH - 60

    draw.rectangle([panel_left, panel_top, panel_right, panel_bottom], outline="white", width=2)
    draw.text((panel_left + 20, panel_top + 14), "Estadísticas", font=font_title, fill="white")

    total = sum(data["stats"])
    draw.text(
        (panel_right - draw.textlength(f"Total: {total}", font_total) - 20, panel_top + 14),
        f"Total: {total}",
        font=font_total,
        fill="white"
    )

    bars_top = panel_top + 102
    bars_bottom = panel_bottom - 58
    bars_height = bars_bottom - bars_top

    bar_width = 120
    gap = 24
    max_stat = 120
    num_bars = len(data["stats"])

    usable_width = (panel_right - panel_left) - 40  # 20 px por lado
    total_bars_width = num_bars * bar_width + (num_bars - 1) * gap
    container_left = panel_left + 20 + (usable_width - total_bars_width) // 2

    for idx, v in enumerate(data["stats"]):
        x = int(container_left + idx * (bar_width + gap))

        o_draw.rectangle([x, bars_top, x + bar_width, bars_bottom], fill=STAT_BG_GRAY)

        h = int((v / max_stat) * bars_height)
        y_top = bars_bottom - h

        draw.rectangle([x, y_top, x + bar_width, bars_bottom], fill=STAT_COLORS[idx])
        draw.rectangle([x, bars_top, x + bar_width, bars_bottom], outline="black", width=2)

        val_text = str(v)
        vw = draw.textlength(val_text, font_value)
        value_y = y_top + 4 if v >= 90 else y_top - 56

        draw.text(
            (x + (bar_width - vw) // 2, value_y),
            val_text,
            font=font_value,
            fill="white",
            stroke_width=1,
            stroke_fill="black"
        )

        draw.text(
            (x + bar_width // 2, bars_bottom + 28),
            STAT_LABELS[idx],
            font=font_label,
            fill="white",
            anchor="mm"
        )

    final = Image.alpha_composite(base, overlay)
    final.save(os.path.join(OUTPUT_DIR, f"sample_{i+1}_{name}.png"))

print("✅ Descripción ajustada: posición, tamaño y márgenes.")
>>>>>>> 766b0c0 (Actualización: descripción movida 20px izquierda y 20px arriba)
