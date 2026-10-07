# Nouê da Sorte: roleta de palco das lives

Roleta pra projetar na TV nas lives de lançamento (Melano-Reativ 3% e Camuflage Touch, 08 e 09/10/2026).
**Página separada** da roleta de captação do site: outro endereço, sem banco, sem cupom ROLETA10.

## Na noite da live

1. Abra o `index.html` no Chrome do notebook ligado na TV (duplo clique no arquivo; funciona **sem internet**).
2. Clique uma vez: entra em tela cheia.
3. **Segure a roleta, arraste e solte** (mouse ou dedo): quanto mais força, mais rápido e por mais tempo ela gira.
   Puxão fraco não vale (aparece "Gire com mais força"). De reserva, um clique (ou Espaço, Enter, setas,
   passador de slide) **gira sozinha**. Clique de novo depois do resultado: **limpa**.

Durante o giro e nos 3 primeiros segundos do resultado o clique não faz nada (protege do clique duplo).
A tela se ajusta sozinha: deitada fica roda e nome lado a lado; em pé (celular), nome em cima e roda embaixo.

| Tecla | O que faz |
|---|---|
| M | liga e desliga o som (o botão do canto faz o mesmo) |
| F | tela cheia |
| G | moldura de teste da TV (overscan) |
| + e - | aumenta e diminui a roleta (0 volta ao normal) |
| H | histórico dos giros: anotar ganhador e baixar a planilha |
| ? | ajuda |

## Teste na TV (dia anterior)

Aperte **G**: a moldura verde tem que aparecer inteira. Se a TV cortar, aperte **-** até aparecer
(o tamanho fica salvo no navegador). Gire umas vezes olhando de onde a plateia vai estar.

## Como funciona o sorteio

O prêmio é sorteado **no clique ou na hora que a mão solta** (gerador criptográfico do navegador) e a animação só
leva a roda até ele, parando no miolo da fatia, nunca na divisa. No giro na mão, a força decide a velocidade e o
tempo (e a roda sai na mesma velocidade da mão), mas não o prêmio: assim ninguém consegue mirar uma fatia.

**A chance é o tamanho da fatia, à vista de todo mundo.** Cada prêmio tem um `peso` no CONFIG (sem peso = 1). Os
descontos estão com 0.5 (decisão do Luan, 07/10: brinde no pedido é mais fácil que desconto): fatia com metade do
tamanho, 3,85% de chance cada, os 2 juntos 7,7% (1 a cada 13 giros); cada produto fica com 7,7%. Simulação com 200
mil giros nos 2 sentidos: 0 erro, descontos saíram 3,85% e 3,87%, produtos entre 7,57% e 7,84%.

## Registro dos giros

Cada giro fica gravado **no navegador daquele notebook** (número do dia, data, hora, prêmio). Na tecla **H**
dá pra escrever o ganhador ao lado e baixar a planilha (CSV, abre no Excel). Apagar o histórico baixa a planilha antes.

## Trocar prêmio, cupom ou texto

Edite o bloco `CONFIG` no começo do `src/roleta.html` e rode `python build.py` (gera o `index.html` com a fonte
e o logo embutidos). Nunca edite o `index.html` direto.
