import chess
import chess.engine
import chess.pgn

# Create an empty board
# board = chess.Board(None)

# Add the pieces
# board.set_piece_at(chess.G6, chess.Piece(chess.KING, chess.WHITE))
# board.set_piece_at(chess.G3, chess.Piece(chess.KING, chess.BLACK))
# board.set_piece_at(chess.E1, chess.Piece(chess.ROOK, chess.BLACK))

# White to move
# board.turn = chess.WHITE

# Location of the Stockfish program
stockfish_path = "stockfish/stockfish-windows-x86-64-universal.exe"

# Start Stockfish
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

# Define helper functions

# FUNCTION 1 — Convert PV to readable notation
def pv_to_san(board, pv):
    temp_board = board.copy()
    moves_san = []

    for move in pv:
        moves_san.append(temp_board.san(move))
        temp_board.push(move)

    return moves_san
# FUNCTION 2 — Format Stockfish evaluation
def format_score(score):
    mate = score.mate()

    if mate is not None:
        if mate > 0:
            return f"White has forced checkmate — mate in {mate}"
        else:
            return f"Checkmate unavoidable — Black mates in {abs(mate)}"

    centipawns = score.score()
    evaluation = centipawns / 100

    if evaluation > 0:
        return f"White advantage: +{evaluation:.2f}"
    elif evaluation < 0:
        return f"Black advantage: {evaluation:.2f}"
    else:
        return "Equal position: 0.00"
# FUNCTION 3 — Identify endgame
def is_endgame(board):
    piece_count = len(board.piece_map())

    if piece_count <= 7:
        return True
    else:
        return False
# FUNCTION 4 — get a FEN position
def get_position():
    fen = input("Enter FEN: ")
    board = chess.Board(fen)

    return board
#

# FUNCTION 5 — load a PNG game
def load_game(pgn_file):
    with open(pgn_file) as file:
        game = chess.pgn.read_game(file)

    return game
#FUNCTION 5 — Walk through the completed game
def replay_game(game):
    board = game.board()

    for move_number, move in enumerate(game.mainline_moves(), start=1):
        move_san = board.san(move)

        print("Move", move_number, ":", move_san)

        board.push(move)


# FUNCTION — Analyze position
def analyze_position(board, engine):
    if is_endgame(board):
        print("Position type: Endgame")

    info = engine.analyse(
        board,
        chess.engine.Limit(depth=15),
        multipv=3
    )

    info = engine.analyse(
        board,
        chess.engine.Limit(depth=15),
        multipv=3
    )
    for candidate in info:
        move = candidate["pv"][0]
        move_san = board.san(move)

        score = candidate["score"].pov(chess.WHITE)
        score_text = format_score(score)

        line = pv_to_san(board, candidate["pv"])

        print("Move:", move_san)
        print("Evaluation:", score_text)
        print("Line:", " ".join(line))
        print()
# Call function
print("Stockfish Analyzer")
print()
print("1 - Analyze a position")
print("2 - Load a completed game")
print()

choice = input("Choose an option: ")

if choice == "1":
    board = get_position()
    analyze_position(board, engine)

elif choice == "2":
    game = load_game("test_game.pgn")

    print("White:", game.headers["White"])
    print("Black:", game.headers["Black"])
    print("Result:", game.headers["Result"])
    print("Moves:", game.mainline())
    print()

    replay_game(game)

else:
    print("Invalid option")


# Close Stockfish
engine.quit()