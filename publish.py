import os
import glob
import shutil
import re
import json
from datetime import datetime

os.makedirs("columns", exist_ok=True)
drafts = sorted(glob.glob("_drafts/*.html"))

if not drafts:
    print("公開待ちの下書きはありません。")
    exit(0)

target = drafts[0]
basename = os.path.basename(target)
clean_name = re.sub(r"^\d+_", "", basename)
dest = os.path.join("columns", clean_name)

shutil.move(target, dest)
print(f"公開完了: {dest}")

published = sorted(glob.glob("columns/*.html"))
links_html = []
articles_data = []
sitemap_urls = [
    "  <url><loc>[https://invoice.initialassetmanagement.com/](https://invoice.initialassetmanagement.com/)</loc></url>",
    "  <url><loc>[https://invoice.initialassetmanagement.com/columns/](https://invoice.initialassetmanagement.com/columns/)</loc></url>"
]

for path in published:
    fname = os.path.basename(path)
    if fname == "index.html":
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", content)
    title = m.group(1) if m else fname
    articles_data.append({"file": fname, "title": title})
    links_html.append(f'<li><a href="./{fname}" class="block p-4 bg-white rounded-lg border border-slate-200 hover:border-indigo-500 font-bold text-slate-800">{title}</a></li>')
    sitemap_urls.append(f"  <url><loc>[https://invoice.initialassetmanagement.com/columns/](https://invoice.initialassetmanagement.com/columns/){fname}</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>")

with open("columns/articles.json", "w", encoding="utf-8") as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=2)

index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>インボイス制度・経理実務コラム一覧（全{len(articles_data)}記事）</title>
  <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
</head>
<body class="bg-slate-50 text-slate-800">
  <div class="max-w-3xl mx-auto px-4 py-8 space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-xl font-bold">インボイス制度・経理実務ガイド一覧（全{len(articles_data)}記事）</h1>
      <a href="../index.html" class="text-sm text-indigo-600 font-bold">← チェッカーへ戻る</a>
    </div>
    <ul class="space-y-3">{''.join(links_html)}</ul>
  </div>
</body>
</html>"""

with open("columns/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="[http://www.sitemaps.org/schemas/sitemap/0.9](http://www.sitemaps.org/schemas/sitemap/0.9)">
{chr(10).join(sitemap_urls)}
</urlset>"""

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_xml)