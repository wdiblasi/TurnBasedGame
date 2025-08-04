from attacker import Attacker
from enemy import Enemy
import asyncio

class Game:
    # List that holds every entity
    entities = []

    # Runs setup method
    # Sets state to running
    # Runs play method until state changes
    # Outputs corresponding result from state
    def __init__(self): 
        self.setup()
        self.state = 0 # 0 = Running, 1 = Player Win, 2 = Player Loss
        while self.state == 0:
            asyncio.run(self.play())
        if self.state == 1:
            print("Congratulations! You Win!!!")
        if self.state == 2:
            print("Game Over. You lose.")

    # Game setup
    # Adds three player controlled characters
    # Adds Enemies
    # Adds list of entities into every entity
    def setup(self):
        for i in range(0,3):
            self.entities.append(Attacker(i))
        for i in range(1,3):
            self.entities[i].set_hp(0)
        self.entities.append(Enemy(3))
        for i in range(len(self.entities)):
            self.entities[i].set_list(self.entities)

    async def play(self):
        for ent in self.entities:
            await ent.inc_timer()
        for ent in self.entities: # Remove after testing
            print(ent.get_hp())
        await self.player_loss_check()
        await self.player_win_check()

    async def player_loss_check(self): # Set state to 2 if all entities position 0-2 inclusive are not alive
        any_alive = False
        for i in range(0,3):
            if self.entities[i].is_alive():
                any_alive = True
        if any_alive == False:
            self.state = 2


    async def player_win_check(self): # Set state to 1 if entity in position 4 is not alive
        any_alive = False
        for i in range(3,len(self.entities)):
            if self.entities[i].is_alive():
                any_alive = True
        if any_alive == False:
            self.state = 1
        

def main():
    runner = Game()

main()