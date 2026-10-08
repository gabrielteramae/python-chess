# Python Chess — xadrez no terminal

![python-chess](https://img.shields.io/badge/python--chess-1.11.2-3776AB?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.4.2-0A9EDC?logo=pytest&logoColor=white)

Dois jogadores no mesmo computador. A biblioteca `chess` valida o lance; o script desenha o tabuleiro com peças Unicode e cor ANSI, lê UCI ou SAN e anuncia xeque, xeque-mate e os empates que `python-chess` detecta. Não há engine.

## Stack

- `chess` 1.11.2 (`requirements.txt`)
- pytest 8.4.2
- ANSI no terminal; `cls` no Windows e `clear` nos outros
- o repositório não fixa a versão do Python

## Estrutura

```
.
├── xadrez.py              # tabuleiro, comandos e loop da partida
├── requirements.txt
└── tests/test_regras.py   # cinco casos de regra
```

Entrada aceita UCI (`e2e4`, `e7e8q`) e SAN (`e4`, `Cf3`, `O-O`, `O-O-O`). Comandos: `ajuda`, `lances`, `desfazer`, `tabuleiro`, `historico`, `sair` (também `exit` e `quit`). O rei em xeque é pintado à parte. Fim de jogo cobre mate, afogamento, material insuficiente, 75 lances, repetição quíntupla e empate reivindicável (50 lances ou tripla repetição). `Ctrl+C` ou EOF encerra com código 0.

## Como rodar

```bash
git clone https://github.com/gabrielteramae/python-chess.git
cd python-chess
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python xadrez.py
```

## Testes realizados

`tests/test_regras.py` cobre `interpretar_lance` e `resultado_final`:

- `e2e5` na posição inicial é recusado; `e2e4` é aceito
- mate do tolo em UCI (`f2f3`, `e7e5`, `g2g4`, `d8h4`) termina com “Xeque-mate! As Pretas vencem.”
- `O-O` no FEN `r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1` coloca o rei em g1 e a torre em f1
- en passant `e5d6` no FEN com peão branco em e5 e alvo d6 captura o peão de d5
- `e7e8q` promove o peão branco a dama

```bash
pytest -q
```

---

© 2026 Gabriel Teramae Chan
