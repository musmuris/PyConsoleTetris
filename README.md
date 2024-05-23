## Tetris in Python with Curses

This is a simple console Tetris game written in Python using the curses library.

Wrote this as I wanted to learn to use ncurses and also a write tetris as a
precursor for another project

## Getting Started

### Prerequisites

* Python 3.x (written on 3.10/12 but should work on earlier)
* (on windows) windows-curses `pip install windows-curses`


### Running the game

Clone the repository and run the following command in your terminal:

```
python tetris.py
```

This will start the Tetris game. Use the left/right arrow keys to move the tetrominoes, 
down to drop them, and the up arrow to rotate them. Press 'q' to quit.

Currently you can only rotate one way - but adding a key to do the other is trivial

## Gameplay

The game follows the classic Tetris rules. Tetrominoes fall down the playfield. You can rotate and move them to form complete lines. When a line is complete, it disappears and grants you points. The game ends when the tetrominoes reach the top of the playfield.

## Controls

* Arrow keys: Left, right, down to move the tetromino. Up to rotate
* 'q': Quit the game.

## License

This project is licensed under the Zero clause BSD License. See the LICENSE file for details.
