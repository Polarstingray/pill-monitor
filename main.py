from datetime import datetime, timedelta

LOG_FILE = "update.log"

def write_to_log(filename, data):
    try:
        with open(filename, 'a') as log:
            log.write(data)
    except IOError as e:
        print(str(e))


class Med:
    def __init__(self):
        self.pills = {}

    def add_med(self, name, cooldown=8, num=1):
        last = datetime.now()
        next_dose = last + timedelta(hours=cooldown)

        self.pills[name] = {
            "num": num,
            "last": last,
            "next": next_dose,
        }

        update = (
            f"{name}: took {num} at {last.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"next dose at {next_dose.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        print(update)
        write_to_log(LOG_FILE, update)


if __name__ == '__main__':
    meds = Med()
    while True:
        print("\n\n============================")
        inp = input("Add med? (yes/no): ").lower()

        if inp != "yes":
            continue

        name = input("Enter name: ")
        cooldown = input("Enter cooldown hours (default 8): ")
        num = input("Enter number of pills: ")

        cooldown = int(cooldown) if cooldown.strip() else 8
        num = int(num) if num.strip() else 1

        meds.add_med(name, cooldown, num)
        print(f"Current medications: {meds.pills}")
