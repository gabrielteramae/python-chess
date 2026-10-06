import chess

from xadrez import interpretar_lance, resultado_final


def jogar(lances, fen=None):
    board = chess.Board(fen) if fen else chess.Board()
    for lance in lances:
        mv = interpretar_lance(board, lance)
        assert mv is not None, lance
        board.push(mv)
    return board


def test_recusa_lance_ilegal():
    board = chess.Board()
    assert interpretar_lance(board, "e2e5") is None
    assert interpretar_lance(board, "e2e4") is not None


def test_mate_do_tolo_em_uci():
    board = jogar(["f2f3", "e7e5", "g2g4", "d8h4"])
    assert board.is_checkmate()
    assert resultado_final(board) == "Xeque-mate! As Pretas vencem."


def test_roque_curto():
    fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
    board = jogar(["O-O"], fen)
    assert board.piece_at(chess.G1).piece_type == chess.KING
    assert board.piece_at(chess.F1).piece_type == chess.ROOK


def test_en_passant():
    fen = "rnbqkbnr/ppp1pppp/8/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"
    board = jogar(["e5d6"], fen)
    assert board.piece_at(chess.D6).piece_type == chess.PAWN
    assert board.piece_at(chess.D5) is None


def test_promocao_a_dama():
    fen = "8/4P3/8/8/8/8/8/4K2k w - - 0 1"
    board = jogar(["e7e8q"], fen)
    peca = board.piece_at(chess.E8)
    assert peca.piece_type == chess.QUEEN
    assert peca.color == chess.WHITE
