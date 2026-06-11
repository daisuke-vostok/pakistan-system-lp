# Antigravity / Gemini に最初に貼るプロンプト

あなたはこのリポジトリ（Vostokのパキスタン人エンジニア向けLP, GitHub Pages公開）の実装を引き継ぎます。
まずリポジトリ直下の `HANDOFF.md` を読んでから着手してください。要点:

## やること（Phase 1の残り）
1. `apply.html` と `profile.html` に、`engineers.html` と同じ EN↔UR 言語トグルを実装する。
   - 仕組みは `HANDOFF.md` の「5. トグルの仕組み」をそのまま流用（ヘッダーのトグルUI＋末尾スクリプト＋RTL用CSS＋`.langtoggle`スタイル）。
   - 翻訳が必要な各テキスト要素に `data-ur="ウルドゥー語訳"` を付ける。`engineers.html` の翻訳トーン・用語に合わせる。
   - **iframe内のAirtableフォームは対象外**（英語のまま。Phase2で自作化予定）。ページの見出し・サブ・バッジ・注記(payinfo)・フッターだけ翻訳トグル化する。
   - localStorageキーは `vostok_lang` で統一（engineersと同じ）。これで全ページ言語選択が共有される。
2. `terms.html` / `privacy.html` のトグル化は、`HANDOFF.md` の「6. 法務上の注意」を必ず確認。
   - 全文ウルドゥー語訳は表示してよいが、「相違時は英語版が優先」の一文は残す方針。
   - 拘束言語の最終確定は弁護士確認待ちなので、不明なら実装せず私(ユーザー)に確認すること。

## ルール
- 既存のデザイン・構造・クラス名は変えない。差分は最小限。
- 変更前に短く実装プランを箇条書きで出して承認を得てから着手。
- ウルドゥー語はネイティブ向け。誤訳に注意し、自信がない箇所はフラグを立てる。
- 各ファイル実装後、ブラウザで EN↔UR 切替・RTL・リロード後の言語維持・スマホ幅崩れを確認。

## 完了後
- `HANDOFF.md`「7. デプロイ手順」に従い、`git add` → `git commit` → `git push origin main`。
- 反映URL: https://daisuke-vostok.github.io/pakistan-system-lp/

不明点は勝手に判断せず、必ず確認してください。
