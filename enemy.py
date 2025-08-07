import random
from entity import Entity

enemy_max_health = 300
enemy_strength = 40
enemy_timer_cap = 140

class Enemy(Entity):

    def __init__(self, position):
        super().__init__(enemy_max_health, enemy_strength, enemy_timer_cap, position, "Enemy")
        self.special_move_name = "Sweeping Strike"
        self.turn_count = 0 # Number of turns the enemy has taken
        self.valid_targets = [0,1,2]

    # The enemy will automatically take its turn and perform an additional special move every three turns
    async def take_turn(self):
        # Removing perished allys from enemy target list
        index_list = self.valid_targets.copy()
        for i in index_list:
            if not self.entities[i].is_alive():
                self.valid_targets.remove(i)

        # Always calls standard attack
        # Calls special move every 3 turns
        self.turn_count += 1
        await self.standard_attack()
        if self.turn_count % 3 == 0:
            await self.special_move()

    # Deal damage equal to strength to a random player character
    async def standard_attack(self):
        taunting_allys = []
        for index in self.valid_targets:
            if self.entities[index].is_taunting:
                taunting_allys.append(index)
                self.entities[index].is_taunting = False
        if len(taunting_allys) > 0:
            target = random.choice(taunting_allys)
        else:
            target = random.choice(self.valid_targets)
        print(f"The enemy has done {int(self.strength)} damage to the ally in position {target}.")
        self.deal_damage(int(self.strength),target)

    # Deal damage equal to strength to all living allies
    async def special_move(self):
        print(f"The enemy has done {int(self.strength)} damage to every ally!")
        for target in self.valid_targets:
            self.deal_damage(int(self.strength),target)