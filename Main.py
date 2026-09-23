import chess
import chess.engine
import os
import sys

APP_NAME = "Stockfish Chess Practice"
APP_VERSION = "1.0.0"

# FUNCTION — Get Stockfish location
def get_stockfish_path():
    if getattr(sys, "frozen", False):
        # Running as a packaged executable
        base_path = sys._MEIPASS
    else:
        # Running normally from Python/PyCharm
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(
        base_path,
        "stockfish",
        "stockfish-windows-x86-64-universal.exe"
    )


stockfish_path = get_stockfish_path()

# FUNCTION — Format Stockfish evaluation
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
# FUNCTION — Identify endgame
def is_endgame(board):
    return len(board.piece_map()) <= 7
# FUNCTION — get a FEN position
def get_position():
    while True:
        fen = input("Enter FEN: ")

        try:
            return chess.Board(fen)
        except ValueError:
            print("Invalid FEN. Try again.")


# FUNCTION — Explain the quality of a candidate move
def assess_move(candidate_move, best_move, before_score, after_score, evaluation_loss):

    if candidate_move == best_move:
        return "Best move"

    # The position was already a forced mate
    if before_score.is_mate():
        before_mate = before_score.mate()

        if before_mate < 0:
            if after_score.is_mate() and after_score.mate() < 0:
                return "Already losing — this move remains in a forced-mate position."
            else:
                return "Improvement — this move escapes the forced mate."

        if before_mate > 0:
            if not after_score.is_mate():
                return "Major mistake — this move loses a forced win."

    # Candidate move creates a forced mate against us
    if after_score.is_mate() and after_score.mate() < 0:
        return "Major mistake — this move allows forced checkmate."

    # Normal numerical evaluations
    if evaluation_loss < 0.20:
        return "Excellent — nearly as strong as the best move."
    elif evaluation_loss < 0.50:
        return "Good — a small difference from the best move."
    elif evaluation_loss < 1.00:
        return "Inaccuracy — gives up some advantage."
    elif evaluation_loss < 2.00:
        return "Mistake — significantly worsens the position."
    else:
        return "Blunder — seriously worsens the position."

# FUNCTION — Analyze position
def analyze_position(board, engine):
    if is_endgame(board):
        print("Position type: Endgame")

    info = engine.analyse(
        board,
        chess.engine.Limit(depth=15)
    )

    move = info["pv"][0]
    move_san = board.san(move)

    score = info["score"].pov(chess.WHITE)
    score_text = format_score(score)

    print()
    print("Best move:", move_san)
    print("Evaluation:", score_text)

# FUNCTION — Convert evaluation to a number
def score_to_number(score):
    # Treat forced mate as a very large advantage/disadvantage
    if score.is_mate():
        mate = score.mate()

        if mate > 0:
            return 100.0
        else:
            return -100.0

    return score.score() / 100

# FUNCTION — Test a move
def test_my_move(board, engine):

    # Remember whose move it is
    player = board.turn

    # Analyze the original position once
    best_info = engine.analyse(
        board,
        chess.engine.Limit(depth=15)
    )

    best_move = best_info["pv"][0]
    best_move_san = board.san(best_move)
    before_score = best_info["score"].pov(player)

    while True:
        print()

        # Keep asking until a legal move is entered
        while True:
            candidate_san = input("Move you are considering: ")

            try:
                candidate_move = board.parse_san(candidate_san)
                break
            except ValueError:
                print("Invalid or illegal move. Try again.")

        # Play candidate move on a COPY of the original position
        test_board = board.copy()
        test_board.push(candidate_move)

        candidate_info = engine.analyse(
            test_board,
            chess.engine.Limit(depth=15)
        )

        after_score = candidate_info["score"].pov(player)

        before_value = score_to_number(before_score)
        after_value = score_to_number(after_score)

        evaluation_loss = before_value - after_value

        print()
        print("Your move:", candidate_san)
        print("Stockfish best move:", best_move_san)
        print()

        assessment = assess_move(
            candidate_move,
            best_move,
            before_score,
            after_score,
            evaluation_loss
        )

        # If the user found Stockfish's best move
        if candidate_move == best_move:
            print(
                "Position after move:",
                format_score(candidate_info["score"].pov(chess.WHITE))
            )
            print()
            print("Assessment:", assessment)

        # If the user chose a different move
        else:
            print(
                "Best possible evaluation:",
                format_score(best_info["score"].pov(chess.WHITE))
            )
            print(
                "After your move:",
                format_score(candidate_info["score"].pov(chess.WHITE))
            )
            print()
            print("Assessment:", assessment)

            if not before_score.is_mate() and not after_score.is_mate():
                print(f"Evaluation lost: {max(0, evaluation_loss):.2f}")
        print()
        again = input("Test another move from this position? (y/n): ")
        if again.lower() != "y":
            break

# Call function
def main():
    try:
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    except (FileNotFoundError, OSError):
        print("Error: Stockfish could not be started.")
        print("Expected location:", stockfish_path)
        input("Press Enter to exit.")
        return

    try:
        while True:
            print()
            print(f"{APP_NAME} v{APP_VERSION}")
            print("For offline study and practice only")
            print()
            print("1 - Analyze a position")
            print("2 - Test my move")
            print("3 - Exit")
            print()

            choice = input("Choose an option: ")

            if choice == "1":
                board = get_position()
                analyze_position(board, engine)

            elif choice == "2":
                board = get_position()
                test_my_move(board, engine)

            elif choice == "3":
                print("Closing Stockfish Chess Practice.")
                break

            else:
                print("Invalid option. Try again.")

    finally:
        engine.quit()

if __name__ == "__main__":
            main()