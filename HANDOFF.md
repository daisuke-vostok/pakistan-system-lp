# Vostok エンジニアLP — 引き継ぎ書（Phase 1 → 継続）

最終更新: 2026-06-11 / 前担当: Claude (Cowork) → 次担当: Gemini (Antigravity)

---

## 0. これは何
パキスタン人エンジニア向けの採用LP（英語/ウルドゥー語）。GitHub Pagesで公開中。
今回 Phase 1 の一部（金額削除・会社リンク・LP本体の言語トグル）を実装済み。残りを継続する。

## 1. リポジトリ / 公開URL
- リポジトリ: `github.com/daisuke-vostok/pakistan-system-lp`（GitHub Pages, branch: main）
- 公開URL（例）:
  - LP本体: https://daisuke-vostok.github.io/pakistan-system-lp/engineers.html
  - 応募: https://daisuke-vostok.github.io/pakistan-system-lp/apply.html
  - マイページ: https://daisuke-vostok.github.io/pakistan-system-lp/profile.html
  - 規約: terms.html / プライバシー: privacy.html
  - 日本企業向け(別系統・対象外): index.html（日本語クライアントページ）

## 2. ファイルと役割
| ファイル | 役割 | 言語トグル | 備考 |
|---|---|---|---|
| engineers.html | エンジニア向けLP本体 | ✅実装済み | 今回の主成果 |
| apply.html | 応募ページ(Airtable iframe埋込) | ❌未 | フォーム本体はAirtable→Phase2で自作化 |
| profile.html | マイページ(Airtable iframe埋込) | ❌未 | 同上。金額表記なし |
| terms.html | 利用規約(英語が本文+UR要約) | ❌未 | 拘束言語は要法務確認(後述) |
| privacy.html | プライバシー(同上) | ❌未 | 同上 |
| index.html | 日本企業向け(日本語) | 対象外 | Phase1の範囲外 |
| bundle.html | 自動生成の巨大ファイル | 触らない | 8MB。無視 |

## 3. 全体のフェーズ計画（背景）
- **役割分担**: エンジニア対面(応募/認証/マイページ)=将来Supabase / 社内運用(企業/案件/マッチング/粗利)=Airtable。突合はメールアドレス。最終的にSupabaseへ一本化しAirtableは卒業。
- **Phase 1（Supabase不要・完了）**: LP/apply/profile/規約の EN↔UR トグル、$1,500–3,000の金額削除、vostok.co.jpリンク追加。
- **Phase 2（Supabase導入後・フロントエンド実装済）**: 応募フォームを自作化（完全EN/UR・チップUI・規約スクロール読了で同意解放・その場サンクス画面）→ Supabaseに保存。これでエンジニア画面からAirtable要素が消滅。
- **Phase 3（フロントエンド実装済）**: マイページ＝Googleログイン＋マジックリンクの2択認証→自分のデータを直接編集（手動マージ問題が消滅）。
  - 次担当・運用者へ: `apply.html` および `profile.html` の Supabase キーは設定済みです。あとは Supabase 側で RLS と Auth(Google/Email) の設定を完了させてください。

## 4. Phase 1 の現状

### ✅ 完了（engineers.html / apply.html）
1. 金額表示 $1,500–$3,000 を全削除（engineers: ヒーロー大型表示＋"Paid monthly"カード / apply: バッジ）。意味は保持しドル額のみ除去。
2. vostok.co.jp リンク追加（engineers: "A bridge you can verify"カード＋フッター会社情報）。
3. **engineers.html に完全な EN↔UR 言語トグル**（下記「5. トグルの仕組み」参照）。検証済み: HTMLパースOK、翻訳対象107要素、金額ゼロ、JS動作。

### ⬜ 残作業（Phase 1の続き）
- [ ] apply.html に同じ言語トグルを実装（※iframe内のAirtableフォームは英語のまま＝触れない。ページの見出し・バッジ・注記・フッターだけトグル化）
- [ ] profile.html に同じ言語トグルを実装（同上。payinfoの説明文・見出し・フッターをトグル化）
- [ ] terms.html / privacy.html のトグル化（**先に下記「6. 法務上の注意」を読むこと**）
- [ ] 全ページのヘッダーで言語選択を共有（localStorageキー `vostok_lang` を全ページ共通にすれば自動で揃う＝engineersと同じスクリプトを使うだけでOK）

## 5. トグルの仕組み（engineers.htmlで採用・他ページも同方式で）
英語を本文(DOM既定)とし、翻訳が必要な各要素に `data-ur="ウルドゥー語"` を付与。JSが起動時に元の英語HTMLを `data-en` として保存し、切替時に innerHTML を入替。`<html dir>` と `lang` を切替、選択を localStorage に保存。

ヘッダーに追加するトグルUI:
```html
<div class="langtoggle" role="group" aria-label="Language">
  <button type="button" data-l="en" class="active" onclick="setLang('en')">EN</button>
  <button type="button" data-l="ur" onclick="setLang('ur')">اردو</button>
</div>
```

ページ末尾に置くスクリプト（全ページ共通でコピペ可）:
```html
<script>
(function(){
  var nodes = document.querySelectorAll('[data-ur]');
  nodes.forEach(function(el){ el.setAttribute('data-en', el.innerHTML); });
  window.setLang = function(lang){
    var ur = (lang === 'ur');
    nodes.forEach(function(el){
      el.innerHTML = ur ? el.getAttribute('data-ur') : el.getAttribute('data-en');
    });
    document.documentElement.lang = ur ? 'ur' : 'en';
    document.documentElement.dir  = ur ? 'rtl' : 'ltr';
    document.querySelectorAll('.langtoggle button').forEach(function(b){
      b.classList.toggle('active', b.getAttribute('data-l') === lang);
    });
    try{ localStorage.setItem('vostok_lang', lang); }catch(e){}
  };
  var saved = 'en';
  try{ saved = localStorage.getItem('vostok_lang') || 'en'; }catch(e){}
  if(saved === 'ur') setLang('ur');
})();
</script>
```

RTL用の最低限CSS（engineers.htmlの末尾に実装済み。他ページにも同様に）:
```css
html[dir="rtl"] body{font-family:'Noto Nastaliq Urdu','Noto Sans',serif;line-height:2.0;}
html[dir="rtl"] th,html[dir="rtl"] td{text-align:right;}
html[dir="rtl"] .frow{flex-direction:row-reverse;}
html[dir="rtl"] .urdu{display:none;} /* 全文URの時は既存のUR要約ブロックを隠す */
```
 langtoggleのスタイルは engineers.html の `<style>` 内 `.langtoggle{...}` をコピーすれば流用可。

注意点:
- 入れ子にHTMLを含む要素(リンク・`<b>`等)も `data-ur` に同じタグごと入れる（engineersの "bridge" カードや表セルが実例）。
- 属性のクォート: data-ur内に `"` を含むなら属性は `'...'`、`'` を含むなら `"..."`、両方なら `&quot;` を使う。
- SVG内のテキスト(PAKISTAN/JAPAN)は今回そのまま。必要なら別途対応。

## 6. 法務上の注意（terms.html / privacy.html）★重要
現状この2ページは「英語が法的拘束力・ウルドゥー語は参考要約」と明記してある。
ユーザー要望は「規約も全訳トグルにし、英語が本文という建付けを見直す」。

判断はユーザー＋弁護士のもの。技術担当への推奨:
- **全文ウルドゥー語訳は表示してよい（UX/信頼性に良い）。ただし『相違時は英語版が優先する』の一文は残すのが国際標準で安全**（英語を隠すわけではなく、どちらが優先かを定めるだけ）。会社がウルドゥー語を読めない以上、誤訳がそのまま拘束力を持つのはリスク。
- 規約v1.2を弁護士レビューに出す流れがあるので、**サイト規約の拘束言語もそのレビューで確定してから**反映するのが安全。
- 急ぐなら、まず terms/privacy にも「トグルUIと全訳」だけ入れ、優先条項の最終文言だけ弁護士確認待ちにする運用も可。

## 7. デプロイ手順（GitHub Pages）
1. 完成ファイル（このフォルダの engineers.html / apply.html）をリポジトリ直下に上書きコピー。
2. ターミナルで:
   ```bash
   cd <pakistan-system-lp のローカルパス>
   git add engineers.html apply.html
   git commit -m "Phase1: 言語トグル(LP本体)・金額削除・vostok.co.jpリンク"
   git push origin main
   ```
3. 1〜2分後に公開URLへ反映。ブラウザはハードリロード（Cmd+Shift+R）で確認。

## 8. 動作確認チェックリスト
- [ ] engineers.html を開く → ヘッダー右に EN/اردو トグルがある
- [ ] اردو を押す → 全文ウルドゥー語＆右寄せ(RTL)になる、金額表示が無い
- [ ] vostok.co.jp リンクが本文カード＋フッターにある（クリックで開く）
- [ ] リロードしても言語選択が維持される（localStorage）
- [ ] apply.html / profile.html / terms.html / privacy.html にも同トグルが付く（残作業実装後）
- [ ] スマホ幅で崩れない
