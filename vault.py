from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Listbox, Toplevel, Label, messagebox
from pathlib import Path
from config import firebase,db,auth
import tkinter as tk
import time 
import threading

class Vault(object):
    def __init__(self, window, account, login_callback):
        self.window = window
        self.window.geometry("664x832")
        self.window.configure(bg="#FFFFFF")
        self.account = account
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
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png",1))
        self.image_1 = self.canvas.create_image(
            331.0,
            40.0,
            image=self.image_image_1
        )

        # search field
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png",1))
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
            font=('Montserrat 20'),
        )
        self.searchEntry.place(
            x=59.0,
            y=81.0,
            width=474.0,
            height=54.0
        )
        self.searchEntry.bind('<KeyRelease>',self.scan)

        # search button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png",1))
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
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png",1))
        self.button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.to_edit,
            relief="flat"
        )
        self.button_2.place(
            x=0.0,
            y=764.0,
            width=222.0,
            height=68.0
        )

        # new button
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png",1))
        self.button_3 = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.to_new,
            relief="flat"
        )
        self.button_3.place(
            x=222.0,
            y=764.0,
            width=222.0,
            height=68.0
        )

        # logout button
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png",1))
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
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png",1))
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
            font=("Montserrat", 30),
            highlightcolor="#2E3571",
            yscrollcommand= True,
            selectmode=tk.SINGLE,
        )
        self.list.place(
            x=0.0,
            y=132.0,
            width=664.0,
            height=633.0
        )
        
        self.snapshot()
        # refresh vault items every 5 seconds while running in the background
        # self.thread = threading.Thread(target=self.refresh)
        # self.thread.start

        self.window.resizable(False, False)

    def relative_to_assets(self, path: str, frame) -> Path:
        ASSETS_PATH = Path(f"assets/frame{frame}")
        return ASSETS_PATH / Path(path)
    
    def logout(self):
        self.window.destroy()
        self.login_page()

    def snapshot(self):
        userId = self.account.get("localId")
        items = db.child("users").child(userId).child("vault").get(self.account['idToken'])
        self.listItems = items.val()
        self.filtered_data = self.listItems
        self.update()
            
    # def refresh(self):
    #     while True:
    #         time.sleep(5) 
    #         self.snapshot()

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
            self.list.insert('end',item.replace('_','.'))

    def fetch(self): 
        self.update()

    def to_new(self):
        new_popup = Toplevel(self.window)
        new_popup.title("New Item")

        # create a new instance of the New() class
        new = New(new_popup, self.account)

    def to_edit(self):
        selected = self.list.curselection()

        try:
            self.list.get(selected)
        except:
            messagebox.showerror("error","Select an item in the list.")
        else:
            edit_popup = Toplevel(self.window)
            edit_popup.title("Edit Credentials")
            # create a new instance of the Edit() class
            edit = Edit(edit_popup, self.account, self.list.get(selected))

#--------------------------------------------------------------- New Page -----------------------------------------------------------------#

class New(Vault):
    def __init__(self, window, account):
        super().__init__(window, account, login_callback=0)
        self.window = window
        self.window.geometry("664x492")
        self.window.configure(bg="#FFFFFF")
        self.showstatus = tk.StringVar()
        self.showstatus.set("*")

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

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png",2))
        self.image_1 = self.canvas.create_image(
            331.0,
            40.0,
            image=self.image_image_1
        )

        self.siteLabel = Label(
            self.canvas,
            bd=0, 
            bg="#FFFFFF",
            anchor="nw",
            text="Website",
            font=("Montserrat", -30)
        )
        self.siteLabel.place(
            x= 77.0,
            y= 102.0,
        )

        self.accLabel = Label(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            anchor="nw",
            text="Username",
            font=("Montserrat", -30)
        )
        self.accLabel.place(
            x=80.0,
            y=204.0,
        )

        self.passwordLabel = Label(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            anchor="nw",
            text="Password",
            font=("Montserrat", -30)
        )
        self.passwordLabel.place(
            x=80.0,
            y=311.0
        )

        self.canvas.create_rectangle(
            34.0,
            290.0,
            525.0,
            291.0,
            fill="#000000",
            outline=""
        )

        self.canvas.create_rectangle(
            34.0,
            402.0,
            524.0,
            403.0,
            fill="#000000",
            outline=""
        )

        self.canvas.create_rectangle(
            36.0, 
            188.0, 
            448.0, 
            189.0,
            fill="#000000",
            outline=""
        )

        # show/hide button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png",2))
        self.showBtn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggleShow,
            relief="flat"
        )
        self.showBtn.place(
            x=537.0,
            y=371.0,
            width=48.0,
            height=48.0
        )

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png",2))
        self.cpBtn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.copyAcc,
            relief="flat"
        )
        self.cpBtn.place(
            x=546.0,
            y=254.0,
            width=39.0,
            height=47.0
        )

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png",2))
        self.cpPassBtn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.copyPass,
            relief="flat"
        )
        self.cpPassBtn.place(
            x=599.0,
            y=371.0,
            width=39.0,
            height=47.0
        )

        # create button
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png",2))
        self.createBtn = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.create,
            relief="flat"
        )
        self.createBtn.place(
            x=167.0,
            y=426.0,
            width=281.0,
            height=44.0
        )

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("web.png",2))
        self.image_2 = self.canvas.create_image(
            55.0,
            124.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("account.png",2))
        self.image_3 = self.canvas.create_image(
            58.0,
            226.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("key.png",2))
        self.image_4 = self.canvas.create_image(
            58.0,
            334.0,
            image=self.image_image_4
        )

        # site entry
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry.png",2))
        self.entry_bg_3 = self.canvas.create_image(
            243.4,
            164.5,
            image=self.entry_image_3
        )
        self.siteEntry = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=('Montserrat 20'),
        )
        self.siteEntry.place(
            x=39,
            y=152,
            width=408,
            height=32,
        )

        # account entry
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry.png",2))
        self.entry_bg_2 = self.canvas.create_image(
            281,
            266.4,
            image=self.entry_image_2
        )
        self.accEntry = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=('Montserrat 20'),
        )
        self.accEntry.place(
            x=37.0,
            y=254,
            width=488,
            height=32,
        )

        # password entry
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry.png",2))
        self.entry_bg_1 = self.canvas.create_image(
            279,
            378.5,
            image=self.entry_image_1
        )
        self.passEntry = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=('Montserrat 20'),
            show=self.showstatus.get(),
        )
        self.passEntry.place(
            x=35.0,
            y=366.0,
            width=487,
            height=32,
        )

        self.window.resizable(False, False)

    def toggleShow(self):
        if self.showstatus.get() == "":
            self.showstatus.set("*")
        else:
            self.showstatus.set("")
        self.passEntry.config(show=self.showstatus.get())

    def copyAcc(self):
        text = self.accEntry.get()
        self.window.clipboard_clear()
        self.window.clipboard_append(text)

    def copyPass(self):
        text = self.passEntry.get()
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        
    def create(self):
        items = db.child("users").child(self.account["localId"]).child("vault").get(self.account['idToken']).val()
        data = { self.accEntry.get().replace('.','_'): self.passEntry.get().replace('.','_') } # replace . as _ to avoid JSON error
        if data == {'':''}:
            messagebox.showerror("error", "Please input your credentials.")
        elif self.siteEntry.get() in items:
            messagebox.showerror("error","Website is already registered.") 
        else:
            self.items = db.child("users").child(self.account.get("localId")).child("vault").child(self.siteEntry.get().replace('.','_')).update(data, self.account['idToken'])
            
            self.window.destroy()



#----------------------------------------------------------------- EDIT ---------------------------------------------------------------------#

class Edit(New):
    def __init__(self, window, account, selected):
        super().__init__(window, account)
        self.window = window
        self.window.geometry("664x492")
        self.window.configure(bg="#FFFFFF")
        self.selected = selected.replace('.','_')

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

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png",2))
        self.image_1 = self.canvas.create_image(
            331.0,
            40.0,
            image=self.image_image_1
        )

        self.siteLabel = Label(
            self.canvas,
            bd=0, 
            bg="#FFFFFF",
            anchor="nw",
            text="Website",
            font=("Montserrat", -30)
        )
        self.siteLabel.place(
            x= 77.0,
            y= 102.0,
        )

        self.accLabel = Label(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            anchor="nw",
            text="Username",
            font=("Montserrat", -30)
        )
        self.accLabel.place(
            x=80.0,
            y=204.0,
        )

        self.passwordLabel = Label(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            anchor="nw",
            text="Password",
            font=("Montserrat", -30)
        )
        self.passwordLabel.place(
            x=80.0,
            y=311.0
        )

        self.canvas.create_rectangle(
            34.0,
            290.0,
            525.0,
            291.0,
            fill="#000000",
            outline=""
        )

        self.canvas.create_rectangle(
            34.0,
            402.0,
            524.0,
            403.0,
            fill="#000000",
            outline=""
        )

        self.canvas.create_rectangle(
            36.0, 
            188.0, 
            448.0, 
            189.0,
            fill="#000000",
            outline=""
        )

        # show/hide button
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png",2))
        self.showBtn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.toggleShow,
            relief="flat"
        )
        self.showBtn.place(
            x=537.0,
            y=371.0,
            width=48.0,
            height=48.0
        )

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png",2))
        self.cpBtn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.copyAcc,
            relief="flat"
        )
        self.cpBtn.place(
            x=546.0,
            y=254.0,
            width=39.0,
            height=47.0
        )

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png",2))
        self.cpPassBtn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.copyPass,
            relief="flat"
        )
        self.cpPassBtn.place(
            x=599.0,
            y=371.0,
            width=39.0,
            height=47.0
        )

        # save button
        self.saveBtn_img = PhotoImage(file=self.relative_to_assets("saveBtn.png",2))
        self.saveBtn = Button(
            self.canvas,
            image=self.saveBtn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.save,
            relief="flat"
        )
        self.saveBtn.place(
            x=96.0,
            y=426.0,
            width=166.0,
            height=45
        )

        # delete button
        self.delBtn_img = PhotoImage(file=self.relative_to_assets("delBtn.png",2))
        self.delBtn = Button(
            self.canvas,
            image=self.delBtn_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete,
            relief="flat"
        )
        self.delBtn.place(
            x=366.0,
            y=426.0,
            width=164.0,
            height=45
        )

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("web.png",2))
        self.image_2 = self.canvas.create_image(
            55.0,
            124.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("account.png",2))
        self.image_3 = self.canvas.create_image(
            58.0,
            226.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("key.png",2))
        self.image_4 = self.canvas.create_image(
            58.0,
            334.0,
            image=self.image_image_4
        )

        # website entry
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry.png",2))
        self.entry_bg_3 = self.canvas.create_image(
            243.4,
            164.5,
            image=self.entry_image_3
        )
        self.siteEntry = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=('Montserrat 20'),
        )
        self.siteEntry.place(
            x=39,
            y=152,
            width=408,
            height=32,
        )
        # insert the old credentials
        self.siteEntry.insert(0, selected.replace('_','.'))

        # site entry
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry.png",2))
        self.entry_bg_2 = self.canvas.create_image(
            281,
            266.4,
            image=self.entry_image_2
        )
        self.accEntry = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=('Montserrat 20'),
        )
        self.accEntry.place(
            x=37.0,
            y=254,
            width=488,
            height=32,
        )
        self.accEntry.insert(0, list(db.child("users").child(account["localId"]).child("vault").child(self.selected).get(self.account['idToken']).val().keys())[0].replace('_','.'))

        # password entry
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry.png",2))
        self.entry_bg_1 = self.canvas.create_image(
            279,
            378.5,
            image=self.entry_image_1
        )
        self.passEntry = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=('Montserrat 20'),
            show=self.showstatus.get(),
        )
        self.passEntry.place(
            x=35.0,
            y=366.0,
            width=487,
            height=32,
        )

        self.passEntry.insert(0, list(db.child("users").child(account["localId"]).child("vault").child(self.selected).get(self.account['idToken']).val().values())[0].replace('_','.'))

        self.window.resizable(False, False)

    def delete(self):
        db.child("users").child(self.account['localId']).child("vault").child(self.selected).remove(self.account['idToken'])
        self.window.destroy()
        messagebox.showinfo("Success",f"Successfully Deleted {self.selected}")
        self.snapshot()

    def save(self):
        items = db.child("users").child(self.account["localId"]).child("vault").get(self.account['idToken']).val()
        
        # check if theres an existing website
        if self.siteEntry.get() != self.selected and self.siteEntry.get() in items:
            messagebox.showerror("Alert!","Website is already registered")
        else:
            path = db.child("users").child(self.account['localId']).child("vault")
            data = { self.siteEntry.get().replace('.','_') : { self.accEntry.get().replace('_','.') : self.passEntry.get().replace('_','.') } }
            path.update(data, self.account['idToken'])
            
            messagebox.showinfo("Success",f"Successfully saved your new credentials.")
            self.window.destroy()
            self.snapshot()