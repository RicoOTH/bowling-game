import unittest
from game import BowlingGame

class BowlingGameTest(unittest.TestCase):
    """Tests for the BowlingGame class. 
    Ensures correct scoring behaviour for strikes, spares, normal rolls, and other edge cases.
    """
    
    def setUp(self):
        """Initialize a new game of bowling for each test.
        """
        self.game = BowlingGame()
    
    def roll_arbitrary(self, rolls, pins):
        """small helper function to fill the scoreboard with multiple rolls of an arbitrarily chosen number of pins.

        Args:
            rolls (int): the number of rolls to fill.
            pins (int): the number of pins each roll should knock down.
        """
        for _ in range(rolls):
            self.game.roll(pins)
    
    def test_invalid_roll(self):
        """Test a negative number of pins for a single roll. Should raise a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.game.roll(-1)
        self.assertEqual("Pins must be between 0 and 10", str(context.exception))
    
    def test_invalid_frame(self):
        """Test case for invalid input where a bowler has hit more than 10 pins in a frame. Should raise a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.game.roll(8)
            self.game.roll(5)
        self.assertEqual("Sum for frame exceeded 10 pins", str(context.exception))
    
    def test_too_many_rolls(self):
        """Test case if the bowler has entered too many turns. 21 rolls should be the maximum.
        """
        with self.assertRaises(ValueError) as context:
            self.roll_arbitrary(23, 5)
        self.assertEqual("Cannot have more than 21 rolls", str(context.exception))

    def test_spare_on_first_roll(self):
        """Test to verify that hitting a spare on the first roll of a frame is impossible.
        """
        with self.assertRaises(ValueError) as context:
            self.game.roll("/")
        self.assertEqual("Spare not eligible on first roll of frame", str(context.exception))

    def test_invalid_string(self):
        """Test to see if string inputs other than / and x (or X) are invalid.
        """
        with self.assertRaises(ValueError) as context:
            self.game.roll("v")
        self.assertEqual("Number of pins entered is invalid. Please enter a number between 0 and 10, "
            "/ for a spare, or X fr a strike", str(context.exception))

    def test_strike_and_spare_string(self):
        """Test to verify that the string inputs for strikes and spare are valid.
        """
        self.game.roll("x")
        self.assertEqual(self.game.score(), 10)
        self.game.roll("X")
        self.assertEqual(self.game.score(), 20)
        self.game.roll(4)
        self.game.roll("/")
        self.assertEqual(self.game.score(), 54)
        
    def test_gutter_game(self):
        """Test a "gutter game" where a bowler does not hit any pins at all in the 20 rolls for a game. Should lead to a total score of 0.
        """
        self.roll_arbitrary(20,0)
        self.assertEqual(self.game.score(), 0)
    
    def test_all_ones(self):
        """Test a game where the bowler only hits a single pin for every roll. Should lead to a score of 20 x 1 = 20.
        """
        self.roll_arbitrary(20,1)
        self.assertEqual(self.game.score(), 20)
    
    def test_one_spare(self):
        """Test a scenario with one spare. Computes the temporary score after 3 rolls. Should lead to 5+5+3 for frame 1 and 3 for frame 2 = 16.
        """
        self.game.roll(5)
        self.game.roll(5)
        self.game.roll(3)
        self.assertEqual(self.game.score(), 16)
        
    def test_one_strike(self): 
        """Test a game with one singular strike on roll #1 and arbitrary rolls for the rest. Score should lead to 10+3+2 for frame 1 and 3+2 for frame 2 = 20.
        """
        self.game.roll(10)
        self.game.roll(3)
        self.game.roll(2)
        self.roll_arbitrary(16,0)
        self.assertEqual(self.game.score(), 20)
        
    def test_presumably_spare(self):
        """Test a game where bowler rolls a "strike" on roll #2 after hitting the gutter on roll 1. Should be treated as a spare, and not a strike.
        """
        self.game.roll(0)
        self.game.roll(10)
        self.game.roll(3)
        self.game.roll(2)
        self.roll_arbitrary(16,0)
        self.assertEqual(self.game.score(), 18)
    
    def test_normal_game(self):
        """The suggested test case from the given example task. A full game with a "normal" game score one might run into in the real world.
        """
        rolls = [1,4,4,5,6,4,5,5,10,0,1,7,3,6,4,10,2,8,6]
        for roll in rolls:
            self.game.roll(roll)
        self.assertEqual(self.game.score(), 133)
    
    def test_all_strikes(self):
        """A test case where the bowler rolls only strikes, thereby ruining the fun for everyone else involved in the game. Ensures that strike scores are added accordingly, even in the final bonus rolls.
        """
        for roll in range(12):
            self.game.roll(10)
        self.assertEqual(self.game.score(), 300)
            
    def test_all_spares(self):
        """Test for the bowler only hitting spares - and therefore an additional "strike" on the final bonus roll. Ensures that spares are addedd correctly and the bonus round calculation works as intended.
        """
        for frame in range(10):
            self.game.roll(1)
            self.game.roll(9)
        self.game.roll(10)
        self.assertEqual(self.game.score(), 119)
        
    def test_unable_to_roll_spare_with_more_than_10_points_in_the_last_frame(self):

        with self.assertRaises(ValueError) as context:
            #                                          VVV 2 + 9 > 10
            rolls = [1,4,4,5,6,4,5,5,10,0,1,7,3,6,4,10,2,9,6]
            #                                          ^^^
            
            for roll in rolls:
                self.game.roll(roll)

        self.assertEqual("Sum for frame 10 exceeded 10 pins.", str(context.exception))
        


if __name__ == '__main__':
    unittest.main()