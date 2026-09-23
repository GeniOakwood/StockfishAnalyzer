# Stockfish Chess Practice

A Python chess practice tool powered by the Stockfish chess engine.

The project is designed for offline chess study and practice. Rather than
only showing the engine's best move, it allows a player to test a move they
are considering and see how that decision changes the evaluation of the
position.

## Features

### Analyze a Position

Enter a position in FEN format to see:

- Stockfish's best move
- The current position evaluation
- Forced checkmate when detected

### Test My Move

Enter a FEN position and a move you are considering.

The program compares your candidate move with Stockfish's preferred move
and reports:

- Your move
- Stockfish's best move
- Best possible evaluation
- Evaluation after your candidate move
- Evaluation lost compared with best play
- A human-readable assessment such as:
  - Best
  - Good
  - Inaccuracy
  - Mistake
  - Blunder
  - Allows forced checkmate

Multiple candidate moves can be tested against the same position without
re-entering the FEN.

## Example

Position:

    r1bqk2r/ppp2ppp/2nb4/4p3/4n3/5NP1/PPP2PBP/RNBQ1RK1 w kq - 0 8

Candidate move:

    Nc3

Example output:

    Your move: Nc3
    Stockfish best move: Nxe5

    Best possible evaluation: Black advantage: -0.28
    After your move: Black advantage: -1.71

    Assessment: Mistake — significantly worsens the position.
    Evaluation lost: 1.43

## Technologies

- Python
- python-chess
- Stockfish 19
- Universal Chess Interface (UCI)
- PyInstaller

## Running from Source

### Requirements

- Python 3
- python-chess
- Stockfish 19

Install python-chess:

    pip install python-chess

Place the Stockfish executable in the project's `stockfish` directory.

Then run:

    python Main.py

## Windows Executable

The project can also be packaged as a standalone Windows executable using
PyInstaller.

The packaged application is intended to run without requiring the user to
install Python separately.

## Project Structure

    StockfishAnalyzer/
    ├── Main.py
    ├── README.md
    ├── THIRD_PARTY_LICENSES.md
    └── stockfish/
        └── stockfish-windows-x86-64-universal.exe

Build and development directories are excluded from the source repository.

## Purpose

This project was created as a learning and portfolio project combining
Python programming, chess analysis, external engine integration, input
validation, evaluation logic, and application packaging.

It is intended exclusively for offline chess study and practice, not for
assistance during live games.

## Stockfish

This project uses Stockfish 19 as its chess analysis engine.

Stockfish is free software licensed under the GNU General Public License
version 3 (GPL-3.0). Stockfish is developed independently by the Stockfish
developers.

See `THIRD_PARTY_LICENSES.md` for licensing and source-code information.