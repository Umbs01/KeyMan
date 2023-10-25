from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label
from pathlib import Path

class New(object):
    def __init__(self, window):
        self.window = window
        self.window.geometry("664x492")
        self.window.configure(bg="#FFFFFF")
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=492,
            width=664,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            664.0,
            81.0,
            fill="#2E3571",
            outline=""
        )

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            331.0,
            40.0,
            image=self.image_image_1
        )

        self.emailLabel = Label(
            self.canvas,
            bd=0, 
            anchor="nw",
            text="Email",
            font=("KufamRoman Regular", 32 * -1)
        )
        self.emailLabel.place(
            x= 71.0,
            y= 109.0,
        )

        self.passwordLabel = Label(
            self.canvas,
            bd=0,
            anchor="nw",
            text="Password",
            font=("KufamRoman Regular", 32 * -1)
        )
        self.passwordLabel.place(
            x=74.0,
            y=247.0
        )

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            34.0,
            124.0,
            image=self.image_image_2
        )

        self.canvas.create_rectangle(
            35.0,
            216.0,
            526.0,
            217.0,
            fill="#000000",
            outline=""
        )

        self.canvas.create_rectangle(
            34.0,
            364.0,
            524.0,
            365.0,
            fill="#000000",
            outline=""
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_1_clicked(),
            relief="flat"
        )
        self.button_1.place(
            x=534.0,
            y=328.0,
            width=48.0,
            height=48.0
        )

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_2_clicked(),
            relief="flat"
        )
        self.button_2.place(
            x=582.0,
            y=170.0,
            width=39.0,
            height=47.0
        )

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_3_clicked(),
            relief="flat"
        )
        self.button_3.place(
            x=602.0,
            y=328.0,
            width=39.0,
            height=47.0
        )

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_4_clicked(),
            relief="flat"
        )
        self.button_4.place(
            x=151.0,
            y=412.0,
            width=362.0,
            height=57.0
        )

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(
            36.0,
            265.0,
            image=self.image_image_3
        )

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            281.99639892578125,
            334.47180557250977,
            image=self.entry_image_1
        )
        self.entry_1 = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
        )
        self.entry_1.place(
            x=38.0,
            y=309.0,
            width=487.9927978515625,
            height=48.94361114501953
        )

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            281.99639892578125,
            182.47180938720703,
            image=self.entry_image_2
        )
        self.entry_2 = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
        )
        self.entry_2.place(
            x=38.0,
            y=157.0,
            width=487.9927978515625,
            height=48.94361877441406
        )

        self.window.resizable(False, False)

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path("assets/frame2")
        return ASSETS_PATH / Path(path)

    def button_1_clicked(self):
        print("button_1 clicked")

    def button_2_clicked(self):
        print("button_2 clicked")

    def button_3_clicked(self):
        print("button_3 clicked")

    def button_4_clicked(self):
        print("button_4 clicked")

if __name__ == "__main__":
    window = Tk()
    new_app = New(window)
    window.mainloop()
