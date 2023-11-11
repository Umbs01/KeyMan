from tkinter import  Canvas, Button, PhotoImage, messagebox, Entry, Label
from pathlib import Path
import requests
from config import firebase, db
import json

class Signin(object):
    def __init__(self, window, login_callback):
        self.login_callback = login_callback
        self.window = window
        self.window.title("KeyMan - Sign in")
        self.window.geometry("664x832")
        self.window.configure(bg="#1A1A2E")

        self.canvas = Canvas(
            self.window,
            bg="#1A1A2E",
            height=832,
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
            outline="")

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            331.0,
            40.0,
            image=self.image_image_2
        )

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            331.0,
            454.0,
            image=self.image_image_1
        )

        # sign up header
        self.canvas.create_text(
                245.0,
                223.0,
            anchor="nw",
            text="Sign Up",
            fill="#FFFFFF",
            font=("Helvetica", 54 * -1)
        )
        
        self.label1 = Label(
            self.canvas,
            bd=0,
            bg="#242439",
            fg="#FFFFFF",
            font=('Helvetica 12'),
            text='Email',
        )
        self.label1.place(
            x=135.0,
            y=330.0
        )

        # image for username entry
        self.entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            331.5,
            382.5,
            image=self.entry_image_1
        )
        self.userEntry = Entry(
            self.canvas,
            bd=0,
            bg="#36364A",
            fg="#FFFFFF",
            highlightthickness=0,
            font=('Helvetica 20'),
        )
        self.userEntry.place(
            x=135.0,
            y=360.0,
            width=393.0,
            height=60.0
        )

        self.label2 = Label(
            self.canvas,
            bd=0,
            bg="#242439",
            fg="#FFFFFF",
            font=('Helvetica 12'),
            text='Password',
        )
        self.label2.place(
            x=135.0,
            y=437.0
        )

        self.entry_image_2 = PhotoImage(
            file=self.relative_to_assets("entry_2.png"))
        self.entry_bg_2 = self.canvas.create_image(
            331.5,
            490.5,
            image=self.entry_image_2
        )
        self.passEntry = Entry(
            self.canvas,
            bd=0,
            bg="#36364A",
            fg="#FFFFFF",
            highlightthickness=0,
            font=('Helvetica 20'),
            show="*"
        )
        self.passEntry.place(
            x=135.0,
            y=467.0,
            width=393.0,
            height=60.0
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            command=self.submit,
            relief="flat"
        )
        self.button_1.place(
            x=125.0,
            y=562.0,
            width=413.0,
            height=71.0
        )

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            command=self.callback,
            relief="flat"
        )
        self.button_2.place(
            x=267.0,
            y=676.0,
            width=120.0,
            height=36.0
        )

        self.window.resizable(False, False)

    def relative_to_assets(self, path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")
        return ASSETS_PATH / Path(path)

    def submit(self):
        auth = firebase.auth()
        account = self.userEntry.get()
        password = self.passEntry.get()

        try:
            auth.create_user_with_email_and_password(account,password)

        except requests.exceptions.ConnectionError as err:
            messagebox.showerror("Connectivity Error","Please check if the device is connected to the internet.")
            return

        except requests.HTTPError as err:
            errJSON = err.args[1]
            error = json.loads(errJSON)['error']['message']

            if error == "EMAIL_EXISTS":
                errmsg = "Email already exist."
            elif error == "INVALID_EMAIL":
                errmsg = "Invalid Email format."
            elif error == "WEAK_PASSWORD : Password should be at least 6 characters":
                errmsg = "Password should be at least 6 characters"
            else:
                errmsg = "Unhandled ERROR"

            messagebox.showerror("Pyrebase error", str(errmsg))

            return

        result = auth.sign_in_with_email_and_password(account,password)
        userId = result.get("localId")
        data = {
            "email":account,
            "password":password,
            "vault":{"sample":"sample"}
        }
        db.child("users").child(userId).set(data, result['idToken'])
        alert = messagebox.showinfo("Message", "Successfully created an account!")

    def callback(self):
        self.window.destroy()
        self.login_callback()

    