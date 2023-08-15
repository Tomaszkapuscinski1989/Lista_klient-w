from tkinter import *
import ttkbootstrap as ttb
from ttkbootstrap.constants import *
from tkinter import filedialog
from contextlib import contextmanager
from ttkbootstrap.dialogs import Messagebox
import sqlite3 as sq

import os

font_m = ("Times", "14")
font_d = ("Times", "18")
bgColor1 = "black"
bgColor2 = "white"
fgColor1 = bgColor1
fgColor2 = bgColor2


@contextmanager
def open_base(name):
    try:
        conn = sq.connect(name)
        c = conn.cursor()
        yield c
    finally:
        conn.commit()
        conn.close()


class Main(ttb.Window):
    def __init__(self, *args, **kwargs):
        ttb.Window.__init__(self, *args, **kwargs)
        self.nazwa_bazy = ""

        self.frame = Frame(self)
        self.frame.pack()

        label1 = ttb.Label(
            self.frame, text="Lista klientów ver 1.0", font=font_d, bootstyle="danger"
        )
        label1.pack()

        button1 = ttb.Button(self.frame, text="Nowa baza", bootstyle=SUCCESS)
        button1.pack(padx=5, pady=10)
        button1.bind("<Button-1>", self.nowa)
        button1.bind("<Return>", self.nowa)

        button2 = ttb.Button(
            self.frame, text="Wczytaj bazę", bootstyle=(SUCCESS, OUTLINE)
        )
        button2.pack(padx=5, pady=10)
        button2.bind("<Button-1>", self.wczytaj)
        button2.bind("<Return>", self.wczytaj)

        button3 = ttb.Button(self.frame, text="Zamknij", bootstyle=DANGER)
        button3.pack(padx=5, pady=10)
        button3.bind("<Button-1>", self.zamknij)
        button3.bind("<Return>", self.zamknij)

        # -----------------------------------------------------------

    def nowa(self, e):
        self.nazwa_bazy = filedialog.asksaveasfilename(
            defaultextension="*.db", filetypes=(("db", "*.db"),)
        )

        if self.nazwa_bazy:
            nazwa = self.nazwa_bazy.split("/")
            if os.path.exists(f"{nazwa[-1]}"):
                os.remove(f"{nazwa[-1]}")

        with open_base(self.nazwa_bazy) as c:
            c.execute(
                """CREATE TABLE company (
                    company_id INTIGER PRIMARY KEY,
                    company_name TEXT DEFAULT "NaN",
                    company_address TEXT DEFAULT "NaN",
                    website_address TEXT DEFAULT "NaN",
                    email_address TEXT DEFAULT "NaN",
                    phone_number INTEGER DEFAULT 0,
                    nip INTEGER DEFAULT 0,
                    regon INTEGER DEFAULT 0,
                    krs INTEGER DEFAULT 0,
                    info TEXT DEFAULT "NaN"
                    ) """
            )

        self.frame2()

    def wczytaj(self, e):
        self.nazwa_bazy = filedialog.askopenfilename(filetypes=(("db", "*.db"),))

        self.frame2()

    def zamknij(self, e):
        self.destroy()

        # --------------------------------------------------------------------------

    def frame2(self):

        for w in self.frame.winfo_children():
            w.destroy()

        label1 = ttb.Label(
            self.frame, text="Lista klientów ver 1.0", font=font_d, bootstyle="danger"
        )
        label1.grid(row=0, column=0, columnspan=2)

        columns = ("company_id", "company_name", "company_address")

        # Create Treeview
        self.my_tree = ttb.Treeview(
            self.frame, bootstyle="danger", columns=columns, show="headings"
        )
        self.my_tree.grid(row=1, column=0, rowspan=5)

        self.my_tree.bind("<ButtonRelease-1>", self.select_record)

        # Define headings
        self.my_tree.heading("company_id", text="ID")
        self.my_tree.heading("company_name", text="Nazwa firmy")
        self.my_tree.heading("company_address", text="Ades Firmy")

        self.TreeView()

        button4 = ttb.Button(self.frame, text="Dodaj", bootstyle=SUCCESS)
        button4.grid(row=1, column=1)
        button4.bind("<Button-1>", self.dodaj)
        button4.bind("<Return>", self.dodaj)

        button5 = ttb.Button(self.frame, text="Edytuj", bootstyle=SUCCESS)
        button5.grid(row=2, column=1)
        button5.bind("<Button-1>", self.edytuj)
        button5.bind("<Return>", self.edytuj)

        button6 = ttb.Button(self.frame, text="Szczeguły", bootstyle=SUCCESS)
        button6.grid(row=3, column=1)
        button6.bind("<Button-1>", self.more)
        button6.bind("<Return>", self.more)

        button7 = ttb.Button(self.frame, text="NaN", bootstyle=SUCCESS)
        button7.grid(row=4, column=1)
        button7.bind("<Button-1>", self.nowa)
        button7.bind("<Return>", self.nowa)

        button8 = ttb.Button(self.frame, text="Usuń", bootstyle=SUCCESS)
        button8.grid(row=5, column=1)
        button8.bind("<Button-1>", self.delate)
        button8.bind("<Return>", self.delate)

    def TreeView(self):

        for item in self.my_tree.get_children():
            self.my_tree.delete(item)

        with open_base(self.nazwa_bazy) as c:
            c.execute("SELECT * FROM company")
            w1 = c.fetchall()
        # Create Sample Data
        contacts = []

        for n in w1:
            contacts.append((f"{n[0]}", f"{n[1]}", f"{n[2]}"))

        # Add Data To Treeview
        for contact in contacts:
            self.my_tree.insert("", END, values=contact)

    def select_record(self, e):
        # Grab record Number
        selected = self.my_tree.focus()
        # Grab record values
        self.values = self.my_tree.item(selected, "values")

    def idNumber(self):
        with open_base(self.nazwa_bazy) as c:
            c.execute("SELECT * FROM company")
            w1 = c.fetchall()

        self.entryLabel.insert(0, len(w1) + 1)

    def w2(self, mode, tablica=[]):

        self.window2 = Toplevel()

        label2 = ttb.Label(
            self.window2, text="Nowy klient", font=font_d, bootstyle="danger"
        )
        label2.grid(row=0, column=0, columnspan=2)

        label3 = ttb.Label(self.window2, text="Id:", font=font_d, bootstyle="danger")
        label3.grid(row=2, column=0)

        self.entryLabel = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entryLabel.grid(row=2, column=1)

        label4 = ttb.Label(
            self.window2, text="Nazwa firmy:", font=font_d, bootstyle="danger"
        )
        label4.grid(row=3, column=0)

        self.entry1 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry1.grid(row=3, column=1)

        label5 = ttb.Label(
            self.window2, text="Adres firmy:", font=font_d, bootstyle="danger"
        )
        label5.grid(row=4, column=0)

        self.entry2 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry2.grid(row=4, column=1)

        label6 = ttb.Label(
            self.window2,
            text="Adres strony internetowej:",
            font=font_d,
            bootstyle="danger",
        )
        label6.grid(row=5, column=0)

        self.entry3 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry3.grid(row=5, column=1)

        label7 = ttb.Label(
            self.window2, text="Adres mail:", font=font_d, bootstyle="danger"
        )
        label7.grid(row=6, column=0)

        self.entry4 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry4.grid(row=6, column=1)

        label8 = ttb.Label(
            self.window2, text="Numer telefonu:", font=font_d, bootstyle="danger"
        )
        label8.grid(row=7, column=0)

        self.entry5 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry5.grid(row=7, column=1)

        label9 = ttb.Label(self.window2, text="NIP:", font=font_d, bootstyle="danger")
        label9.grid(row=8, column=0)

        self.entry6 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry6.grid(row=8, column=1)

        label10 = ttb.Label(
            self.window2, text="Regon:", font=font_d, bootstyle="danger"
        )
        label10.grid(row=9, column=0)

        self.entry7 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry7.grid(row=9, column=1)

        label11 = ttb.Label(self.window2, text="KRS:", font=font_d, bootstyle="danger")
        label11.grid(row=10, column=0)

        self.entry8 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry8.grid(row=10, column=1)

        label12 = ttb.Label(
            self.window2, text="Uwagi:", font=font_d, bootstyle="danger"
        )
        label12.grid(row=11, column=0)

        self.entry9 = ttb.Entry(self.window2, font=font_m, bootstyle="danger")
        self.entry9.grid(row=11, column=1)

        if mode == 2:
            button9 = ttb.Button(self.window2, text="Dodaj", bootstyle=SUCCESS)
            button9.grid(row=12, column=0, columnspan=2)
            button9.bind("<Button-1>", self.dodaj2)
            button9.bind("<Return>", self.dodaj2)

            self.idNumber()

        if mode == 1 or mode == 3:
            self.entryLabel.insert(0, tablica[0])
            self.entry1.insert(0, tablica[1])
            self.entry2.insert(0, tablica[2])
            self.entry3.insert(0, tablica[3])
            self.entry4.insert(0, tablica[4])
            self.entry5.insert(0, tablica[5])
            self.entry6.insert(0, tablica[6])
            self.entry7.insert(0, tablica[7])
            self.entry8.insert(0, tablica[8])
            self.entry9.insert(0, tablica[9])

        if mode == 3:

            button9 = ttb.Button(self.window2, text="Edytuj wpis", bootstyle=SUCCESS)
            button9.grid(row=12, column=0, columnspan=2)
            button9.bind("<Button-1>", self.edytuj2)
            button9.bind("<Return>", self.edytuj2)

    def dodaj(self, e):
        self.w2(2)

    def dodaj2(self, e):

        with open_base(self.nazwa_bazy) as c:
            c.execute(
                "INSERT INTO company (company_id, company_name, company_address, website_address, email_address, phone_number, nip, regon, krs, info) VALUES (:company_id, :company_name, :company_address, :website_address, :email_address, :phone_number, :nip, :regon, :krs, :info)",
                {
                    "company_id": self.entryLabel.get(),
                    "company_name": self.entry1.get(),
                    "company_address": self.entry2.get(),
                    "website_address": self.entry3.get(),
                    "email_address": self.entry4.get(),
                    "phone_number": self.entry5.get(),
                    "nip": self.entry6.get(),
                    "regon": self.entry7.get(),
                    "krs": self.entry8.get(),
                    "info": self.entry9.get(),
                },
            )

        self.TreeView()

        self.window2.destroy()

    def edytuj(self, e):
        try:
            with open_base(self.nazwa_bazy) as c:
                c.execute(
                    "SELECT oid, * FROM company where company_id=:oid", {"oid": self.values[0]}
                )
                r = c.fetchone()
                print(r)

            self.w2(3, r)

        except IndexError:
            Messagebox.show_error("Nie wybrano rekordu", "Błąd")

        except AttributeError:
            Messagebox.show_error("Nie wybrano rekordu", "Błąd")

        except:
            Messagebox.show_error("Nieznany Błąd", "Błąd")

    def edytuj2(self, e):
        with open_base(self.nazwa_bazy) as c:
            c.execute(
                "UPDATE company SET company_name=:company_name, company_address=:company_address, website_address=:website_address, email_address=:email_address, phone_number=:phone_number, nip=:nip, regon=:regon, krs=:krs, info=:info  WHERE company_id=:oid",
                {
                    "oid": self.values[0],
                    "company_name": self.entry1.get(),
                    "company_address": self.entry2.get(),
                    "website_address": self.entry3.get(),
                    "email_address": self.entry4.get(),
                    "phone_number": self.entry5.get(),
                    "nip": self.entry6.get(),
                    "regon": self.entry7.get(),
                    "krs": self.entry8.get(),
                    "info": self.entry9.get(),
                },
            )

        self.TreeView()
        self.window2.destroy()

    def more(self, e):
        try:
            with open_base(self.nazwa_bazy) as c:
                c.execute(
                    "SELECT * FROM company where company_id=:oid", {"oid": self.values[0]}
                )
                r = c.fetchone()

            self.w2(1, r)

        except IndexError:
            Messagebox.show_error("Nie wybrano rekordu", "Błąd")

        except AttributeError:
            Messagebox.show_error("Nie wybrano rekordu", "Błąd")

        except:
            Messagebox.show_error("Nieznany Błąd", "Błąd")


    def delate(self, e):
        try:
            with open_base(self.nazwa_bazy) as c:
                c.execute(
                    "DELETE FROM company where company_id=:oid", {"oid": self.values[0]}
                )

            self.TreeView()

        except IndexError:
            Messagebox.show_error("Nie wybrano rekordu", "Błąd")

        except AttributeError:
            Messagebox.show_error("Nie wybrano rekordu", "Błąd")

        except:
            Messagebox.show_error("Nieznany Błąd", "Błąd")


if __name__ == "__main__":

    start = Main(themename="superhero")
    start.mainloop()
