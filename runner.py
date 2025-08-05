from attacker import Attacker
from healer import Healer
from tank import Tank
from enemy import Enemy
import asyncio

import tkinter as tk
from tkinter import ttk

class Game:
    # List that holds every entity
    entities = []

    # Runs setup method
    # Sets state to running
    # Runs play method until state changes
    # Outputs corresponding result from state
    def __init__(self,root): 
        self.root = root
        self.loop = asyncio.get_event_loop()
        self.health_bars = []
        self.label = tk.Label(root, text="Game Statistics")
        self.label.pack()

        self.state = 0 # 0 = Running, 1 = Player Win, 2 = Player Loss

        self.setup()
        print("Setup Completed")

        self.loop.create_task(self.play())

        # Step asyncio using tkinter's mainloop
        self.root.after(50, self.step_asyncio)


    def step_asyncio(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        self.root.after(50, self.step_asyncio)

    def update_label(self):
        # Schedule GUI update from async code
        for i in range(len(self.health_bars)):
            self.root.after(0, lambda i=i: self.health_bars[i].config(text=self.entities[i].to_string()))


    # Game setup
    # Adds three player controlled characters
    # Adds Enemies
    # Adds list of entities into every entity
    # Window setup
    def setup(self):
        # Entity setup
        self.entities.append(Attacker(0))
        self.entities.append(Healer(1))
        self.entities.append(Tank(2))
        self.entities.append(Enemy(3))
        for i in range(len(self.entities)):
            self.entities[i].set_list(self.entities)
            self.health_bars.append(tk.Label(self.root, text = self.entities[i].to_string()))
            self.health_bars[i].pack()

    # This function creates timer tasks for each entity
    # It also creates tasks that cancel an entities timer task if the game has ended
    # After all of these tasks have finished it outputs the game's result
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
        
        # Output result
        if self.state == 1:
            print("Congratulations! You Win!!!")
            self.root.after(0, lambda: self.label.config(text="Congratulations! You Win!!!"))
        if self.state == 2:
            print("Game Over. You lose.")
            self.root.after(0, lambda: self.label.config(text="Game Over. You lose."))

    # This task will end its corresponding task if the game has ended
    async def tasks_control(self, ent, index, turn_tasks):
        while self.state == 0 and not turn_tasks[index].done():
            await asyncio.sleep(0.2)
        if not ent.is_alive():
            print(f"{index} has died")
        turn_tasks[index].cancel()

    # This task increments its corresponding entity's timer and checks if the game has ended
    # It also updates the label for every entity
    async def timer(self, ent):
        while ent.is_alive():
            await asyncio.sleep(0.01)
            await ent.inc_timer()
            await self.player_loss_check()
            await self.player_win_check()
            self.update_label()

    # Set state to 2 if all allies have died
    async def player_loss_check(self): 
        any_alive = False
        for i in range(0,3):
            if self.entities[i].is_alive():
                any_alive = True
        if any_alive == False:
            self.state = 2

    # Set state to 1 if all enemies have died
    async def player_win_check(self): 
        any_alive = False
        for i in range(3,len(self.entities)):
            if self.entities[i].is_alive():
                any_alive = True
        if any_alive == False:
            self.state = 1
        

def main():
    print("Startup Initiated")
    root = tk.Tk()
    root.title("Turn Based Game")
    game = Game(root)
    root.mainloop()

main()