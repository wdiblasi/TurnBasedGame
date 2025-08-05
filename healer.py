from player_char import Player_Char
import asyncio

healer_max_health = 120
healer_strength = 10
healer_timer_cap = 7
healing_percent = 10

class Healer(Player_Char):
    def __init__(self, position):
        super().__init__(healer_max_health, healer_strength, healer_timer_cap, position)
        self.special_move_name = f"Healing spell (Heal up to {healing_percent}% health for all allies)"

    # Deals (strength * modifier) damage to target enemy
    async def standard_attack(self):
        target = 3 #int(await asyncio.to_thread(input, "Enter the position of your target: "))
        print(f"You have done {int(self.strength)} damage to the enemy in position {target}.")
        self.deal_damage(int(self.strength),target)

    # Increases attack modifier
    async def special_move(self):
        # Removing perished allys from healing target list
        valid_targets = [0,1,2]
        index_list = valid_targets.copy()
        for i in index_list:
            if not self.entities[i].is_alive():
                valid_targets.remove(i)
        for target in valid_targets:
            self.heal_target(healing_percent, target)