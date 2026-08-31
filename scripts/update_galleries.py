from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
STYLES = ROOT / "styles.css"
REVIEWS = ROOT / "assets" / "reviews"
ACHIEVEMENTS = ROOT / "assets" / "achievements"
LEGAL_PAGES = {
    ROOT / "privacy.html": "https://makof.ru/privacy.html",
    ROOT / "consent.html": "https://makof.ru/consent.html",
    ROOT / "offer.html": "https://makof.ru/offer.html",
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".avif"}

# Сохраняем привычный порядок уже опубликованных документов.
# Все новые изображения автоматически добавляются после них.
ACHIEVEMENT_ORDER = [
    "Диплом_RS_338_213172.jpg",
    "olympiad_diploma_2359_participant.jpg",
    "7691998.jpg",
    "1787771425_8956.jpg",
    "5314562.jpg",
    "84095.jpeg",
    "5314622.jpg",
    "1787769122_72944.jpg",
    "diplom.jpg",
    "diplom_author_1120507.jpg",
    "VP100-634258D357556.jpg",
    "umn1-385442.jpg",
    "makov-dmitriy-gennadyevich12.pdf-page1of2.jpg",
    "author.jpg",
]

SEO_BLOCK = '''  <!-- SITE-SEO:START -->
  <link rel="canonical" href="https://makof.ru/">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta name="theme-color" content="#e86819">
  <link rel="icon" href="favicon.png" type="image/png">\n  <link rel="apple-touch-icon" href="favicon.png">

  <meta property="og:locale" content="ru_RU">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Дмитрий Маков — подготовка к ЕГЭ по информатике">
  <meta property="og:title" content="ЕГЭ по информатике — Дмитрий Маков">
  <meta property="og:description" content="10–11 класс · от базы до 80+ баллов · Python с нуля · бесплатное пробное занятие.">
  <meta property="og:url" content="https://makof.ru/">
  <meta property="og:image" content="https://makof.ru/assets/og/og-preview-v2.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:alt" content="Дмитрий Маков — подготовка к ЕГЭ по информатике">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="ЕГЭ по информатике — Дмитрий Маков">
  <meta name="twitter:description" content="10–11 класс · от базы до 80+ баллов · Python с нуля · бесплатное пробное занятие.">
  <meta name="twitter:image" content="https://makof.ru/assets/og/og-preview-v2.jpg">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Person",
        "@id": "https://makof.ru/#person",
        "name": "Дмитрий Маков",
        "url": "https://makof.ru/",
        "jobTitle": "Преподаватель информатики",
        "alumniOf": {
          "@type": "CollegeOrUniversity",
          "name": "Университет ИТМО"
        },
        "knowsAbout": [
          "ЕГЭ по информатике",
          "информатика",
          "Python",
          "программирование"
        ]
      },
      {
        "@type": "Service",
        "@id": "https://makof.ru/#ege-service",
        "name": "Подготовка к ЕГЭ по информатике",
        "serviceType": "Онлайн-подготовка к ЕГЭ по информатике",
        "provider": {"@id": "https://makof.ru/#person"},
        "areaServed": "RU",
        "url": "https://makof.ru/"
      }
    ]
  }
  </script>
  <!-- SITE-SEO:END -->'''

METRIKA_BLOCK = '''  <!-- YANDEX-METRIKA:START -->
  <script>
    (function(m,e,t,r,i,k,a){
      m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
      m[i].l=1*new Date();
      for (var j = 0; j < document.scripts.length; j++) { if (document.scripts[j].src === r) { return; } }
      k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js?id=106373103', 'ym');

    ym(106373103, 'init', {
      ssr: true,
      webvisor: true,
      clickmap: true,
      accurateTrackBounce: true,
      trackLinks: true
    });
  </script>
  <!-- YANDEX-METRIKA:END -->'''

METRIKA_NOSCRIPT = '''  <!-- YANDEX-METRIKA-NOSCRIPT:START -->
  <noscript><div><img src="https://mc.yandex.ru/watch/106373103" style="position:absolute; left:-9999px;" alt=""></div></noscript>
  <!-- YANDEX-METRIKA-NOSCRIPT:END -->'''


def natural_key(path: Path):
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name)]


def image_files(folder: Path):
    return sorted(
        [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS],
        key=natural_key,
    )


def ordered_achievement_files(folder: Path):
    files = image_files(folder)
    by_name = {path.name: path for path in files}
    ordered = [by_name[name] for name in ACHIEVEMENT_ORDER if name in by_name]
    known = set(ACHIEVEMENT_ORDER)
    ordered.extend(path for path in files if path.name not in known)
    return ordered


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
    return re.sub(
        r'\n\.footer-legal \.footer-offer \{.*?\}\n\.footer-legal \.footer-offer:hover \{.*?\}\n',
        "\n",
        styles,
        flags=re.S,
    )


def upsert_marked_block(source: str, start_marker: str, end_marker: str, block: str, anchor: str, before: bool = True) -> str:
    pattern = re.compile(
        rf'\s*{re.escape(start_marker)}.*?{re.escape(end_marker)}\s*',
        re.S,
    )
    if pattern.search(source):
        return pattern.sub("\n" + block + "\n", source, count=1)
    if anchor not in source:
        raise RuntimeError(f"Anchor not found: {anchor}")
    replacement = block + "\n\n" + anchor if before else anchor + "\n" + block
    return source.replace(anchor, replacement, 1)


def add_main_site_meta(source: str) -> str:
    source = upsert_marked_block(
        source,
        "<!-- SITE-SEO:START -->",
        "<!-- SITE-SEO:END -->",
        SEO_BLOCK,
        '  <link rel="preconnect" href="https://fonts.googleapis.com">',
        before=True,
    )
    source = upsert_marked_block(
        source,
        "<!-- YANDEX-METRIKA:START -->",
        "<!-- YANDEX-METRIKA:END -->",
        METRIKA_BLOCK,
        "</head>",
        before=True,
    )
    source = upsert_marked_block(
        source,
        "<!-- YANDEX-METRIKA-NOSCRIPT:START -->",
        "<!-- YANDEX-METRIKA-NOSCRIPT:END -->",
        METRIKA_NOSCRIPT,
        "<body>",
        before=False,
    )
    return source


def update_legal_page(path: Path, canonical_url: str) -> None:
    source = path.read_text(encoding="utf-8")
    source = re.sub(
        r'<meta name="robots" content="[^"]*">',
        '<meta name="robots" content="noindex,follow">',
        source,
        count=1,
    )

    canonical = f'  <link rel="canonical" href="{canonical_url}">\n  <meta name="theme-color" content="#e86819">\n  <link rel="icon" href="favicon.png" type="image/png">\n  <link rel="apple-touch-icon" href="favicon.png">'
    source = upsert_marked_block(
        source,
        "<!-- LEGAL-SEO:START -->",
        "<!-- LEGAL-SEO:END -->",
        f'  <!-- LEGAL-SEO:START -->\n{canonical}\n  <!-- LEGAL-SEO:END -->',
        '  <link rel="preconnect" href="https://fonts.googleapis.com">',
        before=True,
    )
    source = upsert_marked_block(
        source,
        "<!-- YANDEX-METRIKA:START -->",
        "<!-- YANDEX-METRIKA:END -->",
        METRIKA_BLOCK,
        "</head>",
        before=True,
    )

    body_match = re.search(r'<body([^>]*)>', source)
    if body_match:
        source = upsert_marked_block(
            source,
            "<!-- YANDEX-METRIKA-NOSCRIPT:START -->",
            "<!-- YANDEX-METRIKA-NOSCRIPT:END -->",
            METRIKA_NOSCRIPT,
            body_match.group(0),
            before=False,
        )

    path.write_text(source, encoding="utf-8")


def main():
    source = INDEX.read_text(encoding="utf-8")

    student_files = [p for p in image_files(REVIEWS) if p.stem.lower().startswith("student-")]
    parent_files = [p for p in image_files(REVIEWS) if p.stem.lower().startswith("parent-")]
    achievement_files = ordered_achievement_files(ACHIEVEMENTS)

    source = replace_review_group(source, "Ученики", "student", student_files)
    source = replace_review_group(source, "Родители", "parent", parent_files)
    source = replace_achievements(source, achievement_files)
    source = source.replace('class="footer-offer" href="offer.html"', 'href="offer.html"')
    source = add_main_site_meta(source)

    INDEX.write_text(source, encoding="utf-8")

    styles = STYLES.read_text(encoding="utf-8")
    STYLES.write_text(make_offer_link_plain(styles), encoding="utf-8")

    for path, canonical_url in LEGAL_PAGES.items():
        update_legal_page(path, canonical_url)

    print(f"Student reviews: {len(student_files)}")
    print(f"Parent reviews: {len(parent_files)}")
    print(f"Achievements: {len(achievement_files)}")
    print("SEO, canonical URLs and Yandex Metrika: updated")


if __name__ == "__main__":
    main()
