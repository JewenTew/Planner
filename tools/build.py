"""Build index.html (the app served by GitHub Pages) from src/planner.html.

src/planner.html is the page body without the <html>/<head> wrapper, so the same
file can also be published as a Claude artifact. This script adds the wrapper:
the web app manifest, icons, the Firebase settings and the offline service worker.

Usage (from the repository root):
    python tools/build.py
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src', 'planner.html')
OUT = os.path.join(ROOT, 'index.html')

HEAD = '''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f5aecb">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Planner">
<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>
<script src="firebase-config.js"></script>
<script>
if ('serviceWorker' in navigator) addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
</script>
</head>
<body>
'''

body = io.open(SRC, encoding='utf-8').read()
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(HEAD + body + '\n</body>\n</html>\n')
print('built', os.path.relpath(OUT, ROOT))
