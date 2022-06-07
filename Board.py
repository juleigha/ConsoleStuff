import random
class Board():
    """Represent a game board for the game.

       Public methods: __init__, get_num_rows, get_num_cols,
       add_pawn, delete_pawn, take_turn, pawn_at, __str__
    """

    # Annotate fields
    _rows: int          # The number of rows 
    _cols: int          # The number of columns
    _pawns: "dict[tuple: Pawn]"

    def __init__(self, rows: int, cols: int) -> None:
        """Initialize rows and cols to values passed and create an empty dict for pawns."""
        self._rows = rows
        self._cols = cols
        self._pawns = {}

    def get_num_rows(self) -> int:
        """Return the number of rows (int)."""
        return self._rows

    def get_num_cols(self) -> int:
        """Return the number of columns (int)."""
        return self._cols
    
    def add_pawn(self, pawn: "Pawn", row: int, col: int) -> bool:
        """Return True and add the pawn if there isn't already a pawn there
           and (row,col) is within bounds."""
        result = False
        if row < self._rows and row >= 0 and col < self._cols and col >= 0:
            if not (row, col) in self._pawns:
                self._pawns[(row, col)] = pawn
                result = True
        return result

    def delete_pawn(self, pawn: "Pawn", row: int, col: int) -> None:
        """Remove the pawn from the board."""
        if (row, col) in self._pawns:
            del self._pawns[(row, col)]
            
    def take_turn(self) -> None:
        """Allow each pawn to take a turn."""
        safe_pawns = self._pawns.copy()
        for pawn in safe_pawns:
            safe_pawns[pawn].take_turn()

    def pawn_at(self, row: int, col: int) -> bool:
        """Return True if there is a pawn at row, col."""
        return (row, col) in self._pawns

    def __str__(self) -> str:
        """Return a string version of the board."""
        result = " |0|1|2|3|4|5|6|7|8|9|\n"
        count = 0
        for row in range(self._rows):
            result += str(count) + "|"
            for col in range(self._cols):
                if (row, col) in self._pawns:
                    result += str(self._pawns[(row, col)]) + "|"
                else:
                    result += " |"
            result += "\n"
            count += 1
        return result
class Pawn():
    """Abstract superclass of pawn types

    public methods: __init__(), get_row(),get_col(),
    take_turn(),__str__()
    """
    
    _row:int
    _col:int
    _symbol:str
    _board:Board

    def __init__(self, row:int, col:int,board:Board, symbol:str)->None:
        """init a pawn with passed coordinates, name and board to add to,
        adds pawn to board """
        self._row = row
        self._col = col
        self._symbol = symbol
        board.add_pawn(self, row, col)
        self._board = board
        
    def _move_to(self, new_row:int,new_col:int)->bool:
        """checks board & returns false if space is occupied"""
        result:bool = False
        if not(self._board.pawn_at(new_row,new_col)):
            result = True
        return result

    def get_row(self)->int:
        """return row of pawn"""
        return self._row
    
    def get_col(self)->int:
        """returns collumn of pawn"""
        return self._col
    
    def take_turn(self)->None:
        """changes the pawns location depending on subclass"""
        print(hi)
        pass
    def __str__(self)->str:
        """return symbol of pawn"""
        return self._symbol
    
class RandomPawn(Pawn):
    """Represents a pawn that moves randomly

    public methods: __init__, take_turn()"""
    
    def __init__(self, row:int, col:int,board:Board, symbol:str)->None:
        """init super"""
        super().__init__(row,col,board,symbol)

    def take_turn(self)->None:
        """override super, print location, generate rand coords, check
        if blocked, delete and re-add pawn to board"""
        print("I am " + self._symbol + " and I am at ("+str(self._row)+","+str(self._col)+")")
        rows:int = self._board.get_num_rows()
        cols:int = self._board.get_num_cols()
        new_row:int = random.randint(0,self._board.get_num_rows()-1)
        new_col:int = random.randint(0,self._board.get_num_cols()-1)
        if(self._move_to(new_row,new_col)):
            self._board.delete_pawn(self, self._row,self._col)
            self._board.add_pawn(self, new_row,new_col)
            self._row = new_row
            self._col = new_col
            print("Moving to ("+str(new_row)+","+str(new_col)+")")
        else:
            print("can't move, ("+str(new_row)+","+str(new_col)+") is blocked") 
        return
    
class PatrolPawn(Pawn):
    """Represents a pawn that moves around the perimeter

    public methods: __init__, take_turn()"""
    
    def __init__(self, row:int, col:int,board:Board, symbol:str)->None:
        """init super"""
        super().__init__(row,col,board,symbol)

    def take_turn(self)->None:
        """print loc, check if blocked and inrange and delete and re-add to board"""
        print("I am " + self._symbol + " and I am at ("+str(self._row)+","+str(self._col)+")")
        rows:int = self._board.get_num_rows()
        cols:int = self._board.get_num_cols()
        new_row:int = self._row
        new_col:int = self._col
        # change location if at a corner
        if (self._col == cols - 1 and self._row < rows-1):
            new_row = self._row+1
        elif (self._row == rows - 1 and self._col >0):
            new_col = self._col - 1
        elif (self._col == 0 and self._row > 0):
            new_row = self._row - 1
        elif (self._row == 0 and self._col < cols - 1):
            new_col = self._col + 1
        # move pawn 
        if(self._move_to(new_row,new_col)):
            self._board.delete_pawn(self, self._row,self._col)
            self._board.add_pawn(self, new_row,new_col)
            self._row = new_row
            self._col = new_col
            print("Moving to ("+str(new_row)+","+str(new_col)+")")
        else:
            print("can't move, ("+str(new_row)+","+str(new_col)+") is blocked") 
        return

class MagnetPawn(Pawn):
    """Represents a pawn that moves towards the closest pawn

    public methods: __init__, take_turn()"""
    
    def __init__(self, row:int, col:int,board:Board, symbol:str)->None:
        """init super"""
        super().__init__(row,col,board,symbol)

    def take_turn(self)->None:

        """print loc, check if blocked and inrange, find closest
        pawn **not by searching board but by checking pawn_at outwards from
        magnetPawn's location** delete and re-add pawn"""
        
        print("I am " + self._symbol + " and I am at ("+str(self._row)+","+str(self._col)+")")
        rows:int = self._board.get_num_rows()
        cols:int = self._board.get_num_cols()
        searchPerim:int = 1
        #start search at (-1,-1) away from magnet pawn
        r:int = self._row - searchPerim
        c:int = self._col - searchPerim
        found:bool = False
        new_row:int
        new_col:int
        while not(found):
            # do not find self
            if not(c == self._col and r == self._row):
                if(self._board.pawn_at(r,c)):
                    new_row = r
                    new_col = c
                    found = True
            # if end of seach perimeter expand perimeter and start again
            if (r == self._row +searchPerim and c == self._col +searchPerim):
                searchPerim+=1
                r= self._row -searchPerim
            # check next row 
            if (c == self._col + searchPerim):
                c = self._col - searchPerim
                r+=1
            else:
                c+=1
        # determine direction to move 
        if(new_row > self._row):
            new_row= self._row + 1
        elif(new_row < self._row):
            new_row = self._row - 1
        if(new_col > self._col):
            new_col = self._col +1
        elif(new_col < self._col):
            new_col = self._col - 1
        # move pawn
        if(self._move_to(new_row,new_col)):
            self._board.delete_pawn(self, self._row,self._col)
            self._board.add_pawn(self, new_row,new_col)
            self._row = new_row
            self._col = new_col
            print("Moving to ("+str(new_row)+","+str(new_col)+")")
        else:
            print("can't move, ("+str(new_row)+","+str(new_col)+") is blocked") 
        return

def main()->None:
    board:Board = Board(10,10)
    randomPawn:Pawn = RandomPawn(2,2,board,"R")
    patrolPawn:Pawn = PatrolPawn(0,0,board,"P")
    magnetPawn:Pawn = MagnetPawn(random.randint(0,9),random.randint(0,9),board,"M")
    print(board)
    while(input("Type Q to quit, enter for the next round. ").upper()!="Q"):
        board.take_turn()
        print(board)
main()
