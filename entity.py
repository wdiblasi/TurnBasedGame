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
        self.entities = []

    async def inc_timer(self):
        if(self.is_alive()):
            self.timer += 1
            if self.timer >= self.timer_cap:
                await self.take_turn()

    def deal_damage(self, damage, target):
        self.entities[target].take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage

    def set_list(self, entities):
        self.entities = entities

    def set_hp(self, hp):
        self.hp = hp
        
    def get_hp(self):
        return self.hp
    
    def is_alive(self):
        if self.hp > 0:
            return True
        return False
    
    @abstractmethod
    async def take_turn(self):
        pass

    @abstractmethod
    async def standard_attack(self):
        pass

    @abstractmethod
    async def special_move(self):
        pass