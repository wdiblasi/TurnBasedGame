from entity import Entity
from abc import ABC, abstractmethod
import asyncio
from queue import Queue

import tkinter as tk

q = []

# Helper function for popup window
async def get_user_move(root, special_move_name, player):
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    def on_select(move_type):
        if not future.done():
            future.set_result(move_type)

    # Schedule popup to run in Tkinter's main thread
    root.after(0, lambda: MovePopup(root, special_move_name, on_select, player))
    return await future

class Player_Char(Entity):
    def __init__(self, max_health, strength, timer_cap, position, role):
        self.attack_modifier = 1.0
        super().__init__(max_health, strength, timer_cap, position, role)
        self.root = tk._default_root # There can only be one default root

    # Waits for player input before an ally takes a turn
    async def take_turn(self):
        task_num = self.position
        q.append(task_num)
        await self.wait_for_turn(task_num)
        print(f"It is the character in position {self.position}'s turn.")
        print(f"1: Standard Attack (Deal damage to target)\n2: {self.special_move_name}")

        """try:
            move_type = int(await asyncio.to_thread(input, "Enter the number that corresponds with your action: "))
        except ValueError:
            print("Invalid input. Defaulting to standard attack.")
            move_type = 1"""
        
        move_type = await get_user_move(self.root, self.special_move_name, self)

        if move_type == 1:
            asyncio.create_task(self.standard_attack())
        if move_type == 2:
            await self.special_move()
        
        # Remove from queue so next turn can start
        q.remove(task_num)
        
    # Waits to see if it is the ally in this positions turn before continuing its turn
    async def wait_for_turn(self, task_num):
        while q[0] != task_num:
            await asyncio.sleep(0.2)


# Custom popup class because async and tkinter hate each other
class MovePopup(tk.Toplevel):
    def __init__(self, parent, special_move_name, on_select, player):
        super().__init__(parent)
        self.title("Choose Your Action")
        self.on_select = on_select
        

        # Center the popup
        self.update_idletasks()
        width, height = 600, 170
        x = self.winfo_screenwidth() // 2 - width // 2
        y = self.winfo_screenheight() // 2 - height // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        # UI content
        tk.Label(self, text=f"It is the {player.role} in position {player.position}'s Turn", font="Ariel 20").pack(pady=10)
        tk.Button(self, text=f"1: Standard Attack (Deal {int(player.strength * player.attack_modifier)} damage to enemy)", font="Ariel 16", command=lambda: self.choose(1)).pack(pady=5)
        tk.Button(self, text=f"2: {special_move_name}", font="Ariel 16", command=lambda: self.choose(2)).pack(pady=5)

        self.protocol("WM_DELETE_WINDOW", lambda: self.choose(1))  # default on close

    def choose(self, move_type):
        self.on_select(move_type)
        self.destroy()