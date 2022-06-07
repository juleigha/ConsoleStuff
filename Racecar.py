import random

class Racecar:
    _color:str
    _number:int
    _location:int
    _min_speed:int
    _max_speed:int

    def __init__(self, color:str, number:int, min_speed:int = 10, max_speed:int=10)->None:
        self._color = color
        self._number = number
        self._location = 0
        self._min_speed = min_speed
        self._max_speed = max_speed

    def move(self)->None:
        self._location+= random.randint(self._min_speed,self._max_speed)

    def get_name(self)->str:
        return self._color +" "+ str(self._number)

    def get_location(self)->int:
        return self._location
    
    def reset_location(self)->None:
        self._location = 0
