from entity import Entity
from abc import ABC, abstractmethod
import asyncio
from queue import Queue

q = []

class Player_Char(Entity):
    def __init__(self, max_health, strength, timer_cap, position, role):
        super().__init__(max_health, strength, timer_cap, position, role)

    # Waits for player input before an ally takes a turn
    async def take_turn(self):
        task_num = self.position
        q.append(task_num)
        await self.wait_for_turn(task_num)
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
        
        # Remove from queue so next turn can start
        q.remove(task_num)
        

    async def wait_for_turn(self, task_num):
        while q[0] != task_num:
            await asyncio.sleep(0.2)
