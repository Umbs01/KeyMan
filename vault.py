from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Listbox
from pathlib import Path
from config import firebase,db,auth

class Vault(object):
    def __init__(self, window, account, login_callback):
        self.window = window
        self.window.geometry("664x832")
        self.window.configure(bg="#FFFFFF")
        # method to callback to login page
        self.login_page = login_callback

        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
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
            outline=""
        )

        # Search bar 
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(
            331.0,
            40.0,
            image=self.image_image_1
        )

        # search field
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_1 = self.canvas.create_image(
            296.0,
            106.5,
            image=self.entry_image_1
        )
        self.searchEntry = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=('Helvetica 20'),
        )
        self.searchEntry.place(
            x=59.0,
            y=81.0,
            width=474.0,
            height=54.0
        )
        self.searchEntry.bind('<KeyRelease>',self.scan)

        # search button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.searchBTN = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.fetch,
            relief="flat",
        )
        self.searchBTN.place(
            x=533.0,
            y=81.0,
            width=131.0,
            height=51.0
        )

        # Edit button
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=0.0,
            y=764.0,
            width=222.0,
            height=68.0
        )

        # new button
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            x=222.0,
            y=764.0,
            width=222.0,
            height=68.0
        )

        # logout button
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.logout,
            relief="flat"
        )
        self.button_4.place(
            x=444.0,
            y=764.0,
            width=220.0,
            height=68.0
        )

        # magnifying image
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(
            29.0,
            106.0,
            image=self.image_image_2
        )

        # listbox
        self.list = Listbox(
            self.canvas,
            bg="#FFFFFF",
            fg="#000000",
            font=("Arial", 30),
            highlightcolor="#2E3571",
            yscrollcommand= True,
        )
        self.list.place(
            x=0.0,
            y=132.0,
            width=664.0,
            height=633.0
        )
        # vault items
        userId = account.get("localId")
        items = db.child("users").child(userId).child("vault").get(account['idToken'])
        self.listItems = items.val()
        self.filtered_data = self.listItems
        print(self.listItems)
        self.update()

        self.window.resizable(False, False)

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path("assets/frame1")
        return ASSETS_PATH / Path(path)
    
    def logout(self):
        self.window.destroy()
        self.login_page()

    def scan(self,event):
        value = event.widget.get()

        if value == '':
            data = self.listItems
        else:
            data = []
            for item in self.listItems:
                if value.lower() in item.lower():
                    data.append(item)
        
        self.filtered_data = data

    def update(self):
        # clear all the value
        self.list.delete(0,'end')
        # insert new query
        for item in self.filtered_data:
            self.list.insert('end',item)

    def fetch(self): 
        self.update()