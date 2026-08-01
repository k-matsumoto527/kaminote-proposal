#!/usr/bin/env python3
"""~/ewc-docs の Artifact 用HTML断片を、GitHub Pages で配れる完全なHTMLに変換する。

Artifact は publish 時に <!doctype>〜<head> とリセットCSSを自動で被せてくれるが、
GitHub Pages は素のファイルをそのまま配信するため、それを自前で用意する必要がある。
特に viewport が無いとスマホでPCレイアウトが縮小表示になる。

原本は ~/ewc-docs/ のままにして、こちらは生成物だけを置く（二重管理を避ける）。
編集は原本に対して行い、このスクリプトを再実行する。
"""

import html
import pathlib
import re

SRC = pathlib.Path.home() / "ewc-docs"
DST = pathlib.Path(__file__).resolve().parent
BASE_URL = "https://k-matsumoto527.github.io/kaminote-proposal"

# Artifact のラッパーが入れてくれるものと同等の最小リセット。
# ul の padding を落としているのは、.cs-list / ul.marks が list-style:none ＋
# 独自マーカーで左端そろえを前提にしているため（既定の40pxが残ると字下げされる）。
RESET = """\
  *, *::before, *::after { box-sizing: border-box; }
  * { margin: 0; }
  ul, ol { padding: 0; }
  body { min-height: 100vh; -webkit-font-smoothing: antialiased; }
  img, picture, video, canvas, svg { display: block; max-width: 100%; }
  input, button, textarea, select { font: inherit; }
  p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }
"""

# 出力ファイル名 → (原本, og:description, 相互リンクの張り替え)
# 断片どうしは Artifact のURLで相互リンクしているので、Pages 側では相対パスに直す。
PAGES = {
    "index.html": {
        "src": "proposal-kaminote.html",
        "desc": "株式会社 A and K さま向けのサイト構成のご提案です。"
                "放課後等デイを事業所ごとに分ける3サイト案と、1つにまとめる2サイト案を"
                "画面の並び（間取り図）つきでご比較いただけます。",
        "links": {},
    },
}

# 構成イメージは提案書に統合したので、単独ページは無くなった。
# 統合前に structure.html のURLを開いた人が404にならないよう、転送だけ残す。
REDIRECTS = {
    "structure.html": ("index.html#s02", "画面の並び ― 間取り図"),
}

REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta http-equiv="refresh" content="0; url={to}">
<link rel="canonical" href="{to}">
<title>{label}｜EasyWebCraft</title>
</head>
<body style="font:16px/1.8 system-ui,sans-serif;padding:2rem">
<p>この内容はご提案書に統合しました。<a href="{to}">{label}へ移動します</a>。</p>
</body>
</html>
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- 特定のお客さま向けの資料なので検索避けする（URLを知っている人は見られる） -->
<meta name="robots" content="noindex, nofollow, noarchive">
<!-- kids-support-sample と同じ丸ゴシック。読めない環境では端末のゴシックに落ちる -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;500;700;900&display=swap" rel="stylesheet">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="EasyWebCraft">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<style>
{reset}</style>
</head>
<body>
{body}
</body>
</html>
"""


def build(out_name, spec):
    raw = (SRC / spec["src"]).read_text(encoding="utf-8")

    # 断片の先頭にある <title> は <head> 側へ引き上げる
    m = re.search(r"<title>(.*?)</title>\s*", raw, re.S)
    if not m:
        raise SystemExit(f"{spec['src']}: <title> が見つかりません")
    title = m.group(1).strip()
    body = (raw[: m.start()] + raw[m.end():]).strip()

    for old, new in spec["links"].items():
        if old not in body:
            raise SystemExit(f"{spec['src']}: 張り替え対象のリンクが見つかりません: {old}")
        body = body.replace(old, new)

    page = TEMPLATE.format(
        title=html.escape(title, quote=True),
        desc=html.escape(spec["desc"], quote=True),
        url=f"{BASE_URL}/{'' if out_name == 'index.html' else out_name}",
        reset=RESET,
        body=body,
    )
    (DST / out_name).write_text(page, encoding="utf-8")
    print(f"{out_name:16s} <- {spec['src']}  ({len(page):,} bytes)  {title}")


if __name__ == "__main__":
    for name, spec in PAGES.items():
        build(name, spec)
    for name, (to, label) in REDIRECTS.items():
        (DST / name).write_text(
            REDIRECT_TEMPLATE.format(to=to, label=html.escape(label, quote=True)),
            encoding="utf-8",
        )
        print(f"{name:16s} -> {to}  (転送)")
