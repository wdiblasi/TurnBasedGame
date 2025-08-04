from entity import Entity
from abc import ABC, abstractmethod
import asyncio

class Player_Char(ABC, Entity):
    def __init__(self, max_health, timer_cap, position):
        super().__init__(max_health, timer_cap, position)

    async def take_turn(self):
        print("It is the character in position " + self.position + "'s turn.")
        print(f"1: Basic Attack\n2: {self.special_move_name}")
        move_type = await asyncio.to_thread(input, "Enter the number that corresponds with your action: ")