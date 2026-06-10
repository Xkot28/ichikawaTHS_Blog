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
    # Ensure the root directory for the blog exists if it's not '.'
    if blog_root_dir != '.':
        os.makedirs(blog_root_dir, exist_ok=True)

    posts_dir = os.path.join(blog_root_dir, 'posts')
    blog_index_path = os.path.join(blog_root_dir, 'index.html')

    # Ensure posts directory exists
    os.makedirs(posts_dir, exist_ok=True)

    md_files = glob.glob(os.path.join(posts_dir, '*.md'))

    articles_html = ""
    # Sort by date in filename, descending, for newest posts first
    for md_file in sorted(md_files, key=lambda x: os.path.basename(x), reverse=True):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

            # Extract metadata using regex for robustness
            title_match = re.search(r'^title:\s*(.*)$', content, re.MULTILINE)
            date_match = re.search(r'^date:\s*(.*)$', content, re.MULTILINE)

            title = title_match.group(1).strip() if title_match else 'No Title'
            date = date_match.group(1).strip() if date_match else 'No Date'

            # Extract image tag and prepare img_html
            img_html = ""
            # Use r"""...""" for regex pattern to avoid conflict with outer '"""'
            img_match = re.search(r"""!\[.*?\]\((.*?)\)""", content)
            if img_match:
                img_filename = img_match.group(1) # This is just the filename, e.g., "screenshot.png"
                img_html = f'<img src="posts/{img_filename}" style="max-width:100%; height:auto; border-radius:8px; margin-bottom:15px;">'

            # Extract body content after the second '---'
            # Use r"""...""" for regex pattern to avoid conflict with outer '"""'
            body_match = re.search(r"""^---
.*?^---

(.*)""", content, re.DOTALL | re.MULTILINE)
            body = body_match.group(1).strip() if body_match else ""

            body_excerpt = body[:150] + "..." if len(body) > 150 else body

            articles_html += f"""
        <article style='margin-bottom: 40px; border-bottom: 1px solid #eee; padding-bottom: 20px;'>
            <h2>{title}</h2>
            <p style='color: #888; font-size: 0.9rem;'>公開日: {date}</p>
            {img_html}
            <p>{body_excerpt}</p>
        </article>"""

    # If no articles, display a message
    if not articles_html:
        articles_html = "<p style='text-align: center; color: #555;'>まだ記事がありません。</p>"

    # Replace the placeholder in the template
    updated_html = BLOG_INDEX_TEMPLATE.replace(
        "<!-- POSTS_GO_HERE -->",
        articles_html
    )

    with open(blog_index_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    print(f"{blog_index_path} を最新の記事一覧で更新しました。")

if __name__ == "__main__":
    # In GitHub Actions, the current directory will be the repo root (e.g., ichikawaTHS_Blog).
    # So, the script should build the index in the current directory.
    build_blog_index('.')
