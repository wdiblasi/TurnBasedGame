from attacker import Attacker
import asyncio

class Game:
    # List that holds every entity
    entities = []

    def __init__(self): 
        self.setup()
        self.state = 0 # 0 = Running, 1 = Player Win, 2 = Player Loss
        while self.state == 0:
            asyncio.run(self.play())

    def setup(self):
        for i in range(0,2):
            self.entities.append(Attacker(i))
        for i in range(0,2):
            self.entities[i].set_list(self.entities)

    async def play(self):
        for ent in self.entities:
            await ent.inc_timer()
        for ent in self.entities: # Remove after testing
            print(ent.get_hp())

    async def player_loss_check(self): # Set state to 2 if all entities position 0-2 inclusive are not alive
        pass

    async def player_win_check(self): # Set state to 1 if entity in position 4 is not alive
        pass
        

def main():
    runner = Game()

main()