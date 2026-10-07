"""Monta o index.html da roleta: embute a fonte e o logo em base64, pra rodar sem internet.

Uso: python build.py   (edite src/roleta.html, nunca o index.html direto)
"""
import base64
import pathlib
import re

RAIZ = pathlib.Path(__file__).parent


def b64(nome):
    return base64.b64encode((RAIZ / 'src' / 'assets' / nome).read_bytes()).decode()


html = (RAIZ / 'src' / 'roleta.html').read_text(encoding='utf-8')
html = html.replace('{{FONTE}}', b64('satoshi-variable.woff2')).replace('{{LOGO}}', b64('logo-noue.png'))
assert '{{' not in html, 'sobrou marcador sem trocar'
externos = [u for u in re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', html)]
externos += re.findall(r'url\((?!data:|#|var\()\s*["\']?(https?://[^)"\']+)', html)
assert not externos, f'chamada externa quebra o modo sem internet: {externos}'
(RAIZ / 'index.html').write_text(html, encoding='utf-8', newline='\n')
print(f'index.html: {len(html.encode()) // 1024} KB, 0 chamadas externas')
