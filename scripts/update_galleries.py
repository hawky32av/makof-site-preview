from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STYLES = ROOT / "styles.css"
REVIEWS = ROOT / "assets" / "reviews"
ACHIEVEMENTS = ROOT / "assets" / "achievements"

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".avif"}


def natural_key(path: Path):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def image_files(folder: Path):
    return sorted(
        [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS],
        key=natural_key,
    )


def review_button(path: Path, kind: str, number: int) -> str:
    rel = path.relative_to(ROOT).as_posix()
    label = "ученика" if kind == "student" else "родителя"
    alt = f"Отзыв {label} {number}"
    return (
        f'<button class="review-slide" type="button" '
        f'data-lightbox-src="{html.escape(rel, quote=True)}" '
        f'data-lightbox-alt="{html.escape(alt, quote=True)}">'
        f'<img src="{html.escape(rel, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="lazy">'
        f'</button>'
    )


def existing_achievement_meta(source: str):
    result = {}
    pattern = re.compile(
        r'<button class="achievement-item"[^>]*data-lightbox-src="(?P<src>assets/achievements/[^"]+)"'
        r'[^>]*data-lightbox-alt="(?P<alt>[^"]*)"[^>]*>.*?<span>(?P<label>.*?)</span></button>',
        re.S,
    )
    for match in pattern.finditer(source):
        result[match.group("src")] = (match.group("alt"), re.sub(r"\s+", " ", match.group("label")).strip())
    return result


def achievement_button(path: Path, meta: dict[str, tuple[str, str]]) -> str:
    rel = path.relative_to(ROOT).as_posix()
    alt, label = meta.get(rel, ("Дополнительный диплом или сертификат", "Диплом или сертификат"))
    return (
        f'<button class="achievement-item" type="button" '
        f'data-lightbox-src="{html.escape(rel, quote=True)}" '
        f'data-lightbox-alt="{html.escape(alt, quote=True)}">'
        f'<img src="{html.escape(rel, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="lazy">'
        f'<span>{label}</span></button>'
    )


def replace_review_group(source: str, heading: str, kind: str, files: list[Path]) -> str:
    buttons = "".join(review_button(path, kind, i + 1) for i, path in enumerate(files))
    pattern = re.compile(
        rf'(<div class="reviews-group">\s*<h3>{re.escape(heading)}</h3>\s*'
        rf'<div class="review-slider" data-review-slider><div class="review-slides" data-swipe-track>)'
        rf'.*?'
        rf'(</div><div class="review-controls"><span class="review-counter" data-review-counter>).*?(</span></div></div>\s*</div>)',
        re.S,
    )
    replacement = rf'\1{buttons}\g<2>1 / {len(files)}\3'
    updated, count = pattern.subn(replacement, source, count=1)
    if count != 1:
        raise RuntimeError(f"Could not update review group: {heading}")
    return updated


def replace_achievements(source: str, files: list[Path]) -> str:
    meta = existing_achievement_meta(source)
    buttons = "\n            ".join(achievement_button(path, meta) for path in files)
    pattern = re.compile(
        r'(<div class="achievement-track" data-achievement-track data-swipe-track>)'
        r'.*?'
        r'(</div>\s*<div class="achievement-controls"><span class="achievement-counter" data-achievement-counter>)'
        r'.*?'
        r'(</span></div>)',
        re.S,
    )
    replacement = rf'\1\n            {buttons}\n          \g<2>{min(4, len(files))} / {len(files)}\3'
    updated, count = pattern.subn(replacement, source, count=1)
    if count != 1:
        raise RuntimeError("Could not update achievements gallery")
    return updated


def make_offer_link_plain(styles: str) -> str:
    styles = re.sub(
        r'\n\.footer-legal \.footer-offer \{.*?\}\n\.footer-legal \.footer-offer:hover \{.*?\}\n',
        "\n",
        styles,
        flags=re.S,
    )
    return styles


def main():
    source = INDEX.read_text(encoding="utf-8")

    student_files = [p for p in image_files(REVIEWS) if p.stem.lower().startswith("student-")]
    parent_files = [p for p in image_files(REVIEWS) if p.stem.lower().startswith("parent-")]
    achievement_files = image_files(ACHIEVEMENTS)

    source = replace_review_group(source, "Ученики", "student", student_files)
    source = replace_review_group(source, "Родители", "parent", parent_files)
    source = replace_achievements(source, achievement_files)
    source = source.replace('class="footer-offer" href="offer.html"', 'href="offer.html"')

    INDEX.write_text(source, encoding="utf-8")

    styles = STYLES.read_text(encoding="utf-8")
    STYLES.write_text(make_offer_link_plain(styles), encoding="utf-8")

    print(f"Student reviews: {len(student_files)}")
    print(f"Parent reviews: {len(parent_files)}")
    print(f"Achievements: {len(achievement_files)}")


if __name__ == "__main__":
    main()
