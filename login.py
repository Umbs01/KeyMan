from tkinter import Tk, Canvas, Label, Button, PhotoImage, Entry, Toplevel, messagebox
from pathlib import Path
from vault import Vault
from signin import Signin
from config import firebase
import json
import requests

class Login(object):
    def __init__(self, window):
        self.window = window
        self.window.title("KeyMan - Login")
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
        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            331.0,
            454.0,
            image=self.image_image_1
        )
        
        self.label1 = Label(
            bd=0,
            bg="#242439",
            fg="#FFFFFF",
            font=('Montserrat 12'),
            text='Email',
        )
        self.label1.place(
            x=135.0,
            y=330.0
        )

        self.entry_image_1 = PhotoImage(
            file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            331.5,
            382.5,
            image=self.entry_image_1
        )
        self.userEntry = Entry(
            bd=0,
            bg="#36364A",
            fg="#FFFFFF",
            highlightthickness=0,
            font=('Montserrat 20'),
            
        )
        self.userEntry.place(
            x=135.0,
            y=360.0,
            width=393.0,
            height=60.0
        )

        self.label2 = Label(
            bd=0,
            bg="#242439",
            fg="#FFFFFF",
            font=('Montserrat 12'),
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
            bd=0,
            bg="#36364A",
            fg="#FFFFFF",
            highlightthickness=0,
            font=('Montserrat 20'),
            show="*"
        )
        self.passEntry.place(
            x=135.0,
            y=467.0,
            width=393.0,
            height=60.0
        )

        self.canvas.create_text(
            255.0,
            223.0,
            anchor="nw",
            text="Login",
            fill="#FFFFFF",
            font=("Montserrat", 54 * -1)
        )

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
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

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            command=self.to_signin,
            relief="flat"
        )
        self.button_2.place(
            x=267.0,
            y=676.0,
            width=120.0,
            height=36.0
        )

        self.canvas.create_rectangle(
            0.0,
            0.0,
            664.0,
            81.0,
            fill="#2E3571",
            outline="")

        image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            331.0,
            40.0,
            image=image_image_2
        )

        self.account = {}
        self.window.resizable(False,False)
        self.window.mainloop()
        

    def relative_to_assets(self, path: str) -> Path:
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")
        return ASSETS_PATH / Path(path)

    def to_vault(self,account):
        vault_window = Toplevel(self.window)
        vault_window.title("KeyMan - Vault")
        vault_page = Vault(vault_window, account, self.show_login)
    
        def on_vault_close():
            vault_window.destroy()
            self.window.deiconify()

        vault_window.protocol("WM_DELETE_WINDOW", on_vault_close)    
        self.window.withdraw()

    def to_signin(self):
        singin_window = Toplevel(self.window)
        singin_window.title("KeyMan - Sign Up")
        sigin_page = Signin(singin_window, self.show_login)

        def on_page_close():
            singin_window.destroy()
            self.window.deiconify()
        
        singin_window.protocol("WM_DELETE_WINDOW", on_page_close)
        self.window.withdraw()

    def show_login(self):
        self.window.deiconify()

    def submit(self):
        auth = firebase.auth()
        account = self.userEntry.get()
        password = self.passEntry.get()
        
        try: 
            user = auth.sign_in_with_email_and_password(account,password)
        
        except requests.exceptions.ConnectionError as err:
            messagebox.showerror("Connectivity Error","Please check if the device is connected to the internet.")
            return

        except requests.HTTPError as err:
            errJSON = err.args[1]
            error = json.loads(errJSON)['error']['message']

            if error == "INVALID_LOGIN_CREDENTIALS":
                errmsg = "Invalid Email/Password."
            elif error == "INVALID_EMAIL":
                errmsg = "Invalid Email."
            elif error == "MISSING_PASSWORD":
                errmsg = "Please Input your password."
            else:
                errmsg = "Unhandled ERROR"

            messagebox.showerror("Pyrebase error", str(errmsg))
            return

        self.to_vault(user)


