"""Monta as roletas: embute a fonte e o logo em base64, pra rodar sem internet.

Uma fonte só (src/roleta.html), dois temas:
  index.html        Nouê da Sorte (visual claro do site), lives do Melano e do Touch
  1010/index.html   10.10 · data dupla da Nouê (azul-marinho, dourado e branco), live do sábado 10/10
Cada tema guarda o histórico de giros separado no navegador (PREFIXO), pra live de um dia não misturar com a do outro.

Uso: python build.py   (edite src/roleta.html, nunca os index.html direto)
"""
import base64
import pathlib
import re

RAIZ = pathlib.Path(__file__).parent
TEMAS = {
    'padrao': {'saida': 'index.html', 'TEMA': 'padrao', 'COR_TEMA': '#FAF7F2', 'TITULO_PAGINA': 'Nouê da Sorte',
               'TITULO': 'da sorte', 'SUBTITULO': '', 'PREFIXO': 'noue-da-sorte:', 'ARQUIVO': 'noue-da-sorte'},
    '1010': {'saida': '1010/index.html', 'TEMA': '1010', 'COR_TEMA': '#081634', 'TITULO_PAGINA': 'Nouê 10.10',
             'TITULO': '10.10', 'SUBTITULO': '<div id="subtitulo">data dupla da Nouê</div>', 'PREFIXO': 'noue-1010:',
             'ARQUIVO': 'noue-1010'},
}


def b64(nome):
    return base64.b64encode((RAIZ / 'src' / 'assets' / nome).read_bytes()).decode()


fonte = (RAIZ / 'src' / 'roleta.html').read_text(encoding='utf-8')
fonte = fonte.replace('{{FONTE}}', b64('satoshi-variable.woff2')).replace('{{LOGO}}', b64('logo-noue.png'))
for nome, tema in TEMAS.items():
    html = fonte
    for chave, valor in tema.items():
        if chave != 'saida':
            html = html.replace('{{%s}}' % chave, valor)
    assert '{{' not in html, f'{nome}: sobrou marcador sem trocar'
    externos = [u for u in re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', html)]
    externos += re.findall(r'url\((?!data:|#|var\()\s*["\']?(https?://[^)"\']+)', html)
    assert not externos, f'{nome}: chamada externa quebra o modo sem internet: {externos}'
    saida = RAIZ / tema['saida']
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.write_text(html, encoding='utf-8', newline='\n')
    print(f'{tema["saida"]}: {len(html.encode()) // 1024} KB, 0 chamadas externas')
