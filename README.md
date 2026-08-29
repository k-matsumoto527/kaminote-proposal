# 株式会社 A and K さま ご提案（EasyWebCraft）

株式会社 A and K さま（かみのて保育園・かみのて今渡保育園・かみのてKIDS・かみのてSMILE）向けの、
ホームページ制作のご提案ページ。「かみのてグループ」という法人は存在しないので、宛名・法人名は
必ず「株式会社 A and K」を使う。

- <https://easywebcraft.github.io/kaminote-proposal/>

資料の目的は**サイト構成（家づくりでいう間取り図）を2案から選んでもらうこと**。
デザインの合意でも受注のための提案でもないので、売り込みの要素は置かない。

## 素材

`hero.jpg` は表紙の背景。**松本さんからご提供いただいた写真**（工作をしている手元。顔は写っていない）。
2026-08-01に Unsplash の積み木の写真から差し替えた。

元データは 2.7MB の PNG だったので、JPEG（品質0.78・1453px幅・162KB）に再エンコードしている。
この環境には Pillow も ImageMagick も無いため、ヘッドレスの Edge で canvas に描いて
`toDataURL('image/jpeg')` した結果を取り出す方法で変換した（`build.py` には組み込んでいない）。

差し替えるときは、同じ手順で軽くしてから `hero.jpg` を置き換える。
ストック写真を使う場合は Unsplash の無料ライセンスのものを選ぶこと（**Unsplash+ の有料写真は不可**）。

`index.html` からは相対パスで参照しているので、原本（`src/`）を単体で開くと表紙の写真だけ出ない。

## 中身の直し方

`index.html` は**生成物なので直接編集しない**。原本は `src/proposal-kaminote.html`。

**原本も生成物も一緒にコミットする。** デザインを戻したいときに `git revert` 一発で済むようにするため。
原本をリポジトリの外に置いていた頃は、生成物だけ戻しても次のビルドで元に戻ってしまう事故があった。

もとは提案書と構成イメージの2ページだったが、行き来が発生して読みにくいため1ページに統合した。
`src/archive/kaminote-wireframe.html` は統合前の構成イメージで、**もう公開には使っていない**
（Artifact 版が残っているだけ）。ビルド対象にも入っていない。`structure.html` は統合前のURLを
開いた人のための転送ページで、`build.py` が生成する。

原本は Claude の Artifact 用のHTML断片で、`<!doctype>` や `<head>` を持たない（publish 時に自動で付くため）。
GitHub Pages は素のファイルをそのまま配信するので、`build.py` がその外側とリセットCSSを被せ、
Artifact URL で書かれた相互リンクを相対パスに張り替える。

```sh
# src/proposal-kaminote.html を編集したあとに
python3 build.py
git commit -am "内容を更新" && git push
```

ファイルの置き方:

| パス | 役割 |
| --- | --- |
| `src/proposal-kaminote.html` | **原本**。編集するのはここだけ |
| `src/archive/kaminote-wireframe.html` | 統合前の構成イメージ。ビルドしない |
| `index.html` / `structure.html` | 生成物。直接編集しない |
| `hero.jpg` | 表紙の背景 |
| `build.py` | 原本 → 生成物 |

Artifact 版も使い続けるなら、原本を編集したあと Artifact 側も再 publish する（同じ file_path なら同じURLのまま）。

## 公開範囲

特定のお客さま向けの資料なので `noindex, nofollow, noarchive` を入れてある。
検索には出ないが、**URLを知っていれば誰でも見られる**（GitHub Pages に閲覧制限はかけられない）。
商談が終わったらリポジトリごと消してよい。
