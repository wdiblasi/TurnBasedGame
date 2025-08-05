from attacker import Attacker
from healer import Healer
from tank import Tank
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
        self.entities.append(Attacker(0))
        self.entities.append(Healer(1))
        self.entities.append(Tank(2))
        self.entities.append(Enemy(3))
        for i in range(len(self.entities)):
            self.entities[i].set_list(self.entities)

    """
    async def play(self):
        await asyncio.sleep(1)
        for ent in self.entities:
            if ent.timer < ent.timer_cap:
                await ent.inc_timer()
        await self.player_loss_check()
        await self.player_win_check()
    """
    async def play(self):
        turn_tasks = []
        is_alive_tasks = []
        for ent in self.entities:
            turn_tasks.append(asyncio.create_task(self.timer(ent)))
        for i in range(len(turn_tasks)):
            is_alive_tasks.append(asyncio.create_task(self.tasks_control(self.entities[i], i, turn_tasks)))
        for i in range(len(turn_tasks)):
            await is_alive_tasks[i]
            try:
                await turn_tasks[i]
            except asyncio.CancelledError:
                pass

    async def tasks_control(self, ent, index, turn_tasks):
        while self.state == 0 and not turn_tasks[index].done():
            await asyncio.sleep(0.2)
        if not ent.is_alive():
            print(f"{index} has died")
        turn_tasks[index].cancel()

    async def timer(self, ent):
        while ent.is_alive():
            await asyncio.sleep(1)
            await ent.inc_timer()
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
    print("Startup Initiated")
    runner = Game()

main()