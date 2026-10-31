#!/usr/bin/env python3
"""Publish this resource kit as a static site. Requires Python 3.9+ and Pandoc."""
import argparse
from html import escape, unescape
from html.parser import HTMLParser
import os
from pathlib import Path, PurePosixPath
import posixpath
import shutil
import subprocess
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("guides", "examples", "handbook", "templates")
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


def discover():
    """Map source paths to public routes. Directory routes end with a slash."""
    sources = [ROOT / "README.md", ROOT / "LICENSE.md"]
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


class Article(HTMLParser):
    """Rewrite repository links in HTML produced by Pandoc, keeping the article text."""
    def __init__(self, source, routes):
        super().__init__(convert_charrefs=False)
        self.source, self.routes = source, routes
        self.parts, self.ids, self.fragments = [], set(), []
        self.capture, self.buffer = "", []
        self.title, self.description = "", ""

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
        if tag in {"h1", "p"}:
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
            if tag == "p" and not self.description and len(text) >= 35:
                self.description = text
            self.capture = ""

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


def render_article(article, route, base_url, guides, verification):
    parts = PurePosixPath(article.source).parts
    locale = parts[1] if len(parts) > 2 and parts[0] == "guides" else "en"
    native, lang_label, skip = LANGUAGES[locale]
    canonical = base_url + "/" + quote(route, safe="/~")
    language_home = article.source == "README.md" or route == guides.get(locale)
    alternate = []
    menu = []
    for code, guide in guides.items():
        lang_name = LANGUAGES[code][0]
        current = ' aria-current="page"' if guide == route else ""
        menu.append(f'<a href="{relative_url(route, guide)}" lang="{code}" hreflang="{code}" dir="auto"{current}>{lang_name}</a>')
        if language_home:
            alternate.append(f'<link rel="alternate" hreflang="{code}" href="{escape(base_url)}/{guide}">')
    if language_home:
        alternate.append(f'<link rel="alternate" hreflang="x-default" href="{escape(base_url)}/">')
    meta = ""
    if verification:
        meta = f'<meta name="google-site-verification" content="{escape(verification, quote=True)}">'
    desc = article.description or article.title
    if len(desc) > 180:
        desc = desc[:177].rstrip() + "…"
    return f"""<!doctype html>
<html lang="{locale}" dir="{'rtl' if locale == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(article.title)} | SlideTalk</title>
<meta name="description" content="{escape(desc, quote=True)}">
<link rel="canonical" href="{escape(canonical)}">
{chr(10).join(alternate)}
{meta}
<link rel="stylesheet" href="{relative_url(route, 'assets/site.css')}">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header><nav><a class="brand" href="{relative_url(route, '')}" dir="ltr"><span aria-hidden="true">▶</span> SlideTalk</a>
<details><summary>{lang_label}</summary><div class="languages">{''.join(menu)}</div></details></nav></header>
<main id="main" tabindex="-1"><article>{''.join(article.parts)}</article></main>
<footer><a href="{relative_url(route, '')}" dir="ltr">SlideTalk</a><span lang="{locale}">{native}</span></footer>
</body>
</html>
"""


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
            html = render_article(articles[source], route, base, guides, os.getenv("SEARCH_CONSOLE_VERIFICATION", ""))
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
    (output / ".slidetalk-build").write_text("\n".join(written + ["assets/site.css", "sitemap.xml"]) + "\n", encoding="utf-8")
    print(f"Built {len(articles)} pages and copied {len(routes) - len(articles)} resources into {output}")


if __name__ == "__main__":
    main()
