from abc import ABC, abstractmethod
import asyncio

class Entity(ABC):
    def __init__(self, max_health, strength, timer_cap, position):
        self.max_health = max_health
        self.hp = self.max_health
        self.strength = strength
        self.timer_cap = timer_cap
        self.timer = 0
        self.position = position
        self.is_alive = True

    async def inc_timer(self):
        self.timer += 1
        if self.timer >= self.timer_cap:
            await self.take_turn()

    @abstractmethod
    async def take_turn(self):
        pass

    @abstractmethod
    async def standard_attack(self):
        pass

    @abstractmethod
    async def special_move(self):
        pass