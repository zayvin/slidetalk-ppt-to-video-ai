#!/usr/bin/env python3
"""Publish this resource kit as a static site. Requires Python 3.9+ and Pandoc."""
import argparse
from html import escape, unescape
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import shutil
import subprocess
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("guides", "examples", "handbook", "templates", "use-cases", "compare", "faq", "images")
# Sections written in Chinese by default. Everything else is treated as English.
CHINESE_SECTIONS = {"use-cases", "compare", "faq"}
LANGUAGES = {
    "en": ("English", "Guides by language", "Skip to content"),
    "zh-CN": ("简体中文", "按语言浏览指南", "跳至正文"),
    "zh-TW": ("繁體中文", "依語言瀏覽指南", "跳至內文"),
    "ar": ("العربية", "الأدلة حسب اللغة", "انتقل إلى المحتوى"),
    "de": ("Deutsch", "Anleitungen nach Sprache", "Zum Inhalt"),
    "es": ("Español", "Guías por idioma", "Ir al contenido"),
    "fr": ("Français", "Guides par langue", "Aller au contenu"),
    "hi": ("हिन्दी", "भाषा के अनुसार गाइड", "सामग्री पर जाएँ"),
    "it": ("Italiano", "Guide per lingua", "Vai al contenuto"),
    "ja": ("日本語", "言語別のガイド", "本文へ移動"),
    "ko": ("한국어", "언어별 가이드", "본문으로 이동"),
    "nb": ("Norsk bokmål", "Veiledninger etter språk", "Hopp til innholdet"),
    "nl": ("Nederlands", "Handleidingen per taal", "Naar de inhoud"),
    "pt": ("Português", "Guias por idioma", "Ir para o conteúdo"),
    "ru": ("Русский", "Руководства по языкам", "Перейти к содержанию"),
    "sv": ("Svenska", "Guider efter språk", "Till innehållet"),
}
# route, Chinese label, English label
NAV = (
    ("use-cases/", "使用场景", "Use cases"),
    ("compare/ppt-to-video-tools/", "方案对比", "Compare"),
    ("faq/", "常见问题", "FAQ"),
)
APP_URL = "https://www.slidetalk.online/"
STORE_URL = "https://apps.apple.com/app/id6800015747"
SITE_NAME = "SlideTalk"
OG_IMAGE = "images/og.jpg"


def discover():
    """Map source paths to public routes. Directory routes end with a slash."""
    sources = [ROOT / "README.md", ROOT / "LICENSE.md"]
    # Localized landing pages live at the repository root as README.<locale>.md.
    sources += [p for p in sorted(ROOT.glob("README.*.md")) if p.is_file()]
    for section in SECTIONS:
        for path in sorted((ROOT / section).rglob("*")):
            rel = path.relative_to(ROOT)
            if path.is_file() and not path.is_symlink() and not any(p.startswith(".") for p in rel.parts):
                sources.append(path)
    routes = {}
    for path in sources:
        if not path.is_file():
            raise ValueError(f"Missing required public file: {path.name}")
        name = path.relative_to(ROOT).as_posix()
        if path.name == "README.md":
            route = name[:-len("README.md")]
        elif path.parent == ROOT and path.name.startswith("README."):
            route = path.stem[len("README."):] + "/"
        elif path.suffix == ".md":
            route = name[:-len(".md")] + "/"
        else:
            route = name
        if route in routes.values():
            raise ValueError(f"Duplicate output route: {route}")
        routes[name] = route
    return routes


def relative_url(source_route, target_route):
    origin = source_route if source_route.endswith("/") else posixpath.dirname(source_route)
    rel = posixpath.relpath(target_route or ".", origin or ".")
    if target_route.endswith("/") or not target_route:
        rel += "/"
    return quote(rel, safe="/~")


def page_locale(source):
    if source == "README.md":
        return "en"
    parts = PurePosixPath(source).parts
    if len(parts) == 1 and parts[0].startswith("README."):
        return PurePosixPath(source).stem.split(".", 1)[1]
    if len(parts) > 2 and parts[0] == "guides":
        return parts[1]
    if parts[0] in CHINESE_SECTIONS:
        return "zh-CN"
    return "en"


def is_landing_page(source):
    return "/" not in source and source.startswith("README")


class Article(HTMLParser):
    """Rewrite repository links in HTML produced by Pandoc, keeping the article text."""
    def __init__(self, source, routes):
        super().__init__(convert_charrefs=False)
        self.source, self.routes = source, routes
        self.parts, self.ids, self.fragments = [], set(), []
        self.capture, self.buffer = "", []
        self.title, self.description = "", ""
        self.question, self.qa = "", []

    def rewrite(self, value):
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc:
            if parsed.hostname in {"slidetalk.online", "www.slidetalk.online"} and parsed.query:
                fields = parse_qsl(parsed.query, keep_blank_values=True)
                if ("utm_source", "github") in fields:
                    query = urlencode([(k, "github_pages" if (k, v) == ("utm_source", "github") else v)
                                       for k, v in fields])
                    return parsed._replace(query=query).geturl()
            return value
        if parsed.path:
            path = unquote(parsed.path)
            if path.startswith("/"):
                target = posixpath.normpath(path.lstrip("/"))
            else:
                target = posixpath.normpath(posixpath.join(posixpath.dirname(self.source), path))
            if target not in self.routes:
                target = posixpath.normpath(posixpath.join(target, "README.md"))
            if target not in self.routes:
                raise ValueError(f"{self.source}: missing or unpublished link {value!r}")
            href = relative_url(self.routes[self.source], self.routes[target])
        else:
            target, href = self.source, ""
        if parsed.fragment and target.endswith(".md"):
            self.fragments.append((target, unquote(parsed.fragment), value))
        return urlunsplit(("", "", href, parsed.query, parsed.fragment))

    def start_element(self, tag, attrs, closing):
        new_attrs = []
        for key, value in attrs:
            if key in {"href", "src", "poster"} and value:
                value = self.rewrite(value)
            if key in {"id", "name"} and value:
                self.ids.add(value)
            new_attrs.append(f' {key}="{escape(value, quote=True)}"' if value is not None else f" {key}")
        self.parts.append("<" + tag + "".join(new_attrs) + closing)
        if tag in {"h1", "h3", "p"}:
            self.capture, self.buffer = tag, []

    def handle_starttag(self, tag, attrs):
        self.start_element(tag, attrs, ">")

    def handle_startendtag(self, tag, attrs):
        self.start_element(tag, attrs, " />")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")
        if tag == self.capture:
            text = " ".join("".join(self.buffer).split())
            if tag == "h1" and not self.title:
                self.title = text
            if tag == "h3":
                self.question = text
            if tag == "p":
                if not self.description and len(text) >= 35:
                    self.description = text
                if self.question and len(text) >= 20:
                    self.qa.append((self.question, text))
                    self.question = ""
            self.capture = ""
            self.buffer = []

    def handle_data(self, data):
        self.parts.append(data)
        if self.capture:
            self.buffer.append(data)

    def handle_entityref(self, name):
        self.parts.append("&" + name + ";")
        if self.capture:
            self.buffer.append(unescape(self.parts[-1]))

    def handle_charref(self, name):
        self.handle_entityref("#" + name)

    def handle_comment(self, data):
        self.parts.append("<!--" + data + "-->")


def load_articles(routes):
    articles = {}
    for source in routes:
        if not source.endswith(".md"):
            continue
        html = subprocess.run(
            ["pandoc", "--from=gfm", "--to=html5", "--wrap=none", source],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout
        article = Article(source, routes)
        article.feed(html)
        article.close()
        if not article.title:
            raise ValueError(f"{source}: page needs a level-one heading")
        articles[source] = article
    for article in articles.values():
        for target, fragment, value in article.fragments:
            if fragment not in articles[target].ids:
                raise ValueError(f"{article.source}: missing heading or anchor {value!r}")
    return articles


def structured_data(article, route, base_url, locale):
    """Schema.org markup that helps search engines and rich results."""
    canonical = base_url + "/" + quote(route, safe="/~")
    graph = []
    if is_landing_page(article.source):
        graph.append({
            "@type": "WebSite",
            "@id": base_url + "/#website",
            "url": base_url + "/",
            "name": f"{SITE_NAME} · PPT to Video Creator Kit",
            "description": article.description or article.title,
            "inLanguage": locale,
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": APP_URL},
        })
        graph.append({
            "@type": "SoftwareApplication",
            "@id": base_url + "/#app",
            "name": "SlideTalk",
            "alternateName": "PPT讲解员",
            "applicationCategory": "MultimediaApplication",
            "applicationSubCategory": "PPT to video converter",
            "operatingSystem": "macOS 15.1 or later, iOS 17 or later, iPadOS 17 or later",
            "url": APP_URL,
            "downloadUrl": STORE_URL,
            "installUrl": STORE_URL,
            "inLanguage": ["zh-CN", "en"],
            "featureList": [
                "AI narration script per slide",
                "58 AI voices in Chinese and English",
                "Burned-in subtitles plus sidecar SRT",
                "Six scene animations and Ken Burns motion",
                "On-device AVFoundation rendering up to 4K",
                "AI cover, title, description, tags and chapters",
            ],
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
                "description": "Free download. Import, editing, voice preview, rendering and export are free; AI generation is metered with credits.",
                "url": STORE_URL,
            },
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": APP_URL},
        })
    if article.qa and article.source.startswith("faq/"):
        graph.append({
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "url": canonical,
            "inLanguage": locale,
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in article.qa[:40]
            ],
        })
    if not graph:
        return ""
    payload = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + payload.replace("</", "<\\/") + "</script>"


def navigation(route, routes, locale):
    labels = 1 if locale in {"zh-CN", "zh-TW"} else 2
    links = []
    for target, zh, en in NAV:
        if target in routes.values():
            current = ' aria-current="page"' if route == target else ""
            links.append(f'<a href="{relative_url(route, target)}"{current}>{zh if labels == 1 else en}</a>')
    return '<div class="links">' + "".join(links) + f'<a class="cta" href="{STORE_URL}">App Store</a></div>'


def render_article(article, route, base_url, guides, verification, routes):
    locale = page_locale(article.source)
    native, lang_label, skip = LANGUAGES[locale]
    canonical = base_url + "/" + quote(route, safe="/~")
    language_home = is_landing_page(article.source) or route == guides.get(locale)
    alternate = []
    if is_landing_page(article.source):
        # The README.<locale>.md files are translated landing pages: point them at
        # each other so search engines pick one version per language.
        homes = {page_locale(src): target for src, target in routes.items() if is_landing_page(src)}
        for code, home in sorted(homes.items()):
            alternate.append(f'<link rel="alternate" hreflang="{code}" href="{escape(base_url)}/{home}">')
        alternate.append(f'<link rel="alternate" hreflang="x-default" href="{escape(base_url)}/">')
    elif language_home:
        for code, guide in guides.items():
            alternate.append(f'<link rel="alternate" hreflang="{code}" href="{escape(base_url)}/{guide}">')
        alternate.append(f'<link rel="alternate" hreflang="x-default" href="{escape(base_url)}/">')
    menu = []
    for code, guide in guides.items():
        lang_name = LANGUAGES[code][0]
        current = ' aria-current="page"' if guide == route else ""
        menu.append(f'<a href="{relative_url(route, guide)}" lang="{code}" hreflang="{code}" dir="auto"{current}>{lang_name}</a>')
    meta = ""
    if verification:
        meta = f'<meta name="google-site-verification" content="{escape(verification, quote=True)}">'
    desc = article.description or article.title
    if len(desc) > 180:
        desc = desc[:177].rstrip() + "…"
    page_title = article.title if SITE_NAME in article.title else f"{article.title} | {SITE_NAME}"
    # Prefer a localized social card when one exists, e.g. images/zh-CN/og.jpg.
    og_path = f"images/{locale}/og.jpg" if f"images/{locale}/og.jpg" in routes else OG_IMAGE
    og_image = escape(base_url + "/" + og_path) if og_path in routes else ""
    og_alt = ("SlideTalk 把 PPT 变成带 AI 配音、字幕和封面的讲解视频。"
              if locale in {"zh-CN", "zh-TW"} else
              "SlideTalk turns a PowerPoint deck into a narrated video with subtitles, cover and titles.")
    social = ""
    if og_image:
        social = f"""<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og_image}">"""
    schema = structured_data(article, route, base_url, locale)
    return f"""<!doctype html>
<html lang="{locale}" dir="{'rtl' if locale == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(page_title)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{escape(canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:locale" content="{locale.replace('-', '_')}">
<meta property="og:title" content="{escape(page_title, quote=True)}">
<meta property="og:description" content="{escape(desc, quote=True)}">
<meta property="og:url" content="{escape(canonical)}">
<meta name="twitter:title" content="{escape(page_title, quote=True)}">
<meta name="twitter:description" content="{escape(desc, quote=True)}">
{social}
{chr(10).join(alternate)}
{meta}
{schema}
<link rel="icon" href="{relative_url(route, 'images/icon.png')}" type="image/png">
<link rel="apple-touch-icon" href="{relative_url(route, 'images/icon.png')}">
<link rel="stylesheet" href="{relative_url(route, 'assets/site.css')}">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header><nav><a class="brand" href="{relative_url(route, '')}" dir="ltr"><span aria-hidden="true">▶</span> {SITE_NAME}</a>
{navigation(route, routes, locale)}
<details><summary>{lang_label}</summary><div class="languages">{''.join(menu)}</div></details></nav></header>
<main id="main" tabindex="-1"><article>{''.join(article.parts)}</article></main>
<footer><a href="{relative_url(route, '')}" dir="ltr">{SITE_NAME}</a><span lang="{locale}">{native}</span></footer>
</body>
</html>
"""


def llms_index(articles, routes, base_url):
    """A plain-text map for answer engines, following the llms.txt convention."""
    lines = [
        f"# {SITE_NAME} · PPT to Video Creator Kit",
        "",
        "> Free, reusable material for turning PowerPoint decks and PDFs into narrated videos with "
        "AI voiceover, subtitles, scene animations and publish-ready covers and titles. SlideTalk is an "
        "Apple-native app for macOS, iOS and iPadOS.",
        "",
        "## Start here",
        "",
    ]
    for source, route in routes.items():
        if not source.endswith(".md"):
            continue
        title = articles[source].title
        summary = articles[source].description
        line = f"- [{title}]({base_url}/{route})"
        if summary:
            line += f": {summary[:160]}"
        lines.append(line)
    lines += ["", "## App", "", f"- [SlideTalk product site]({APP_URL})", f"- [App Store]({STORE_URL})", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True, help="Absolute site URL, including the repository subpath")
    parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    parsed = urlsplit(base)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment:
        parser.error("--base-url must be an absolute HTTP(S) URL without a query or fragment")
    output = args.output.resolve()
    if output == ROOT or ROOT.is_relative_to(output) or any(output.is_relative_to(ROOT / p) for p in (*SECTIONS, "tools", ".github")):
        parser.error("--output must be separate from the source files")
    if output.exists() and any(output.iterdir()) and not (output / ".slidetalk-build").is_file():
        parser.error("--output must be empty or contain a previous SlideTalk build")
    routes = discover()
    articles = load_articles(routes)
    guides = {code: routes[f"guides/{code}/README.md"] for code in LANGUAGES if f"guides/{code}/README.md" in routes}
    unknown = {PurePosixPath(p).parts[1] for p in articles if p.startswith("guides/") and len(PurePosixPath(p).parts) > 2} - guides.keys()
    if unknown:
        raise ValueError(f"Unsupported guide locale or missing guide index: {', '.join(sorted(unknown))}")
    if output.exists() and (output / ".slidetalk-build").is_file():
        # Only prune files listed in our last successful build.
        for previous in (output / ".slidetalk-build").read_text().splitlines():
            old = (output / previous).resolve()
            if old.is_relative_to(output) and old.is_file():
                old.unlink()
    output.mkdir(parents=True, exist_ok=True)
    written = []
    for source, route in routes.items():
        dest = output / route
        if source in articles:
            dest /= "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
            html = render_article(articles[source], route, base, guides,
                                  os.getenv("SEARCH_CONSOLE_VERIFICATION", ""), routes)
            dest.write_text(html, encoding="utf-8")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / source, dest)
        written.append(dest.relative_to(output).as_posix())
    (output / "assets").mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "tools/site.css", output / "assets/site.css")
    sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for source in articles:
        ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = base + "/" + quote(routes[source], safe="/~")
    ET.ElementTree(sitemap).write(output / "sitemap.xml", encoding="utf-8", xml_declaration=True)
    (output / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: " + base + "/sitemap.xml\n", encoding="utf-8")
    (output / "llms.txt").write_text(llms_index(articles, routes, base), encoding="utf-8")
    (output / ".slidetalk-build").write_text(
        "\n".join(written + ["assets/site.css", "sitemap.xml", "robots.txt", "llms.txt"]) + "\n", encoding="utf-8")
    print(f"Built {len(articles)} pages and copied {len(routes) - len(articles)} resources into {output}")


if __name__ == "__main__":
    main()
