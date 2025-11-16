from datetime import datetime
from time import sleep


class pill :
    def __init__(self, name, last_taken=None, cooldown=8, dosage=8) :
        self.name = name
        self.dosage = dosage
        self.last = last_taken
        self.cooldown = (cooldown) * 60**2

    def take(self) :
        self.last = datetime.now()

    def time_till_next(self) :
        if self.last == None :
            return True
        curr = datetime.now()
        elapsed = (curr - self.last).total_seconds()
        print(f"Time since last taken: {elapsed}s")
        return elapsed >= (self.cooldown)
        

oxy = pill("Oxy Long", datetime.now(), 1/360)

sleep(10)

print(oxy.time_till_next())








