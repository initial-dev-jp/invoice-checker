import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 1
os.makedirs("_drafts", exist_ok=True)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}｜インボイスT番号・経理実務ガイド</title>
  <meta name="description" content="{description}" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2661516129849212" crossorigin="anonymous"></script>
</head>
<body class="bg-slate-50 text-slate-800 antialiased">
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30">
    <div class="max-w-3xl mx-auto px-4 py-3 flex items-center justify-between">
      <a href="../index.html" class="font-bold text-indigo-600 text-sm">← T番号逆引きチェッカーへ戻る</a>
      <a href="./index.html" class="text-xs font-bold text-slate-600 hover:underline">コラム一覧</a>
    </div>
  </header>

  <main class="max-w-3xl mx-auto px-4 py-6 space-y-6">
    <article class="bg-white p-6 sm:p-8 rounded-xl border border-slate-200 shadow-sm space-y-5 leading-relaxed">
      <div class="inline-block bg-indigo-50 text-indigo-700 text-xs font-bold px-2.5 py-1 rounded">{category}</div>
      <h1 class="text-xl sm:text-2xl font-extrabold text-slate-900">{title}</h1>
      <p class="text-sm text-slate-600 bg-slate-50 p-4 rounded-lg border border-slate-200">{lead}</p>
      
      <div class="space-y-5 text-sm sm:text-base text-slate-700">
        {body_html}
      </div>

      <div class="bg-indigo-50 border border-indigo-200 rounded-xl p-5 text-center space-y-2 mt-6">
        <p class="font-bold text-indigo-900">レシートの店舗名・T番号を今すぐ無料チェック</p>
        <p class="text-xs text-indigo-700">屋号からの運営会社逆引き検索・13桁T番号の打ち間違い判定が10秒で完了します。</p>
        <a href="../index.html" class="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm px-6 py-3 rounded-lg transition">T番号逆引きチェッカーを使う →</a>
      </div>

      <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 mt-4">
        <span class="text-[11px] font-bold bg-amber-500 text-white px-2 py-0.5 rounded">PR・経理業務の自動化</span>
        <p class="text-sm font-bold text-slate-900 mt-1">レシートのT番号手入力・国税庁サイトへの毎回照会をゼロにする方法</p>
        <a href="../index.html#guide" class="inline-block mt-2 text-xs font-bold text-amber-700 underline">インボイス対応の経理効率化ポイントを見る →</a>
      </div>
    </article>

    <nav id="chain-nav" class="grid grid-cols-1 sm:grid-cols-2 gap-3"></nav>
    <section id="related-section" class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-3 hidden">
      <div class="flex items-center justify-between border-b pb-2">
        <h2 class="text-base font-bold text-slate-900">あわせて読みたいインボイス・経理ガイド</h2>
        <a href="./index.html" class="text-xs text-indigo-600 font-bold hover:underline">すべて見る →</a>
      </div>
      <ul id="related-list" class="space-y-2 text-sm"></ul>
    </section>
  </main>

  <footer class="bg-slate-900 text-slate-400 text-xs py-6 mt-12 text-center space-y-2">
    <div>
      <a href="../index.html" class="text-slate-300 hover:underline">T番号チェッカーTOP</a> ｜
      <a href="./index.html" class="text-slate-300 hover:underline">コラム一覧</a> ｜
      <a href="https://sim.initialassetmanagement.com/" class="text-slate-300 hover:underline">住宅ローン・新NISA計算ツール</a>
    </div>
    <p>&copy; 2026 インボイスT番号・経理実務チェッカー事務局</p>
  </footer>

  <script>
    fetch('./articles.json')
      .then(res => res.json())
      .then(articles => {{
        const currentFile = location.pathname.split('/').pop();
        const idx = articles.findIndex(a => a.file === currentFile);
        const nav = document.getElementById('chain-nav');
        if (idx !== -1) {{
          if (idx > 0) {{
            const prev = articles[idx - 1];
            nav.innerHTML += `<a href="./${{prev.file}}" class="p-3 bg-white rounded-lg border border-slate-200 hover:border-indigo-500 text-xs"><span class="text-slate-400 block">← 前の記事</span><span class="font-bold text-slate-800 line-clamp-1">${{prev.title}}</span></a>`;
          }}
          if (idx < articles.length - 1) {{
            const next = articles[idx + 1];
            nav.innerHTML += `<a href="./${{next.file}}" class="p-3 bg-white rounded-lg border border-slate-200 hover:border-indigo-500 text-xs sm:text-right"><span class="text-slate-400 block">次の記事 →</span><span class="font-bold text-slate-800 line-clamp-1">${{next.title}}</span></a>`;
          }}
        }}
        const others = articles.filter(a => a.file !== currentFile);
        if (others.length > 0) {{
          document.getElementById('related-section').classList.remove('hidden');
          const picks = others.sort(() => 0.5 - Math.random()).slice(0, 5);
          document.getElementById('related-list').innerHTML = picks.map(p =>
            `<li><a href="./${{p.file}}" class="block p-2.5 rounded-lg bg-slate-50 hover:bg-indigo-50 text-slate-800 hover:text-indigo-700 font-medium transition">・${{p.title}}</a></li>`
          ).join('');
        }}
      }}).catch(() => {{}});
  </script>
</body>
</html>"""

def call_gemini(prompt):
    res = requests.post(URL, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
    if not res.ok:
        raise RuntimeError(f"APIエラー ({res.status_code}): {res.text}")
    text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    return text.replace("```json", "").replace("```html", "").replace("```", "").strip()

def main():
    topics_file = "_drafts/topics.json"
    if os.path.exists(topics_file):
        with open(topics_file, "r", encoding="utf-8") as f:
            topics = json.load(f)
    else:
        print("8カテゴリ×経理実務切り口で50記事のテーマリストを生成中...")
        topics_prompt = """
        あなたは税理士・経理実務コンサルタント兼SEO編集長です。
        中小企業の経理担当者・個人事業主・フリーランスが検索するインボイス制度・領収書処理・消費税経理に関する記事テーマを、以下の8カテゴリから指定本数ずつ合計50個作成し、JSON配列で出力してください。

        【重要ルール】
        ・似たような表現の繰り返しは禁止。すべて実務上の異なる場面・業種・疑問にフォーカスすること。
        ・タイトルは30〜36文字程度で、実務担当者が思わずクリックしたくなる具体的な悩みに即したものにすること。

        【8カテゴリ構成（合計50本）】
        1. レシート・屋号逆引きの調査術（7本）：店舗名と運営会社名が違うレシートの調べ方、FC加盟店・コインパーキング・個人タクシー・Amazon領収書のT番号確認法など
        2. 少額特例・出張旅費特例・公共交通機関特例（7本）：税込1万円未満の少額特例の適用条件、3万円未満の電車・バス特例、出張日当・宿泊費のインボイス不要ルールなど
        3. 免税事業者との取引・経過措置（8割・5割控除）（6本）：T番号がない相手への仕訳処理、8割控除から5割控除へ移行するタイミング、免税事業者への値下げ交渉・独禁法リスクなど
        4. EC・ネット決済・クレカ明細のインボイス対応（6本）：クレジットカード利用明細だけでは控除不可な理由、ETCカード（ETC利用照会サービス）、Apple・Google・Adobeなど海外事業者のリバースチャージ方式など
        5. 請求書・領収書の記載要件と不備修正（6本）：端数処理（1インボイス1回ルール）の計算ミス、宛名なしレシートが認められる業種（小売・飲食・タクシー）、T番号の打ち間違い・失効確認など
        6. 個人事業主・フリーランスの登録判断（6本）：2割特例の終了時期と本則課税・簡易課税の選び方、インボイス登録すべき売上・取引先基準、登録取消（取りやめ）の手続きなど
        7. 電子帳簿保存法・クラウド会計連携（6本）：スマホ撮影レシートの保存要件、T番号自動照合機能を使った経理時短術、ペーパーレス化の注意点など
        8. 業種別・特殊ケースのインボイス処理（6本）：不動産賃貸（事務所家賃・駐車場）の契約書対応、立替金精算書の作成ルール、従業員の経費精算・慶弔見舞金・交際費の扱いなど

        出力JSONフォーマット（50要素）:
        [{"category": "カテゴリ名", "slug": "unique-english-slug", "title": "記事タイトル"}, ...]
        """
        topics = json.loads(call_gemini(topics_prompt))[:50]
        with open(topics_file, "w", encoding="utf-8") as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)

    target_topics = topics[:LIMIT]
    for i, item in enumerate(target_topics, 1):
        filename = f"_drafts/{i:02d}_{item['slug']}.html"
        if os.path.exists(filename):
            print(f"[{i}/{LIMIT}] スキップ（作成済）: {item['title']}")
            continue
        print(f"[{i}/{LIMIT}] [{item.get('category', '')}] 生成中: {item['title']}")
        article_prompt = f"""
        カテゴリ「{item.get('category', '')}」、タイトル「{item['title']}」の経理実務解説記事をJSON形式で出力してください。
        ・具体的な仕訳例や判定基準の比較表（Tailwind CSSのtableタグ）を必ず1つ入れること
        ・実務上の注意点や税務調査で指摘されやすい落とし穴を必ず1つ盛り込むこと
        ・見出しは <h2 class="text-lg font-bold text-slate-900 border-b pb-1 mt-6"> を使用すること
        出力JSONフォーマット:
        {{"description": "メタディスクリプション110文字", "lead": "結論を先に伝える導入文150文字", "body_html": "本文HTML（h2, p, tableを含む1500文字程度）"}}
        """
        try:
            data = json.loads(call_gemini(article_prompt))
            html = HTML_TEMPLATE.format(
                category=item.get("category", "実務ガイド"),
                title=item["title"],
                description=data["description"],
                lead=data["lead"],
                body_html=data["body_html"]
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"完了: {filename}")
            if LIMIT > 1:
                time.sleep(2)
        except Exception as e:
            print(f"エラー ({i}): {e}")

if __name__ == "__main__":
    main()