# Stockfish Chess Practice

A Python chess practice tool powered by the Stockfish engine.

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

- Stockfish's best move
- The evaluation after your candidate move
- Evaluation lost compared with best play
- A human-readable assessment such as:
  - Best move
  - Excellent
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

## Requirements

- Python
- python-chess
- Stockfish chess engine

## Purpose

This project was created as a learning project combining Python programming,
chess analysis, and engine integration.

It is intended for offline study and practice, not for assistance during
live games.
