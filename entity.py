from abc import ABC, abstractmethod
import asyncio

class Entity(ABC):
    # Initialize variables
    def __init__(self, max_health, strength, timer_cap, position, role):
        self.max_health = max_health
        self.hp = self.max_health
        self.strength = strength
        self.timer_cap = timer_cap
        self.timer = 0
        self.position = position
        self.entities = []
        self.is_taunting = False
        self.role = role

    # Increase timer for when turns are taken
    async def inc_timer(self):
        if(self.is_alive()):
            self.timer += 1
            if self.timer == self.timer_cap:
                Turn = asyncio.create_task(self.take_turn())
                await Turn
                self.timer = 0

    # Calls the take_damage method from the target entity
    def deal_damage(self, damage, target):
        self.entities[target].take_damage(damage)

    # Deals damage to self
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    # Heals a percentage of target's health
    def heal_target(self, heal_percent, target):
        self.entities[target].heal_self(heal_percent)

    # Heals a percentage of own health
    def heal_self(self, heal_percent):
        old_hp = self.hp
        self.hp += int(self.max_health * (heal_percent/100.0))
        if(self.hp > self.max_health):
            self.hp = self.max_health
        if old_hp < self.hp:
            print(f"{self.position} has been healed from {old_hp} to {self.hp} hp!")

    # Sets entity list so objects can damage each other
    def set_list(self, entities):
        self.entities = entities

    # Sets an entities hp
    def set_hp(self, hp):
        self.hp = hp

    # Returns an entities hp for testing
    def get_hp(self):
        return self.hp
    
    # Returns True if an entity is alive and False otherwise
    def is_alive(self):
        if self.hp > 0:
            return True
        return False
    
    # Returns a string to be put into a label
    def health_string(self):
        if self.is_alive():
            return f"{self.role} in position {self.position} has {self.hp} health remaining."
        else:
            return f"{self.role} in position {self.position} has passed out."
    
    def turn_string(self):
        if self.is_alive():
            if self.timer == self.timer_cap:
                return f"Turn Status: Ready"
            else:
                return f"Turn Status: {int(100*(self.timer + 0.0)/self.timer_cap)}"
        else:
            return f"Turn Status: X"

    
    @abstractmethod
    async def take_turn(self):
        pass

    @abstractmethod
    async def standard_attack(self):
        pass

    @abstractmethod
    async def special_move(self):
        pass