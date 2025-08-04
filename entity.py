from abc import ABC, abstractmethod
import asyncio

class Entity(ABC):
    def __init__(self, max_health, timer_cap, position):
        self.max_health = max_health
        self.hp = self.max_health
        self.timer_cap = timer_cap
        self.timer = 0
        self.position = position
        self.is_alive = True

    def inc_timer(self):
        self.timer += 1
        if self.timer >= self.timer_cap:
            self.take_turn()

    @abstractmethod
    async def take_turn(self):
        pass

    @abstractmethod
    async def base_attack(self):
        pass

    @abstractmethod
    async def special_move(self):
        pass