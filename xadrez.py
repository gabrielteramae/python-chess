#!/usr/bin/env python3
"""
Jogo de Xadrez em Python - Terminal
Dois jogadores no mesmo computador (modo local), com validação completa
das regras oficiais do xadrez (roque, en passant, promoção, xeque-mate, etc.)

Requisitos:
    pip install chess

Como jogar:
    - Lances em notação UCI (ex: e2e4, g1f3) ou SAN (ex: e4, Cf3, O-O)
    - Digite 'ajuda' para ver os comandos disponíveis
"""

import chess
import os
import sys

# ---------- Cores ANSI ----------
class Cor:
    RESET = "\033[0m"
    NEGRITO = "\033[1m"
    BRANCO_PECA = "\033[97m"
    PRETO_PECA = "\033[30m"
    CASA_CLARA_BG = "\033[48;5;223m"
    CASA_ESCURA_BG = "\033[48;5;137m"
    DESTAQUE_BG = "\033[48;5;150m"
    CHECK_BG = "\033[48;5;203m"
    TEXTO_INFO = "\033[96m"
    TEXTO_ERRO = "\033[91m"
    TEXTO_OK = "\033[92m"


PECAS_UNICODE = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}

NOME_PECA_PT = {
    chess.PAWN: "Peão", chess.KNIGHT: "Cavalo", chess.BISHOP: "Bispo",
    chess.ROOK: "Torre", chess.QUEEN: "Dama", chess.KING: "Rei",
}


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def desenhar_tabuleiro(board: chess.Board, destaques=None):
    destaques = destaques or set()
    linhas = []
    linhas.append("")
    linhas.append("     a  b  c  d  e  f  g  h")
    for rank in range(7, -1, -1):
        linha = f"  {rank + 1}  "
        for file in range(8):
            sq = chess.square(file, rank)
            piece = board.piece_at(sq)
            casa_clara = (file + rank) % 2 == 1

            if board.is_check() and piece and piece.piece_type == chess.KING and piece.color == board.turn:
                bg = Cor.CHECK_BG
            elif sq in destaques:
                bg = Cor.DESTAQUE_BG
            elif casa_clara:
                bg = Cor.CASA_CLARA_BG
            else:
                bg = Cor.CASA_ESCURA_BG

            if piece:
                simbolo = PECAS_UNICODE[piece.symbol()]
                cor_peca = Cor.BRANCO_PECA if piece.color == chess.WHITE else Cor.PRETO_PECA
                fundo_peca = f"{bg}{cor_peca}{Cor.NEGRITO}"
                celula = f"{fundo_peca} {simbolo} {Cor.RESET}"
            else:
                celula = f"{bg}   {Cor.RESET}"
            linha += celula
        linha += f"  {rank + 1}"
        linhas.append(linha)
    linhas.append("     a  b  c  d  e  f  g  h")
    linhas.append("")
    print("\n".join(linhas))


def nome_da_peca(piece_type):
    return NOME_PECA_PT.get(piece_type, "")


def mostrar_ajuda():
    print(f"""
{Cor.TEXTO_INFO}Como jogar:{Cor.RESET}
  - Digite o lance em notação UCI: ex. e2e4, g8f6, e1g1 (roque)
  - Ou em notação SAN: ex. e4, Cf3, Dxd5, O-O, O-O-O
  - Para promover um peão em UCI, adicione a letra da peça: e7e8q (dama), e7e8n (cavalo)

Comandos especiais:
  ajuda        - mostra esta mensagem
  lances       - lista os lances legais na posição atual
  desfazer     - desfaz o último lance
  tabuleiro    - redesenha o tabuleiro
  historico    - mostra o histórico de lances
  sair         - encerra o jogo
""")


def historico_para_texto(board: chess.Board):
    temp = chess.Board()
    partes = []
    for i, mv in enumerate(board.move_stack):
        san = temp.san(mv)
        temp.push(mv)
        if i % 2 == 0:
            partes.append(f"{i // 2 + 1}. {san}")
        else:
            partes[-1] += f"  {san}"
    return "  ".join(partes) if partes else "(nenhum lance ainda)"


def interpretar_lance(board: chess.Board, entrada: str):
    """Tenta interpretar a entrada como UCI ou SAN. Retorna chess.Move ou None."""
    entrada = entrada.strip()
    # Tenta UCI primeiro
    try:
        mv = chess.Move.from_uci(entrada.lower())
        if mv in board.legal_moves:
            return mv
    except ValueError:
        pass
    # Tenta SAN
    try:
        mv = board.parse_san(entrada)
        return mv
    except ValueError:
        return None


def resultado_final(board: chess.Board):
    if board.is_checkmate():
        vencedor = "Pretas" if board.turn == chess.WHITE else "Brancas"
        return f"Xeque-mate! As {vencedor} vencem."
    if board.is_stalemate():
        return "Empate por afogamento (stalemate)."
    if board.is_insufficient_material():
        return "Empate por material insuficiente."
    if board.is_seventyfive_moves():
        return "Empate pela regra dos 75 lances."
    if board.is_fivefold_repetition():
        return "Empate por repetição de posição (5x)."
    if board.can_claim_draw():
        return "Empate pode ser reivindicado (50 lances / 3x repetição)."
    return None


def jogar():
    board = chess.Board()
    limpar_tela()
    print(f"{Cor.NEGRITO}{Cor.TEXTO_INFO}=== JOGO DE XADREZ ==={Cor.RESET}")
    print("Digite 'ajuda' a qualquer momento para ver os comandos.\n")

    while not board.is_game_over(claim_draw=True):
        desenhar_tabuleiro(board)

        vez = "Brancas" if board.turn == chess.WHITE else "Pretas"
        if board.is_check():
            print(f"{Cor.TEXTO_ERRO}Xeque!{Cor.RESET}")
        print(f"{Cor.NEGRITO}Vez das {vez}.{Cor.RESET}")

        entrada = input(f"Lance ({vez}) > ").strip()

        if entrada == "":
            continue
        cmd = entrada.lower()

        if cmd in ("sair", "exit", "quit"):
            print("Jogo encerrado.")
            return
        elif cmd == "ajuda":
            mostrar_ajuda()
            continue
        elif cmd == "tabuleiro":
            limpar_tela()
            continue
        elif cmd == "historico":
            print(f"\n{Cor.TEXTO_INFO}{historico_para_texto(board)}{Cor.RESET}\n")
            continue
        elif cmd == "desfazer":
            if board.move_stack:
                mv = board.pop()
                print(f"{Cor.TEXTO_OK}Lance desfeito: {mv.uci()}{Cor.RESET}")
            else:
                print(f"{Cor.TEXTO_ERRO}Não há lances para desfazer.{Cor.RESET}")
            limpar_tela()
            continue
        elif cmd == "lances":
            legais = sorted(board.san(m) for m in board.legal_moves)
            print(f"\n{Cor.TEXTO_INFO}Lances legais: {', '.join(legais)}{Cor.RESET}\n")
            continue

        mv = interpretar_lance(board, entrada)
        if mv is None:
            print(f"{Cor.TEXTO_ERRO}Lance inválido: '{entrada}'. Digite 'ajuda' ou 'lances' para ver as opções.{Cor.RESET}")
            continue

        san = board.san(mv)
        peca_movida = board.piece_at(mv.from_square)
        captura = board.is_capture(mv)
        board.push(mv)
        limpar_tela()

        desc = f"{nome_da_peca(peca_movida.piece_type)} joga {san}"
        if captura:
            desc += " (captura!)"
        print(f"{Cor.TEXTO_OK}{desc}{Cor.RESET}")

    # Fim de jogo
    desenhar_tabuleiro(board)
    print(f"\n{Cor.NEGRITO}{Cor.TEXTO_INFO}=== FIM DE JOGO ==={Cor.RESET}")
    print(resultado_final(board))
    print(f"\nHistórico completo: {historico_para_texto(board)}\n")


if __name__ == "__main__":
    try:
        jogar()
    except (KeyboardInterrupt, EOFError):
        print("\nJogo interrompido.")
        sys.exit(0)
