"""Monta as roletas: embute a fonte e o logo em base64, pra rodar sem internet.

Uma fonte só (src/roleta.html), três temas:
  index.html        Nouê da Sorte (visual claro do site), lives do Melano e do Touch
  1010/index.html   10.10 · data dupla da Nouê (azul-marinho, dourado e branco), live do sábado 10/10
  live/index.html   live de sábado 17/10/2026 (pedido do Luan: "duplicar aquela e adaptar com as condições do anexo",
                    depois "segue essa id aqui" = a roleta da /pages/live): visual café, ouro e cobre com lâmpadas no
                    aro, "LIVE" no miolo, faixa animada no topo e as FAIXAS por valor de pedido (R$ 350+ = 1 prêmio,
                    R$ 500+ = 3, R$ 1.000+ = 10) na tela, com contador do pedido da vez
Cada tema guarda o histórico de giros separado no navegador (PREFIXO), pra live de um dia não misturar com a do outro.

Uso: python build.py   (edite src/roleta.html, nunca os index.html direto)
"""
import base64
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).parent
# MIOLO = o que vai no centro da roda; FITA = faixa animada do topo (só no tema live)
SEM_FAIXAS = {'FAIXAS': '[]', 'AJUDA_FAIXAS': '', 'MIOLO': '<div class="logo"></div>', 'FITA': ''}
_FITA_TXT = ' · '.join(['ROLETA DE PRÊMIOS DA LIVE', 'R$ 350+ = 1 PRÊMIO', 'R$ 500+ = 3 PRÊMIOS', 'R$ 1.000+ = 10 PRÊMIOS'] * 4) + ' · '
FITA_LIVE = ('<div id="fita" aria-hidden="true">'
             f'<div class="banda atras"><span class="trilho">{_FITA_TXT}{_FITA_TXT}</span></div>'
             f'<div class="banda frente"><span class="trilho">{_FITA_TXT}{_FITA_TXT}</span></div></div>')
FAIXAS_LIVE = [{'rotulo': 'R$ 350+', 'premios': 1}, {'rotulo': 'R$ 500+', 'premios': 3}, {'rotulo': 'R$ 1.000+', 'premios': 10}]
AJUDA_FAIXAS = ('<li><kbd>1</kbd><kbd>2</kbd><kbd>3</kbd>faixa do pedido da vez (R$ 350+, R$ 500+, R$ 1.000+): digite nome e '
                'pedido, a tela conta "prêmio 1 de 3" e a planilha já sai preenchida. <kbd>Esc</kbd> cancela a faixa</li>')
TEMAS = {
    'padrao': {'saida': 'index.html', 'TEMA': 'padrao', 'COR_TEMA': '#FAF7F2', 'TITULO_PAGINA': 'Nouê da Sorte',
               'TITULO': 'da sorte', 'SUBTITULO': '', 'PREFIXO': 'noue-da-sorte:', 'ARQUIVO': 'noue-da-sorte', **SEM_FAIXAS},
    '1010': {'saida': '1010/index.html', 'TEMA': '1010', 'COR_TEMA': '#081634', 'TITULO_PAGINA': 'Nouê 10.10',
             'TITULO': '10.10', 'SUBTITULO': '<div id="subtitulo">data dupla da Nouê</div>', 'PREFIXO': 'noue-1010:',
             'ARQUIVO': 'noue-1010', **SEM_FAIXAS},
    # 16/10 tarde: o Luan pediu a identidade da roleta da /pages/live ("segue essa id aqui") no lugar do azul do 10.10
    'live': {'saida': 'live/index.html', 'TEMA': 'live', 'COR_TEMA': '#22150F', 'TITULO_PAGINA': 'Nouê da Sorte · Live',
             'TITULO': 'da sorte', 'SUBTITULO': '<div id="subtitulo">roleta de prêmios da live</div>',
             'PREFIXO': 'noue-live-1710:', 'ARQUIVO': 'noue-live-1710',
             'FAIXAS': json.dumps(FAIXAS_LIVE, ensure_ascii=False), 'AJUDA_FAIXAS': AJUDA_FAIXAS,
             'MIOLO': '<div class="miolo-texto">LIVE</div>', 'FITA': FITA_LIVE},
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
