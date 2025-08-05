from entity import Entity
from abc import ABC, abstractmethod
import asyncio

class Player_Char(Entity):
    def __init__(self, max_health, strength, timer_cap, position):
        super().__init__(max_health, strength, timer_cap, position)

    # Waits for player input before an ally takes a turn
    async def take_turn(self):
        print(f"It is the character in position {self.position}'s turn.")
        print(f"1: Standard Attack (Deal damage to target)\n2: {self.special_move_name}")
        try:
            move_type = int(await asyncio.to_thread(input, "Enter the number that corresponds with your action: "))
        except ValueError:
            print("Invalid input. Defaulting to standard attack.")
            move_type = 1

        if move_type == 1:
            asyncio.create_task(self.standard_attack())
        if move_type == 2:
            await self.special_move()