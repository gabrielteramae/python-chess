# ♟️ Python Chess — Jogo de Xadrez em Terminal

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)
![python-chess](https://img.shields.io/badge/python--chess-1.11.2-blue?style=flat)
![Status](https://img.shields.io/badge/status-concluído-brightgreen?style=flat)

Jogo de xadrez para dois jogadores, jogado diretamente no terminal, com validação completa das regras oficiais (roque, en passant, promoção, xeque-mate) usando a biblioteca [`python-chess`](https://python-chess.readthedocs.io/) e um tabuleiro renderizado com cores ANSI.

## 🎮 Demonstração

```
     a  b  c  d  e  f  g  h
  8  ♜  ♞  ♝  ♛  ♚  ♝  ♞  ♜   8
  7  ♟  ♟  ♟  ♟  ♟  ♟  ♟  ♟   7
  6                          6
  5                          5
  4              ♙           4
  3                          3
  2  ♙  ♙  ♙  ♙     ♙  ♙  ♙   2
  1  ♖  ♘  ♗  ♕  ♔  ♗  ♘  ♖   1
     a  b  c  d  e  f  g  h

Vez das Pretas.
Lance (Pretas) >
```

## ✨ Funcionalidades

- Tabuleiro colorido com peças em Unicode
- Lances em notação **UCI** (`e2e4`) ou **SAN** (`e4`, `Cf3`, `O-O`)
- Regras completas: roque, en passant, promoção de peão
- Detecção de xeque, xeque-mate, afogamento e empates
- Comandos auxiliares: `ajuda`, `lances`, `historico`, `desfazer`, `tabuleiro`, `sair`

## 🚀 Como rodar

```bash
git clone https://github.com/gabrielteramae/python-chess.git
cd python-chess
pip install chess
python3 xadrez.py
```

## 🕹️ Como jogar

| Comando | Ação |
|---|---|
| `e2e4` | Move o peão de e2 para e4 (notação UCI) |
| `Cf3` | Move o cavalo para f3 (notação SAN) |
| `O-O` / `O-O-O` | Roque curto / roque longo |
| `lances` | Lista todos os lances legais na posição atual |
| `historico` | Mostra o histórico da partida |
| `desfazer` | Desfaz o último lance |
| `ajuda` | Mostra a lista de comandos |
| `sair` | Encerra o jogo |

## 🛠️ Tecnologias

- **Python 3**
- **[python-chess](https://pypi.org/project/chess/)** — validação de regras e geração de lances legais
- Códigos ANSI para renderização colorida do tabuleiro no terminal

---

© 2026 Gabriel Teramae Chan
