import asyncio
count = 0

class Greeting:
    def __init__(self, greeting, counts_between):
        self.greeting = greeting
        self.counts_between = counts_between

    async def greet(self):
        name = await asyncio.to_thread(input, "Enter your name: ")
        print(self.greeting, name)

    def get_cb(self):
        return self.counts_between

greetings = [Greeting("Hi",2),Greeting("Hello",3),Greeting("Waddup",5)]

async def main():
    global count
    global greetings
    while count < 21:
        count += 1
        print(count)
        for g in greetings:
            if count % g.get_cb() == 0:
                await g.greet()
        
    

asyncio.run(main())