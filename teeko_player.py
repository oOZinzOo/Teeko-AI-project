# Author: Rattee Jarusirawong
# netID: jarusirawong
# e-mail: jarusirawong@wisc.edu

import random
import copy

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
    
    def check_drop_phase(self,state):
        cnt = 0
        for row in state:
            cnt += row.count('b') + row.count('r')
        if(cnt < 8):
            return True
        return False

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = self.check_drop_phase(state)   # TODO: detect drop phase

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        
        move = []
        if not drop_phase:
            succ_list = self.succ_move(state, self.my_piece)
            alpha= -999999
            beta = 999999
            next_move = [(0,0),(0,0)]
            #print(succ_list)
            for suc in succ_list:
                tmp_state = copy.deepcopy(state)
                tmp_state[suc[0][0]][suc[0][1]] = self.my_piece
                tmp_state[suc[1][0] ][ suc[1][1] ] = ' '
                suc_val = self.Min_Value(tmp_state, 0, alpha, beta)
                if(alpha < suc_val):
                    next_move = suc
                    alpha = suc_val
            move = next_move
            return move
        
        """
        (row, col) = (random.randint(0,4), random.randint(0,4))
        while not state[row][col] == ' ':
            (row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        """
        succ_list = self.succ(state)
        alpha= -999999
        beta = 999999
        next_move = [0,0]
        for suc in succ_list:
            row = suc[0]
            col = suc[1]
            tmp_state = copy.deepcopy(state)
            tmp_state[row][col] = self.my_piece
            suc_val = self.Min_Value(tmp_state, 0, alpha, beta)
            #print(suc, suc_val)
            if(alpha <= suc_val):
                next_move = [row,col]
                alpha = suc_val
        move.insert(0, next_move)
        return move
    
    def Max_Value(self, state, depth, alpha, beta):
        #print("Max")
        if(self.game_value(state) != 0):
            #print(self.heuristic_game_value(state,self.my_piece)  )
            return self.game_value(state)
        if(depth  >= 1):
            return self.heuristic_game_value(state,self.my_piece)
        #self.print_board(state)
        # TODO: always check drop_phase
        if( self.check_drop_phase(state) ):
            succ_list = self.succ(state)
            for row,col in succ_list:
                tmp_state = copy.deepcopy(state)
                tmp_state[row][col] = self.my_piece
                alpha = max(alpha,  self.Min_Value(tmp_state,depth+1, alpha,beta) )
                #if(alpha >= beta): #pruning
                #    return beta
        else:
            succ_list = self.succ_move(state,self.my_piece)
            
            for suc in succ_list:
                tmp_state = copy.deepcopy(state)
                tmp_state[suc[0][0]][suc[0][1]] = self.my_piece
                tmp_state[suc[1][0] ][ suc[1][1] ] = ' '
                alpha = max(alpha,  self.Min_Value(tmp_state,depth+1, alpha,beta) )
                #if(alpha >= beta): #pruning
                #    return beta
        return alpha
    
    def Min_Value(self, state, depth, alpha, beta):
        if(self.game_value(state) != 0):
            return self.game_value(state)
        if(depth  >= 1):
            return self.heuristic_game_value(state,self.opp)
        #self.print_board(state)
        # TODO: always check drop_phase
        if(self.check_drop_phase(state) ):
            succ_list = self.succ(state)
            for row,col in succ_list:
                tmp_state = copy.deepcopy(state)
                tmp_state[row][col] = self.opp
                beta = min(beta,  self.Max_Value(tmp_state,depth+1, alpha, beta) )
                #if(alpha >= beta):   #pruning
                #    return alpha
        else:
            succ_list = self.succ_move(state,self.opp)
            #print(succ_list)
            for suc in succ_list:
                tmp_state = copy.deepcopy(state)
                tmp_state[suc[0][0]][suc[0][1]] = self.opp
                tmp_state[suc[1][0] ][ suc[1][1] ] = ' '
                beta = min(beta,  self.Max_Value(tmp_state,depth+1, alpha,beta) )
               # if(alpha >= beta): #pruning
                #    return alpha
        return beta
    
    def succ(self, state): 
        # [(row, col)]
        
        suc = list()
        for row in range(5):
            for col in range(5):
                if(state[row][col] == ' '):
                    suc.append( (row,col) )
        random.shuffle(suc)
        return suc
        
    def succ_move(self, state, piece):
        #[(row, col), (source_row, source_col)]
        move_row = [-1,0,1]
        move_col = [-1,0,1]
        suc = list()
        for row in range(5):
            for col in range(5):
                if(state[row][col] == piece):
                    for mr in move_row:
                        for mc in move_col:
                            if( row+mr <5 and row+mr>=0 and col+mc<5 and col+mc>=0 and state[row+mr][col+mc] == ' '):
                                suc.append( [(row+mr,col+mc),(row,col)] )
        random.shuffle(suc)
        return suc

        

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece
    '''
    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")'''
    
    def print_board(self, board = []):
        if(board == []):
            board = self.board
        """ Formatted printing for the board """
        for row in range(len(board)):
            line = str(row)+": "
            for cell in board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        
    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            #print("sdfs row", row)
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in  range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col]==self.my_piece else -1
            
        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(3,5):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col]==self.my_piece else -1
        # TODO: check diamond wins
        for row in range(1,4):
            for col in  range(1,4):
                if state[row][col] == ' ' and state[row+1][col] != ' ' and state[row+1][col] == state[row-1][col] == state[row][col-1] == state[row][col+1]:
                    return 1 if state[row][col+1]==self.my_piece else -1
        return 0 # no winner yet
    
    
    def heuristic_game_value(self, state,piece):
        #TODO: generate heauristic
        val = self.game_value(state)
        if(val != 0):
            return val
        mx_val = -2
        mn_val = 2
        # horizontal
        for row in state:
            for col in range(2):
                tmp = list()
                for i in range(4):
                    tmp.append( row[col+i] )
                mx_val = max( mx_val, tmp.count(self.my_piece)*0.2 )
                mn_val = min( mn_val, tmp.count(self.opp)*0.2*(-1) )

        # vertical
        for col in range(5):
            for row in range(2):
                tmp = list()
                for i in range(4):
                    tmp.append( state[row+i][col] )
                mx_val = max( mx_val, tmp.count(self.my_piece)*0.2 )
                mn_val = min( mn_val, tmp.count(self.opp)*0.2*(-1) )

        # \ diagonal
        for row in range(2):
            for col in range(2):
                tmp = list()
                for i in range(4):
                    if(col+i < 5 and row+i < 5):
                        tmp.append( state[row+i][col+i] )
                mx_val = max( mx_val, tmp.count(self.my_piece)*0.2 )
                mn_val = min( mn_val, tmp.count(self.opp)*0.2*(-1) )
            
        # / diagonal
        for row in range(2):
            for col in range(3,5):
                tmp = list()
                for i in range(4):
                    if(col-i >= 0 and row+i < 5):
                        tmp.append( state[row+i][col-i] )
                mx_val = max( mx_val, tmp.count(self.my_piece)*0.2 )
                mn_val = min( mn_val, tmp.count(self.opp)*0.2*(-1) )
                
        # diamond
        for row in range(1,4):
            for col in  range(1,4):
                tmp = list()
                tmp.append(state[row+1][col])
                tmp.append(state[row][col+1])
                tmp.append(state[row-1][col])
                tmp.append(state[row][col-1])
                mx_val = max( mx_val, tmp.count(self.my_piece)*0.2 )
                mn_val = min( mn_val, tmp.count(self.opp)*0.2*(-1) )
        return mx_val+mn_val
        #return mx_val if piece==self.my_piece else mn_val
            
        

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            print(move)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:
        #print("hey")
        #ai.print_board()

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(move)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()

