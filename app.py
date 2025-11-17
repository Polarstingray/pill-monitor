from flask import Flask, request, render_template, redirect
from datetime import datetime, timedelta

app = Flask(__name__)

pills = {}

LOG_FILE = "update.log"

def write_to_log(filename, data):
    try:
        with open(filename, 'a') as log:
            log.write(data)
    except IOError as e:
        print(str(e))

def format_remaining(next_time_str):
    next_time = datetime.strptime(next_time_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    diff = next_time - now
    seconds = int(diff.total_seconds())

    if seconds <= 0:
        seconds = abs(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return ("overdue", f"OVERDUE by {hours}h {minutes}m")

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return ("ok", f"{hours}h {minutes}m remaining")

def parse_time_field(time_str: str):
    """
    Accepts user input like:
      14:30
      2:30 pm
      2 pm
      14
    and returns a datetime with today's date & the parsed time.
    Returns None if parsing fails.
    """

    if not time_str:
        return None

    time_str = time_str.strip().lower()

    formats = [
        "%H:%M", 
        "%I:%M %p",
        "%I %p", 
        "%H", 
    ]

    for fmt in formats:
        try:
            t = datetime.strptime(time_str, fmt).time()
            now = datetime.now()
            return now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        except ValueError:
            continue

    return None

@app.route("/")
def home():
    display = {}

    for name, data in pills.items():
        status, remaining = format_remaining(data["next"])
        display[name] = { **data, "remaining": remaining, "status": status }

    return render_template("index.html", pills=display)

@app.route("/update/<name>", methods=["POST"])
def update(name) :
    if name not in pills :
        return redirect("/")
    
    cooldown = pills[name]["cooldown"]
    now = datetime.now()
    next_time = now + timedelta(hours=cooldown)

    pills[name]["last"] = now.strftime("%Y-%m-%d %H:%M:%S")
    pills[name]["next"] = next_time.strftime("%Y-%m-%d %H:%M:%S")
    pill = pills[name]
    write_to_log(LOG_FILE, f"you took {pill["num"]} {name} at {pill["last"]} | next is {pill["next"]}\n")
    return redirect("/")

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    cooldown = int(request.form.get("cooldown", 8))
    num = int(request.form.get("num", 1))
    time_input = request.form.get("time", None)
    last = parse_time_field(time_input) or datetime.now()

    next_time = last + timedelta(hours=cooldown)

    pills[name] = {
        "num": num,
        "cooldown" : cooldown,
        "last": last.strftime("%Y-%m-%d %H:%M:%S"),
        "next": next_time.strftime("%Y-%m-%d %H:%M:%S")
    }   

    pill = pills[name]
    write_to_log(LOG_FILE, f"you took {pill["num"]} {name} at {pill["last"]} | next is {pill["next"]}\n")
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


