class BowlingGame:
    """Represents a game of American ten-pin bowling.
    
    Attributes:
        strike (int): The number of knocked down pins needed for a strike (10).
        frames (int): The number of frames / turns per game (10).
        rolls (list): A list storing the knocked down pins of each roll.
        frame (int): Tracks the current frame / turn of the game.
        roll_in_frame (int): Tracks the current roll count within the frame.

    Note: An invalid number of pins hit in a roll, number of rolls, or number of pins hit in a frame will raise `ValueError`.
    """
    strike = 10
    frames = 10
    
    def __init__(self):
        """Simple init for a game of bowling.
        """
        self.rolls = [] # list to store the rolls in
        self.frame = 1  # used to track invalid inputs for each frame
        self.roll_in_frame = 1 # track the roll within a frame
    
    def roll(self, pins):
        """Records the number of knocked down pins for a single roll. 

        Args:
            pins (int): The number of pins that were hit on a roll.

        Raises:
            ValueError: If the number of pins in a roll are invalid (less than 0 or greater than 10).
            ValueError: If the bowler hit more than 10 pins in a frame (unless it's the 10th frame).
            ValueError: If the bowler exceeds the maximum number of 21 rolls per game.
            ValueError: If the user inputs a spare on the first roll of a frame.
            ValueError: If the input is invalid (string outside of the allowed input).
        """

        def is_valid_pins(pins):
            try:
                pins = int(pins)
                return True
            except ValueError:
                return False

        # convert "x" or "X" to a strike
        if isinstance(pins, str) and pins.upper() == "X":
            pins = BowlingGame.strike

        # convert "/" to a spare based on the last input
        elif isinstance(pins, str) and pins == "/":
            if self.roll_in_frame < 2:
                raise ValueError("Spare not eligible on first roll of frame")
            first_roll = self.rolls[-1]
            pins = 10 - first_roll


        elif not is_valid_pins(pins):
            raise ValueError("Number of pins entered is invalid. Please enter a number between 0 and 10, "
            "/ for a spare, or X fr a strike")
        else:
            pins = int(pins)

        # check if the number of pins is valid
        if pins < 0 or pins > BowlingGame.strike:
            raise ValueError("Pins must be between 0 and 10")
        
        if len(self.rolls) >= 21:
            raise ValueError("Cannot have more than 21 rolls")
        
        if self.frame < BowlingGame.frames and self.roll_in_frame == 2 and (self.rolls[-1] + pins > BowlingGame.strike):
            raise ValueError("Sum for frame exceeded 10 pins")
        
        self.rolls.append(pins)
        
        if self.frame < BowlingGame.frames:
            if self.roll_in_frame == 2 or pins == BowlingGame.strike:
                self.frame += 1
                self.roll_in_frame = 1
            else:
                self.roll_in_frame += 1
        else:
            # handle logic of 10th frame; end game if 10th turn and no spare/strike, 21st roll (maximum), or third roll in frame (maximum)
            if self.roll_in_frame > 1 and (self.frame == BowlingGame.frames and sum(self.rolls[-2:]) < BowlingGame.strike) or len(self.rolls) == 21 or self.roll_in_frame > 2:
                self.frame += 1 # increase the frame counter to signal that the game is over
            else:
                self.roll_in_frame += 1

        
    def score(self):
        """Computes the (current) score of the bowling game, based on the recorded rolls.

        Returns:
            int: returns the score of the game.
        """
        score = 0
        roll_index = 0
        
        for turn in range(self.frame):     # compute the score for each frame / turn of the game
            if roll_index < len(self.rolls):
                if self.is_strike(roll_index):      # 10 points for strike + total of next 2 rolls
                    score += 10 + self.rolls[roll_index + 1] + self.rolls[roll_index + 2]     
                    roll_index += 1                                     
                elif self.is_spare(roll_index):     # 10 points for spare + the next roll                   
                    score += 10 + self.rolls[roll_index + 2]
                    roll_index += 2
                elif roll_index + 1 < len(self.rolls) and turn < BowlingGame.frames:    # simply take the sum of the two rolls in a frame if no special case occurred
                    score += self.rolls[roll_index] + self.rolls[roll_index + 1]
                    roll_index += 2
                else:       # compute temporary scoreboard for the current roll, even if frame is not yet finished
                    if turn < BowlingGame.frames:
                        score += self.rolls[roll_index]
                    break   # ensure that score computation is stopped for temporary results
                    
        return score
    
    
    def is_spare(self, index):
        """Checks if the bowler hit a spare (two rolls in a frame sum up to 10).

        Args:
            index (int): The index of the first roll of the current frame.

        Returns:
            bool: True if the bowler hit a spare, False otherwise.
        """
        if index + 2 < len(self.rolls): # check for list index out of range; error handling for temporary score results.
            return self.rolls[index] + self.rolls[index +1] == BowlingGame.strike
        return False
    
    def is_strike(self, index):
        """Checks if the bowler hit a strike (knocked down all ten pins on first roll of frame).

        Args:
            index (int): The index of the first roll of the current frame.

        Returns:
            bool: True if the bowler hit a strike, False otherwise
        """
        if index + 2 < len(self.rolls): # check for list index out of range; error handling for temporary score results.
            return self.rolls[index] == BowlingGame.strike
        return False

if __name__ == '__main__':
    game = BowlingGame()
    
    print("Welcome to a game of American ten-pin bowling.")
    print("Please enter the number of pins you knocked down in each roll.")
    
    
    while game.frame <= 10:
        try:
            pins = (input(f"Frame {game.frame}, Roll {game.roll_in_frame}:"))
            game.roll(pins)
            print(f"Current Score: {game.score()}")
        except ValueError as e:
            print(f"Invalid input: {e}. Try again.")
    print(f"Game Over! Final Score is: {game.score()}")