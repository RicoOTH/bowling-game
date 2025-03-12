# A Bowling Game

Write a program to calculate the score during an american ten pin bowling game.

We can briefly summarize the scoring for this form of bowling:

- Each game, or “line” of bowling, includes ten turns, or “frames” for the bowler.

- In each frame, the bowler gets up to two tries to knock down all the pins.

- If in two tries, he fails to knock them all down, his score for that frame is the total number of pins knocked down in his two tries.

- If in two tries he knocks them all down, this is called a “spare” ("/" within score table) and his score for the frame is ten plus the number of pins knocked down on his next throw (in his next turn).

- If on his first try in the frame he knocks down all the pins, this is called a “strike” ("X" within score table). His turn is over, and his score for the frame is ten plus the simple total of the pins knocked down in his next two rolls.

- If he gets a spare or strike in the last (tenth) frame, the bowler gets to throw one or two more bonus balls, respectively. These bonus throws are taken as part of the same turn. If the bonus throws knock
down all the pins, the process does not repeat: the bonus throws are only used to calculate the score of
the final frame.

- The game score is the total of all frame scores.

## How to play

The game can be played on the command line with `python3 game.py` and simply adding the number of knocked down pins for each roll. It (should :) ) automatically end the game if the player is not allowed to take another roll/turn. It also computes the current score after every roll and prints out the final score at the end. It also keeps track of the score via a small scoreboard visualisation (which is not yet pixel-perfect).

Valid inputs for the game are the number of pins the bowler has hit in each roll. Since this is a game of American Ten-pin bowling, this number lies between 0 and 10. Additionally, the user can input the following characters:

- `/` to signify a spare has occured
- `x` (or `X`) to signify that a strike has occcurred

## Open Questions

- Is it considered a spare or a strike, if the bowler hits 10 poins in the second roll of a frame? [Google](/https://out-of-bounds.co.uk/how-points-are-calculated-in-bowling/) said a strike is only possible on the first attempt. Therefore I accounted for it as a normal spare here.

## Implemented Test Cases

I used standard unittests to verify the differing functionality of the game. The following will give an overview over the different test cases that are implemented.

### Invalid inputs

- Invalid number of pins (more than 10 pins for one roll; more than 10 pins for one frame).
- Invalid number of turns (more than 21 rolls are impossible).
- User enters a spare on the first roll of frame, which should not be possible.
- User enters an invalid string.

## Score calculation

- A test to ensure that the character inputs for spares and strikes work as intended.
- Testing a gutter game where the bowler scores 0 points for every frame.
- Testing a game where the bowler hits 1 pin in every round for every frame.
- Testing frames with only one spare. Computes a temporary result after roll #3.
- Testing a game with only one strike.
- Testing a "normal" game that uses the suggested score from the pdf task.
- Testing a game with only strikes, making sure the final frame is added correctly.
- Testing a game with only spares (and one strike), making sure the final frame is added correctly.

## Notes

- I thought about adding visuals that would let you enter the score roll by roll but deemed it too big of a timesink. While I am a big fan of doing that for these types of projects, I would end up spending a lot of time gathering gifs for cool visual effects upon strikes/spares, and probably even individual scoring for each frame, instead of focusing on keeping the main functionality concise.

- The notes.txt contains some basic outlines and rules I tried to brainstorm before starting with the actual coding.
- As I am a big fan of utilising Docstring, I did so. It should help clarify what each function does and what errors may occur.
