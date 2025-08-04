from attacker import Attacker
import asyncio

characters = []
def setup():
    characters.append(Attacker(0))

async def play():
    for character in characters:
        await character.inc_timer()

def main():
    setup()
    for i in [0,0,0]:
        asyncio.run(play())

main()