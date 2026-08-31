from pathlib import Path
from urllib.request import urlretrieve
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PHOTO_PATH = ROOT / "assets" / "about" / "about.png"
FAVICON_PATH = ROOT / "favicon.png"
OUTPUT_DIR = ROOT / "assets" / "og"
OUTPUT_PATH = OUTPUT_DIR / "og-preview.jpg"
FONT_PATH = Path("/tmp/GolosText.ttf")
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/golostext/GolosText%5Bwght%5D.ttf"

W, H = 1200, 630
BG = "#ffffff"
SURFACE = "#fafafa"
PHOTO_BG = "#f4eee7"
PHOTO_BORDER = "#eadfd4"
TEXT = "#171717"
MUTED = "#6d6d6d"
ACCENT = "#e86819"
LINE = "#e6e6e6"


def get_font(size: int, weight: int = 400):
    if not FONT_PATH.exists():
        urlretrieve(FONT_URL, FONT_PATH)
    font = ImageFont.truetype(str(FONT_PATH), size)
    try:
        font.set_variation_by_axes([weight])
    except Exception:
        pass
    return font


def fit_rgba(image: Image.Image, max_w: int, max_h: int) -> Image.Image:
    image = image.convert("RGBA")
    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)
    w, h = image.size
    scale = min(max_w / w, max_h / h)
    return image.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)


def draw_centered(draw, xy, text, font, fill):
    x1, y1, x2, y2 = xy
    box = draw.textbbox((0, 0), text, font=font)
    tw = box[2] - box[0]
    th = box[3] - box[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - box[1]), text, font=font, fill=fill)


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)

font_kicker = get_font(22, 650)
font_title = get_font(69, 650)
font_body = get_font(27, 450)
font_name = get_font(25, 650)
font_small = get_font(19, 500)
font_badge = get_font(19, 600)

# Subtle site-like geometry, deliberately neutral/cream rather than green.
draw.rectangle((0, 0, W, H), fill=BG)
draw.rectangle((0, H - 10, W, H), fill=ACCENT)
draw.ellipse((930, -180, 1280, 170), fill="#fff5ed")
draw.ellipse((-170, 430, 190, 790), fill="#faf5ef")

# Brand line.
if FAVICON_PATH.exists():
    logo = Image.open(FAVICON_PATH).convert("RGBA")
    logo.thumbnail((58, 58), Image.Resampling.LANCZOS)
    canvas.paste(logo, (74, 58), logo)
    name_x = 148
else:
    name_x = 74

draw.text((name_x, 58), "Дмитрий Маков", font=font_name, fill=TEXT)
draw.text((name_x, 91), "преподаватель информатики", font=font_small, fill=MUTED)

# Main copy.
draw.text((74, 162), "ЕГЭ ПО ИНФОРМАТИКЕ · 10–11 КЛАСС", font=font_kicker, fill=ACCENT)
draw.multiline_text((74, 206), "Подготовка к ЕГЭ\nпо информатике", font=font_title, fill=TEXT, spacing=4)
draw.text((74, 382), "от базы до 80+ баллов", font=font_body, fill=TEXT)
draw.text((74, 426), "Python с нуля · бесплатное пробное занятие", font=font_body, fill=MUTED)

# Compact proof badges using the same rectangular visual language as the site.
badges = [
    ("81 балл", "средний результат"),
    ("с 2019", "готовлю к экзаменам"),
]
x = 74
for strong, caption in badges:
    box_w = 252
    draw.rounded_rectangle((x, 500, x + box_w, 568), radius=2, fill=SURFACE, outline=LINE, width=1)
    draw.text((x + 18, 512), strong, font=font_badge, fill=TEXT)
    draw.text((x + 18, 540), caption, font=font_small, fill=MUTED)
    x += box_w + 14

# Photo card: warm cream, matching the site portrait treatment.
card = (760, 42, 1132, 596)
draw.rounded_rectangle(card, radius=2, fill=PHOTO_BG, outline=PHOTO_BORDER, width=2)
draw.rectangle((760, 586, 1132, 596), fill=ACCENT)

photo = Image.open(PHOTO_PATH).convert("RGBA")
photo = fit_rgba(photo, 350, 530)
px = 760 + (372 - photo.width) // 2
py = 586 - photo.height
canvas.paste(photo, (px, py), photo)

# Tiny site label inside photo card.
draw.rounded_rectangle((785, 68, 930, 108), radius=2, fill="#ffffff", outline=PHOTO_BORDER, width=1)
draw_centered(draw, (785, 68, 930, 108), "makof.ru", font_small, TEXT)

canvas.save(OUTPUT_PATH, "JPEG", quality=94, subsampling=0, optimize=True)
print(f"Built {OUTPUT_PATH} ({W}x{H}) using Golos Text")
