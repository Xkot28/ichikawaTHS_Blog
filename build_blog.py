import os
import glob
import re

BLOG_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang='ja'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <link rel='stylesheet' href='index.css'>
    <title>ブログ-千葉県立市川工業高校</title>
    <style>
        .post-body { white-space: pre-wrap; word-wrap: break-word; line-height: 1.6; }
    </style>
</head>
<body>
    <nav>
        <a href='https://xkot28.github.io/ichikawaTHS_website-EA3group/'>Home (概要)</a>
        <a href='index.html'>Blog (活動記録)</a>
    </nav>
    <header>
        <h1>BLOG POSTS</h1>
        <p>日々の活動の記録</p>
    </header>
    <main id='blog-list'>
        <!-- POSTS_GO_HERE -->
    </main>
    <footer><p>&copy; 2023 千葉県立市川工業高校 EA3 Group</p></footer>
</body>
</html>"""

def build_blog_index(blog_root_dir='.'):
    if blog_root_dir != '.':
        os.makedirs(blog_root_dir, exist_ok=True)

    posts_dir = os.path.join(blog_root_dir, 'posts')
    blog_index_path = os.path.join(blog_root_dir, 'index.html')
    os.makedirs(posts_dir, exist_ok=True)

    md_files = glob.glob(os.path.join(posts_dir, '*.md'))

    articles_html = ""
    for md_file in sorted(md_files, key=lambda x: os.path.basename(x), reverse=True):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

            title_match = re.search(r'^title:\s*(.*)$', content, re.MULTILINE)
            date_match = re.search(r'^date:\s*(.*)$', content, re.MULTILINE)

            title = title_match.group(1).strip() if title_match else 'No Title'
            date = date_match.group(1).strip() if date_match else 'No Date'

            img_html = ""
            img_match = re.search(r"""!\[.*?\]\((.*?)\)""", content)
            if img_match:
                img_filename = img_match.group(1)
                img_html = f'<img src="posts/{img_filename}" style="max-width:100%; height:auto; border-radius:8px; margin-bottom:15px;">'

            body_match = re.search(r"""^---\n.*?^---\n\n(.*)""", content, re.DOTALL | re.MULTILINE)
            body = body_match.group(1).strip() if body_match else ""

            articles_html += f"""
        <article style='margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 20px;'>
            <h2>{title}</h2>
            <p style='color: #888; font-size: 0.9rem;'>公開日: {date}</p>
            {img_html}
            <div class='post-body'>{body}</div>
        </article>"""

    if not articles_html:
        articles_html = "<p style='text-align: center; color: #555;'>まだ記事がありません。</p>"

    updated_html = BLOG_INDEX_TEMPLATE.replace("<!-- POSTS_GO_HERE -->", articles_html)

    with open(blog_index_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print(f"{blog_index_path} を改行維持対応で更新しました。")

if __name__ == "__main__":
    build_blog_index('.')
