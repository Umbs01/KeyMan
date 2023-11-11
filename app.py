import tkinter as tk
from login import Login
from config import db

class Application(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KeyMan")
        self.current_frame = None

        self.show_login_page()

    def show_login_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = Login(self.root)

    def run(self):
        self.root.mainloop()
        

if __name__ == "__main__":
    app = Application()
    app.run()