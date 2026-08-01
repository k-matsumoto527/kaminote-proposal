# 株式会社 A and K さま ご提案（EasyWebCraft）

株式会社 A and K さま（かみのて保育園・かみのて今渡保育園・かみのてKIDS・かみのてSMILE）向けの、
ホームページ制作のご提案ページ。「かみのてグループ」という法人は存在しないので、宛名・法人名は
必ず「株式会社 A and K」を使う。

- <https://k-matsumoto527.github.io/kaminote-proposal/>

資料の目的は**サイト構成（家づくりでいう間取り図）を2案から選んでもらうこと**。
デザインの合意でも受注のための提案でもないので、売り込みの要素は置かない。

## 中身の直し方

`index.html` は**生成物なので直接編集しない**。原本は `~/ewc-docs/proposal-kaminote.html`。

もとは提案書と構成イメージの2ページだったが、行き来が発生して読みにくいため1ページに統合した。
`~/ewc-docs/kaminote-wireframe.html` は統合前の構成イメージで、**もう公開には使っていない**
（Artifact 版が残っているだけ）。`structure.html` は統合前のURLを開いた人のための転送ページで、
`build.py` が生成する。

原本は Claude の Artifact 用のHTML断片で、`<!doctype>` や `<head>` を持たない（publish 時に自動で付くため）。
GitHub Pages は素のファイルをそのまま配信するので、`build.py` がその外側とリセットCSSを被せ、
Artifact URL で書かれた相互リンクを相対パスに張り替える。

```sh
# 原本を編集したあとに
python3 build.py
git commit -am "内容を更新" && git push
```

Artifact 版も使い続けるなら、原本を編集したあと Artifact 側も再 publish する（同じ file_path なら同じURLのまま）。

## 公開範囲

特定のお客さま向けの資料なので `noindex, nofollow, noarchive` を入れてある。
検索には出ないが、**URLを知っていれば誰でも見られる**（GitHub Pages に閲覧制限はかけられない）。
商談が終わったらリポジトリごと消してよい。
