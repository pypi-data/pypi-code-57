class Tictactoe:
    
    def __init__(self):
        """ 
            Initializes the co_ordinates and total_steps
        
            Args:
                None
            return:
                None
        """
        self.total_steps = 0
        self.co_ordinates = [[0 for i in range(3)] for j in range(3)]
       
    def check_valid(self, x, y):
        """ 
            Checks whether a move is valid or not
        
            Args:
                x is x_co_ordinate and y is y_co_ordinate
            return:
                boolean for the valid move.
        """
        return (x>=0 and x<3) and (y>=0 and y<3) and (self.co_ordinates[x][y] is 0)
    
    def check_mate(self, player, x, y):
        """
            Checks whether the move lead to victory or not.
            
            Args:
                player specifies the player, x is x_co_ordinate and y is y_co_ordinate
                
            return:
                boolean whether player is won or not.
        """
        
        case_check = [x, y]
        self.co_ordinates[x][y] = player
        self.total_steps += 1
        if x is 0 and y is 0:
            return  ((self.co_ordinates[0][1] is player and self.co_ordinates[0][2] is player) or
                    (self.co_ordinates[1][0] is player and self.co_ordinates[2][0] is player) or
                    (self.co_ordinates[1][1] is player and self.co_ordinates[2][2] is player))
        elif x is 0 and y is 1:
            return ((self.co_ordinates[0][0] is player and self.co_ordinates[0][2] is player) or
                   (self.co_ordinates[1][1] is player and self.co_ordinates[2][1] is player))
        elif x is 0 and y is 2:
            return ((self.co_ordinates[0][0] is player and self.co_ordinates[0][1] is player) or
                   (self.co_ordinates[1][2] is player and self.co_ordinates[2][2] is player) or
                   (self.co_ordinates[1][1] is player and self.co_ordinates[2][0] is player))
        elif x is 1 and y is 0:
            return ((self.co_ordinates[0][0] is player and self.co_ordinates[2][0] is player) or
                   (self.co_ordinates[1][1] is player and self.co_ordinates[1][2] is player))     
        elif x is 1 and y is 1:
            return ((self.co_ordinates[0][0] is player and self.co_ordinates[2][2] is player) or
                   (self.co_ordinates[0][2] is player and self.co_ordinates[2][0] is player) or
                   (self.co_ordinates[0][1] is player and self.co_ordinates[2][1] is player) or 
                   (self.co_ordinates[1][0] is player and self.co_ordinates[1][2] is player))
        elif x is 1 and y is 2:
            return ((self.co_ordinates[0][2] is player and self.co_ordinates[2][2] is player) or
                   (self.co_ordinates[1][0] is player and self.co_ordinates[1][1] is player))        
        elif x is 2 and y is 0:
            return ((self.co_ordinates[0][0] is player and self.co_ordinates[1][0] is player) or
                   (self.co_ordinates[2][1] is player and self.co_ordinates[2][2] is player) or
                   (self.co_ordinates[1][1] is player and self.co_ordinates[0][2] is player))    
        elif x is 2 and y is 1:
            return ((self.co_ordinates[2][0] is player and self.co_ordinates[2][2] is player) or
                   (self.co_ordinates[1][1] is player and self.co_ordinates[0][1] is player))  
        elif x is 2 and y is 2:
            return ((self.co_ordinates[0][2] is player and self.co_ordinates[1][2] is player) or
                   (self.co_ordinates[2][0] is player and self.co_ordinates[2][1] is player) or
                   (self.co_ordinates[0][0] is player and self.co_ordinates[1][1] is player))            
        else:
            print("Invalid input")
            return False
        
    def next_move(self, player):
        """
            notes the next move after validating it.
            
            Args:
                player specifies the player
            return:
                boolean whether a player is won or not
        """
        print("Player : {}, type the co-ordinates if you wanna move, with space between them.".format(player))
        valid_move = False
        x, y = [int(i) for i in input().split(" ", 2)]
        while(not valid_move):
            valid_move = self.check_valid (x, y)
            if not valid_move:
                print("Not a valid move. Enter Again!!!")
                x, y = [int(i) for i in input().split(" ", 2)]
            else:
                check_win = self.check_mate(player, x, y)
        return check_win
    
    
    def start_game(self):
        """
            Starts the game where each player has to take turns
            
            Args:
                None
            return:
                None
             
            Determines the winner.
        """
        
        print("Welcome to the game.....\nBoth the players play alternatively.\nSwitch if response is 'Next Player Turn'\nContinue playing if response is 'Play Again'\nThe one who starts the game is the player 'One'")
        while(self.total_steps <= 8):
            result = self.next_move(1)
            if result:
                print("Player One won the game. Congrats!!!")
                break
            if self.total_steps is 9:
                print("There are no winners.")
                break
            result = self.next_move(2)
            if result:
                print("Player Two won the game. Congrats!!!")
                break
                