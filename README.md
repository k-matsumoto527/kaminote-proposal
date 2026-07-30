# かみのてグループさま ご提案（EasyWebCraft）

株式会社 A and K／かみのてグループさま向けの、ホームページ制作のご提案ページ。

- ご提案 <https://k-matsumoto527.github.io/kaminote-proposal/>
- 構成イメージ <https://k-matsumoto527.github.io/kaminote-proposal/structure.html>

## 中身の直し方

`index.html` と `structure.html` は**生成物なので直接編集しない**。原本は `~/ewc-docs/` にある。

| 公開ファイル | 原本 |
| --- | --- |
| `index.html` | `~/ewc-docs/proposal-kaminote.html` |
| `structure.html` | `~/ewc-docs/kaminote-wireframe.html` |

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
