class BowlingGame:
    """Represents a game of American ten-pin bowling. Valid inputs are 0-10, /, x, and X.
    
    Attributes:
        strike (int): The number of knocked down pins needed for a strike (10).
        frames (int): The number of frames / turns per game (10).
        rolls (list): A list of dicts storing the knocked down pins of each roll.
        frame (int): Tracks the current frame / turn of the game.
        roll_in_frame (int): Tracks the current roll count within the frame.

    Note: An invalid number of pins hit in a roll, number of rolls, or number of pins hit in a frame will raise `ValueError`.
    """
    strike = 10
    frames = 10
    
    
    def __init__(self):
        """Simple init for a game of bowling.
        """
        self.rolls = [] # list of dicts to store the rolls in
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
            first_roll = self.rolls[-1]["pins"]
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
        
        if self.frame < BowlingGame.frames and self.roll_in_frame == 2 and (self.rolls[-1]["pins"] + pins > BowlingGame.strike):
            raise ValueError("Sum for frame exceeded 10 pins")
        
        
        self.rolls.append({
            "frame": self.frame,
            "roll_in_frame": self.roll_in_frame,
            "pins": pins
        })
        
        if self.frame < BowlingGame.frames:
            if self.roll_in_frame == 2 or pins == BowlingGame.strike:
                self.print_scoreboard()
                self.frame += 1
                self.roll_in_frame = 1
            else:
                self.roll_in_frame += 1
        else:
            # handle logic of 10th frame; end game if 10th turn and no spare/strike, 21st roll (maximum), or third roll in frame (maximum)
            if self.roll_in_frame > 1:  # can safely ignore the first roll in 10th frame
                last_two_rolls = self.rolls[-2:] # fetch the last two rolls to check if they sum to a spare
                if last_two_rolls[0]["frame"] == last_two_rolls[1]["frame"]:
                    if (sum(roll["pins"] for roll in last_two_rolls) < BowlingGame.strike) or len(self.rolls) == 21 or self.roll_in_frame > 2:
                        self.print_scoreboard()
                        self.frame += 1 # increase the frame counter to signal that the game is over
                    else:
                        self.roll_in_frame += 1
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
                    score += 10 + self.rolls[roll_index + 1]["pins"] + self.rolls[roll_index + 2]["pins"]
                    roll_index += 1                                     
                elif self.is_spare(roll_index):     # 10 points for spare + the next roll                   
                    score += 10 + self.rolls[roll_index + 2]["pins"]
                    roll_index += 2
                elif roll_index + 1 < len(self.rolls) and turn < BowlingGame.frames:    # simply take the sum of the two rolls in a frame if no special case occurred
                    score += self.rolls[roll_index]["pins"] + self.rolls[roll_index + 1]["pins"]
                    roll_index += 2
                else:       # compute temporary scoreboard for the current roll, even if frame is not yet finished
                    if turn < BowlingGame.frames:
                        score += self.rolls[roll_index]["pins"]
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
            return self.rolls[index]["pins"] + self.rolls[index +1]["pins"] == BowlingGame.strike
        return False
    
    
    def is_strike(self, index):
        """Checks if the bowler hit a strike (knocked down all ten pins on first roll of frame).

        Args:
            index (int): The index of the first roll of the current frame.

        Returns:
            bool: True if the bowler hit a strike, False otherwise
        """
        if index + 2 < len(self.rolls): # check for list index out of range; error handling for temporary score results.
            return self.rolls[index]["pins"] == BowlingGame.strike
        return False
  
    def print_scoreboard(self):
        """Prints the current scoreboard in the command line.
        """
        print("\n" + "-" * 80)
        print("Frame: ", end=" ")
        for i in range(1,11):
            print(f"{i:^6}", end=" ")
        print (" |", end=" ")
        print("\nRolls:  ", end=" ")
        
          
        next_roll = -1        
        i = 0
        while i < len(self.rolls):
            current_roll = self.rolls[i]
            
            # print strikes
            if current_roll["pins"] == BowlingGame.strike:
                if current_roll["frame"] == BowlingGame.frames: # special print in the last frame to safe space
                    if current_roll["roll_in_frame"] == 1:
                        print("[X", end="|")
                    elif current_roll["roll_in_frame"] == 3:
                        print("X]", end="|")
                    else: 
                        print("X", end="|")
                        
                # print strikes before last frame
                else:
                    print(f"[ {'X':^2} ]", end="|")
                i += 1
            
            elif i + 1 < len(self.rolls): # check if next roll exists to detect spares
                next_roll = self.rolls[i+1]
                
                # print spares; same frame, next roll_in_frame and sum of the two rolls is a "strike"
                if current_roll["frame"] == next_roll["frame"] and current_roll["roll_in_frame"] + 1 == next_roll["roll_in_frame"] and current_roll["pins"] + next_roll["pins"] == BowlingGame.strike:
                    
                    # handle 10th frame special print
                    if current_roll["frame"] == BowlingGame.frames:
                        if current_roll["roll_in_frame"] == 1:
                            print(f"[{current_roll['pins']}|{'/'}", end="|")
                        elif current_roll["roll_in_frame"] == 2:
                            print(f"{current_roll['pins']}|{'/'}]", end="|")
                    
                    # print normal spares        
                    else:
                        print(f"[ {current_roll['pins']:^1}|{'/'} ]", end="|")
                    i += 2
                    
                # print normal turns
                else:
                    # handle 10th frame special print
                    if current_roll["frame"] == BowlingGame.frames:
                        if current_roll["roll_in_frame"] == 2:
                            print(f"{current_roll['pins']}|{next_roll['pins']}]", end="|")
                    else:
                        print(f"[{current_roll['pins']:^1}|{next_roll['pins']:^1}]", end="|")
                    i += 2
                    
            # handle final roll in the game
            else:   
                if current_roll["frame"] == BowlingGame.frames and current_roll["roll_in_frame"] == 3:
                    print(f"{current_roll['pins']}]", end="|")

                # make sure while loop is exited at the end
                break
                    
            next_roll = -1                    


if __name__ == '__main__':
    game = BowlingGame()
    
    print("Welcome to a game of American ten-pin bowling.")
    print("Please enter the number of pins you knocked down in each roll.")
    
    
    while game.frame <= 10:
        try:
            pins = (input(f"Frame {game.frame}, Roll {game.roll_in_frame}:"))
            game.roll(pins)
            print(f"\nCurrent Score: {game.score()}")
        except ValueError as e:
            print(f"Invalid input: {e}. Try again.")
    print(f"Game Over! Final Score is: {game.score()}")