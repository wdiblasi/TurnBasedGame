from player_char import Player_Char
import asyncio

attacker_max_health = 100
attacker_strength = 20
attacker_timer_cap = 1

class Attacker(Player_Char):
    def __init__(self, position):
        super().__init__(attacker_max_health, attacker_strength, attacker_timer_cap, position)
        self.special_move_name = "Charge (increase attack modifier)"
        self.attack_modifier = 1.0

    async def standard_attack(self):
        target = int(await asyncio.to_thread(input, "Enter the position of your target: "))
        print(f"You have done {int(self.strength * self.attack_modifier)} damage to the enemy in position {target}.")

    async def special_move(self):
        self.attack_modifier += 0.25
        print(f"Your attack modifier has been increased to {self.attack_modifier}")