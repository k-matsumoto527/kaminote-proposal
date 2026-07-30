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
        "desc": "かみのてグループさま向けのホームページ制作のご提案です。"
                "保育園と放課後等デイサービスのサイト構成を2案でご比較いただけます。",
        "links": {
            "https://claude.ai/code/artifact/361b12e8-b114-4e9a-8d44-83b0a5fe9665": "structure.html",
        },
    },
    "structure.html": {
        "src": "kaminote-wireframe.html",
        "desc": "かみのてグループさまのホームページ構成イメージです。"
                "どのサイトに何のページが入るのかを画面の形でまとめています。",
        "links": {
            "https://claude.ai/code/artifact/c96d6593-c650-4900-b5cd-76dab0714427": "index.html",
        },
    },
}

TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- 特定のお客さま向けの資料なので検索避けする（URLを知っている人は見られる） -->
<meta name="robots" content="noindex, nofollow, noarchive">
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
