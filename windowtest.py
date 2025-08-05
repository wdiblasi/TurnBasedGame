import tkinter as tk
import asyncio

class Game:
    def __init__(self, root):
        self.root = root
        self.loop = asyncio.get_event_loop()
        self.label = tk.Label(root, text="Game starts soon...")
        self.label.pack()

        # Start the async game loop
        self.loop.create_task(self.game_loop())

        # Step asyncio using tkinter's mainloop
        self.root.after(50, self.step_asyncio)

    def step_asyncio(self):
        self.loop.call_soon(self.loop.stop)
        self.loop.run_forever()
        self.root.after(50, self.step_asyncio)

    def update_label(self, text):
        # Schedule GUI update from async code
        self.root.after(0, lambda: self.label.config(text=text))

    async def game_loop(self):
        for i in range(5):
            await asyncio.sleep(1)
            self.update_label(f"Turn {i}")
        self.update_label("Game Over!")

# Start the GUI
root = tk.Tk()
root.title("Async + Tkinter")
game = Game(root)
root.mainloop()