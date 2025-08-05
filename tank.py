from player_char import Player_Char
import asyncio

tank_max_health = 200
tank_strength = 15
tank_timer_cap = 50

class Tank(Player_Char):
    def __init__(self, position):
        super().__init__(tank_max_health, tank_strength, tank_timer_cap, position, "Tank")
        self.special_move_name = f"Taunt (Enemy must target this character on its next turn)"

    # Deals (strength * modifier) damage to target enemy
    async def standard_attack(self):
        target = 3 #int(await asyncio.to_thread(input, "Enter the position of your target: "))
        print(f"You have done {int(self.strength)} damage to the enemy in position {target}.")
        self.deal_damage(int(self.strength),target)

    # Increases attack modifier
    async def special_move(self):
        self.is_taunting = True