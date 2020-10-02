from .model.player import Player
from .model.board import Board 
from .model.agent import Agent
from .model.tile import Tile 
from .model.color import Color
from .model.pawn import Pawn
from .model.state import State

from .io.cli_input import CLIInput
from .io.cli_output import CLIOutput

class Halma():
    '''Halma class responsible for controlling flow in the game
    '''
    def __init__(self, b_size, t_limit, h_player, inputter, outputter):
        '''Constructor

        Parameters:
            b_size (int): Board size
            t_limit (int): Time limit
            h_player (int): Player color
            inputter (CLIInput): Input for CLI
            outputter (CLIOutput): Output for CLI
        '''
        # Initialize properties
        self.inputter = inputter    
        self.outputter = outputter  

        self.t_limit = t_limit
        self.b_size = b_size
        self.h_player = h_player

        # Initialize game location
        red, green, tiles = self.init_location()

        # Initialize Board
        board = Board(b_size, red['pawns'] + green['pawns'], tiles)

        # Init player
        player_1, player_2 = self.init_player(red, green)

        # History
        self.history = []

        # Current Player        
        currentPlayer = player_1 if h_player == Color.GREEN else player_2

        # State
        self.state = State(board, player_1, player_2, currentPlayer)

    def move(self):
        '''Method to move pawn
        '''
        before, after = self.inputter.input(self.state.board, self.state.currentPlayer) 
        self.state.board.move_pawn(before, after)

    def game(self):
        '''Main method for each turn
        '''
        self.state.player_2.state = self.state

        self.move()
        self.outputter.show(self.state.board)
        self.next()
    
    def next(self):
        '''Updating attribute after turn end
        '''
        self.history.append(self.state.deepcopy())
        self.state.currentPlayer = self.state.player_2 if self.state.currentPlayer == self.state.player_1 else self.state.player_1
        self.state.turn += 1
        # self.state.update(self.board, self.state.player_1, self.state.player_2, self.currentPlayer, self.turn)
    
    def init_player(self, red, green):
        '''Initialize Player
        
        Parameters:
            red (dict): Red player
            green (dict): Green player
        
        Returns:
            Tuple(Player, Player: Initialized Player
        '''
        # Initialize Player
        if self.h_player == Color.RED:
            player_1 = Player(red['pawns'], Color.RED, red['win_condition'])
            player_2 = Agent(green['pawns'], Color.GREEN, green['win_condition'], self.t_limit)
        else:
            player_1 = Player(green['pawns'], Color.GREEN, green['win_condition'])
            player_2 = Agent(red['pawns'], Color.RED, red['win_condition'], self.t_limit)
        
        return (player_1, player_2)
    
    def init_location(self):
        '''Initialize all location (tiles, winCondition, etc) for green, red, and board

        Returns:
            Tuple(map, map, list(Tile)): Initialized Location
        '''
        cur_id = 0

        red = {
            'pawns': [],
            'win_condition': [],
        }
        green = {
            'pawns': [],
            'win_condition': [],
        }

        # Create all tiles to neutral
        tiles = [[Tile(i, j, Color.NEUTRAL) for j in range(self.b_size)] for i in range(self.b_size)]

        # Red Location
        for i in range(4):
            for j in range(4-i):
                # Change Tile color to red
                tiles[i][j].color = Color.RED
                # Add win condition for green
                red['win_condition'].append(tiles[i][j])
                # Add red pawn to list
                red['pawns'].append(Pawn(cur_id, tiles[i][j], Color.RED))  
                cur_id += 1

        # Green Location
        count = 1
        for i in range(self.b_size-count, self.b_size-5, -1):
            for j in range(self.b_size-1, self.b_size+count-6, -1):
                # Change Tile color to green
                tiles[i][j].color = Color.GREEN
                # Add win condition for red
                green['win_condition'].append(tiles[i][j])
                # Add green pawn to list
                green['pawns'].append(Pawn(cur_id, tiles[i][j], Color.GREEN))
                cur_id += 1
            count += 1

        return red, green, tiles
