"""
Author: Jonathan Harjono
Date of Creation: 21 May 2020
Program Description: A GUI application for database management
Copyright 2020, Jonathan Harjono, all rights reserved.
"""

from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
from tkinter.messagebox import showerror, askquestion, showinfo
from datetime import datetime
import sqlite3
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import xlwt
import xlrd

informan = []
columnPicked = []
row_data = []
printColumn = []

class Error(Exception):
    '''Base class for other exceptions'''
    pass


class notFoundError(Error):
    '''Raised when data is not found'''
    pass


class Choice:
    def __init__(self):
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.master.geometry("1000x600")

        self.img = Image.open("Logo Elim.jpg") #logo
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)

        self.mode = IntVar()
        self.fontStyle = tkFont.Font(family="Helvetica", size=16) #font that will used for labels

        self.insert_button = Radiobutton(self.master, text="Insert", variable=self.mode, value=1, font=self.fontStyle)
        self.insert_button.grid(row=2, column=0, padx=40, sticky=W)

        self.search_button = Radiobutton(self.master, text="Search", variable=self.mode, value=2, font=self.fontStyle)
        self.search_button.grid(row=3, column=0, padx=40, sticky=W)

        self.edit_button = Radiobutton(self.master, text="Edit", variable=self.mode, value=3, font=self.fontStyle)
        self.edit_button.grid(row=4, column=0, padx=40, sticky=W)

        self.delete_button = Radiobutton(self.master, text="Delete", variable=self.mode, value=4, font=self.fontStyle)
        self.delete_button.grid(row=5, column=0, padx=40, sticky=W)

        self.sumbitButton = Button(self.master, text="Submit", command=self.checkMode)
        self.sumbitButton.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.quitButton = Button(self.master, text="Quit", command=self.quitExit)
        self.quitButton.grid(row=7, column=4, columnspan=2, pady=10, padx=10, ipadx=100)

        self.master.protocol("WM_DELETE_WINDOW", self.x_button) #overwrite the x button to show message window
        self.master.mainloop()

    def x_button(self):
        global mainmenu, keluar
        response = askquestion("Keluar program", "Yakin mau keluar program?")
        if response == "yes":
            keluar = True
            mainmenu = False
            self.closeWindow()

    def checkMode(self):
        global insert, search, edit, delete
        mode = self.mode.get()
        if mode == 1:
            print("Inner")
            insert = True
            self.closeWindow()
        elif mode == 2:
            search = True
            self.closeWindow()
        elif mode == 3:
            edit = True
            self.closeWindow()
        elif mode == 4:
            print("In4")
            delete = True
            self.closeWindow()
        else:
            showerror(title="Error", message="Tolong pilih mode")
            return

    def closeWindow(self):
        global mainmenu
        mainmenu = False
        self.master.destroy()

    def quitExit(self):
        global mainmenu, keluar
        mainmenu = False
        keluar = True
        self.master.destroy()


class Jemaat:
    def __init__(self):
        print("Jemaat")
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.master.geometry("1000x600")
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)

        dateNumber = []
        monthNumber = []
        for i in range(1, 32):
            dateNumber.append(i)

        for i in range(1, 13):
            monthNumber.append(i)

        self.tanggal = IntVar()
        self.bulan = IntVar()

        # Create text boxes
        self.name = Entry(self.master, width=30)
        self.name.grid(row=3, column=1, padx=20)

        self.date = OptionMenu(self.master, self.tanggal, *dateNumber)
        self.date.grid(row=4, column=1, padx=5)
        self.month = OptionMenu(self.master, self.bulan, *monthNumber)
        self.month.grid(row=5, column=1, padx=5)
        self.year = Entry(self.master, width=10)
        self.year.grid(row=6, column=1, padx=5)

        # Create labels for text boxes
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.name_label = Label(self.master, text="Nama lengkap", font=self.fontStyle)
        self.name_label.grid(row=3, column=0, padx=30, sticky=W)

        self.date_label = Label(self.master, text="Tanggal lahir", font=self.fontStyle)
        self.date_label.grid(row=4, column=0, padx=30, sticky=W)
        self.month_label = Label(self.master, text="Bulan lahir", font=self.fontStyle)
        self.month_label.grid(row=5, column=0, padx=30, sticky=W)
        self.year_label = Label(self.master, text="Tahun lahir", font=self.fontStyle)
        self.year_label.grid(row=6, column=0, padx=30, sticky=W)

        # Create submit button
        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.insertData)
        self.sumbitButton.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def insertData(self):
        global informan, database_file
        print(database_file)
        informan.clear()
        name = self.name.get().lower()
        date = self.tanggal.get()
        month = self.bulan.get()
        year = self.year.get()
        if self.checkAge(year):
            year = str(year)
            dob = str(date) + "/" + str(month) + "/" + str(year)
            inserting = [name, dob]
            informan.append(name)
            informan.append(dob)
            print("Year")
            # insert name to main table
            try:
                print("COnn")
                conn = sqlite3.connect(database_file)
                conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
                cursor = conn.cursor()  # creates cursor

                # Insert name to jemaat
                print("Inserting")
                insert_string = "INSERT INTO Jemaat(nama, `tanggal lahir`) VALUES(?, ?)"
                cursor.execute(insert_string, inserting)
                print("Done")
                conn.commit()

            except sqlite3.IntegrityError:
                global mainmenu, dewasa, anak, remaja
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                # Message box with error
                print("Error")
                showerror(title="Nama Error", message="Nama yang mau di masukan sudah ada di database")
                # Clear the textboxes
                self.name.delete(0, END)
                self.year.delete(0, END)

                mainmenu = True
                dewasa = False
                anak = False
                remaja = False

            except sqlite3.Error as err:
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                print("SQLite Error: %s" % err.args[0])
                sys.exit(-1)

            else:
                print("Passed")

            finally:
                if conn:
                    conn.close()
                self.closeWindow()

            # myEntry = Label(text=data)
            # myEntry.pack()
            # print("Finish pack")

        else:
            return

    def checkAge(self, tahun):
        global anak, remaja, dewasa, mainmenu
        print("Masuk")
        if not tahun.isdigit():
            showerror(title="Error Tahun", message="Tolong masukan angka untuk tahun")
            # mainmenu = True
            return False

        if len(tahun) != 4:
            showerror(title="Error Tahun", message="Tahun harus 4 angka")
            # mainmenu = True
            return False

        if tahun.isdigit() and len(tahun) == 4:
            year = datetime.today().year
            tahun = int(tahun)

            if (year - tahun) < 12:
                print("anak")
                anak = True
            elif 12 <= (year - tahun) < 20:
                print("remaja")
                remaja = True
            else:
                print("dewasa")
                dewasa = True
            return True

    def closeWindow(self):
        self.master.destroy()


class Anak:
    def __init__(self):
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.master.geometry("1000x600")
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        genders = ["P", "W"]

        self.tempat = StringVar()
        self.telpon = StringVar()
        self.kelamin = StringVar()
        self.ortu = StringVar()
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()
        self.skolah_minggu = StringVar()
        self.skolah_nama = StringVar()
        self.filename = StringVar()
        self.foto = ""
        self.photo_loc = ""

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        # Create Text Boxes
        self.tempat_lahir = Entry(self.master, width=30)
        self.tempat_lahir.grid(row=2, column=1, padx=5, sticky=W)
        self.alamat = Entry(self.master, width=30)
        self.alamat.grid(row=3, column=1, padx=5, sticky=W)
        self.telpon = Entry(self.master, width=30)
        self.telpon.grid(row=4, column=1, padx=5, sticky=W)
        self.gender = OptionMenu(self.master, self.kelamin, *genders)
        self.gender.grid(row=5, column=1)
        self.ortu = Entry(self.master, width=30)
        self.ortu.grid(row=6, column=1, padx=5, sticky=W)
        self.nama_skolah_minggu = Entry(self.master, width=30)
        self.nama_skolah_minggu.grid(row=7, column=1, padx=5, sticky=W)
        self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
        self.som1_button.grid(row=8, column=1, padx=20)
        self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
        self.som1_button2.grid(row=8, column=2, padx=20)

        self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
        self.som2_button.grid(row=9, column=1, padx=20)
        self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
        self.som2_button2.grid(row=9, column=2, padx=20)

        self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
        self.som3_button.grid(row=10, column=1, padx=20)
        self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
        self.som3_button2.grid(row=10, column=2, padx=20)
        self.skolah_nama = Entry(self.master, width=30)
        self.skolah_nama.grid(row=11, column=1, padx=5, sticky=W)

        # Create Label for text boxes
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=10)
        self.legend_label = Label(self.master, text="Kategori yang memiliki * adalah kategori wajib",
                                  font=self.fontStyle2)
        self.legend_label.grid(row=1, column=0, padx=5, sticky=W)
        self.tempat_lahir_label = Label(self.master, text="Tempat Lahir*", font=self.fontStyle)
        self.tempat_lahir_label.grid(row=2, column=0, padx=5, sticky=W)
        self.alamat_label = Label(self.master, text="Alamat*", font=self.fontStyle)
        self.alamat_label.grid(row=3, column=0, padx=5, sticky=W)
        self.telpon_label = Label(self.master, text="Nomor telpon", font=self.fontStyle)
        self.telpon_label.grid(row=4, column=0, padx=5, sticky=W)
        self.gender_label = Label(self.master, text="Jenis Kelamin", font=self.fontStyle)
        self.gender_label.grid(row=5, column=0, padx=5, sticky=W)
        self.ortu_label = Label(self.master, text="Nama orang tua*", font=self.fontStyle)
        self.ortu_label.grid(row=6, column=0, padx=5, sticky=W)
        self.nama_skolah_minggu_label = Label(self.master, text="Nama sekolah minggu", font=self.fontStyle)
        self.nama_skolah_minggu_label.grid(row=7, column=0, padx=5, sticky=W)
        self.som1_label = Label(self.master, text="Ikut SOM 1?", font=self.fontStyle)
        self.som1_label.grid(row=8, column=0, padx=5, sticky=W)
        self.som2_label = Label(self.master, text="Ikut SOM 2?", font=self.fontStyle)
        self.som2_label.grid(row=9, column=0, padx=5, sticky=W)
        self.som3_label = Label(self.master, text="Ikut SOM 3?", font=self.fontStyle)
        self.som3_label.grid(row=10, column=0, padx=5, sticky=W)
        self.skolah_nama_label = Label(self.master, text="Nama Sekolah?", font=self.fontStyle)
        self.skolah_nama_label.grid(row=11, column=0, padx=5, sticky=W)

        # self.print_button = Button(self.master, text="Print nama foto", command=self.printPhoto)
        # self.print_button.pack()
        # Upload photo & submit button
        self.gettingphoto_button = Button(self.master, text="Click untuk masukan photo*", font=self.fontStyle,
                                          command=self.uploadAction)
        self.gettingphoto_button.grid(row=14, column=2, columnspan=2, pady=10, padx=10, ipadx=10)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.insertData)
        self.sumbitButton.grid(row=14, column=0, columnspan=2, pady=10, padx=10, ipadx=10)

        self.master.grid_rowconfigure(1, minsize=20)

        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def insertData(self):
        global informan, database_file
        inserting = []
        nama = informan[0]
        tanggal_lahir = informan[1]
        inserting.append(nama)
        inserting.append(tanggal_lahir)

        # Getting values to store to variables
        tempat = str(self.tempat_lahir.get().lower())
        address = str(self.alamat.get().lower())
        telpon = str(self.telpon.get())
        gender = str(self.kelamin.get())
        ortu = str(self.ortu.get().lower())
        nama_skolah_minggu = str(self.nama_skolah_minggu.get().lower())
        skolah_nama = str(self.skolah_nama.get().lower())
        photo_name = str(self.photo_loc)
        print("A")
        print(os.path.dirname(os.path.abspath("jemaatElim.db")))
        print(photo_name)
        # Check required entry
        if tempat == "" or address == "" or ortu == "":
            showerror(title="Textbox wajib kosong", message="Tolong isi data wajib")
            return

        if photo_name == "" or photo_name == os.path.dirname(os.path.abspath("jemaatElim.db")):
            photo_insert = ""
        else:
            # Getting photo to variable
            with open(photo_name, 'rb') as pic:
                photo_insert = pic.read()

        # inserting to list to insert
        inserting.append(tempat)
        inserting.append(address)
        inserting.append(telpon)
        inserting.append(gender)
        inserting.append(ortu)
        inserting.append(nama_skolah_minggu)

        if self.som1.get() == 2:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        if self.som2.get() == 4:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        if self.som3.get() == 6:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        inserting.append(skolah_nama)
        inserting.append(photo_insert)

        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            # Insert name to Anak
            insert_string = "INSERT INTO Anak(nama, `tanggal lahir`, `tempat lahir`, alamat, `nomor telpon`," \
                            "`jenis kelamin`, ortu, `nama sekolah minggu`, `SOM 1`, `SOM 2`, `SOM 3`, `nama sekolah`," \
                            "photo) " \
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_string, inserting)
            conn.commit()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")

        finally:
            if conn:
                conn.close()

            informan.clear()
            self.closeWindow()

        # myEntry = Label(text=data)
        # myEntry.pack()
        # print("Finish pack")

    def uploadAction(self):
        file = filedialog.askopenfilename()  # opens file dialog
        self.filename = file  # saves the file location/name
        self.photo_loc = os.path.abspath(file)
        filename = self.filename[::-1]
        name_of_pic = ""

        for i in filename:
            if i == "/":
                break
            name_of_pic += i

        self.foto = name_of_pic


class Remaja:
    def __init__(self):
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        genders = ["P", "W"]
        status_pel = ["Sudah", "Belum, tapi bersedia", "Belum, dan belum bersedia"]

        self.alamat = StringVar()
        self.tempat = StringVar()
        self.telpon = StringVar()
        self.kelamin = StringVar()
        self.kelamin.set(genders[0])
        self.ortu = StringVar()
        self.sudah_baptisan = StringVar()
        self.sudah_baptisan.set(status_pel[2])
        self.tanggal_baptis = StringVar()
        self.sudah_pelayanan = StringVar()
        self.sudah_pelayanan.set(status_pel[2])
        self.jenis_pel = StringVar()
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()
        self.som1.set(3)
        self.som2.set(5)
        self.som3.set(7)
        self.sudah_gabung_komisi = StringVar()
        self.sudah_gabung_komisi.set(status_pel[2])
        self.nama_komisi = StringVar()
        self.sudah_gabung_jdm = StringVar()
        self.sudah_gabung_jdm.set(status_pel[2])
        self.nama_jdm = StringVar()
        self.filename = StringVar()
        self.foto = ""
        self.photo_loc = ""

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        # Create Text Boxes
        self.tempat_lahir = Entry(self.master, width=30)
        self.tempat_lahir.grid(row=3, column=1, padx=20)
        self.alamat = Entry(self.master, width=30)
        self.alamat.grid(row=4, column=1, padx=20)
        self.telpon = Entry(self.master, width=30)
        self.telpon.grid(row=5, column=1, padx=20)
        self.gender = OptionMenu(self.master, self.kelamin, *genders)
        self.gender.grid(row=6, column=1)
        self.ortu = Entry(self.master, width=30)
        self.ortu.grid(row=7, column=1, padx=20)
        self.sudah_baptis = OptionMenu(self.master, self.sudah_baptisan, *status_pel)
        self.sudah_baptis.grid(row=8, column=1)
        self.tanggal_baptis = Entry(self.master, width=30)
        self.tanggal_baptis.grid(row=9, column=1)
        self.sudah_pel = OptionMenu(self.master, self.sudah_pelayanan, *status_pel)
        self.sudah_pel.grid(row=10, column=1)
        self.jenis_pel = Entry(self.master, width=30)
        self.jenis_pel.grid(row=11, column=1, padx=20)

        self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
        self.som1_button.grid(row=12, column=1, padx=20)
        self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
        self.som1_button2.grid(row=12, column=2, padx=20)

        self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
        self.som2_button.grid(row=13, column=1, padx=20)
        self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
        self.som2_button2.grid(row=13, column=2, padx=20)

        self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
        self.som3_button.grid(row=14, column=1, padx=20)
        self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
        self.som3_button2.grid(row=14, column=2, padx=20)
        self.gabung_komisi = OptionMenu(self.master, self.sudah_gabung_komisi, *status_pel)
        self.gabung_komisi.grid(row=15, column=1)
        self.komisi_nama = Entry(self.master, width=30)
        self.komisi_nama.grid(row=16, column=1, padx=20)

        # Create Label for text boxes
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.tempat_lahir_label = Label(self.master, text="Tempat Lahir", font=self.fontStyle)
        self.tempat_lahir_label.grid(row=3, column=0, padx=7, sticky=W)
        self.alamat_label = Label(self.master, text="Alamat*", font=self.fontStyle)
        self.alamat_label.grid(row=4, column=0, padx=7, sticky=W)
        self.telpon_label = Label(self.master, text="Nomor telpon", font=self.fontStyle)
        self.telpon_label.grid(row=5, column=0, padx=7, sticky=W)
        self.gender_label = Label(self.master, text="Jenis Kelamin*", font=self.fontStyle)
        self.gender_label.grid(row=6, column=0, padx=7, sticky=W)
        self.ortu_label = Label(self.master, text="Nama orang tua*", font=self.fontStyle)
        self.ortu_label.grid(row=7, column=0, padx=7, sticky=W)
        self.sudah_baptis_label = Label(self.master, text="Sudah dibaptis?*", font=self.fontStyle)
        self.sudah_baptis_label.grid(row=8, column=0, padx=7, sticky=W)
        self.tanggal_baptis_label = Label(self.master, text="Kalau sudah, tolong masukan tanggal dibaptis?",
                                          font=self.fontStyle)
        self.tanggal_baptis_label.grid(row=9, column=0, padx=7, sticky=W)
        self.sudah_pel_label = Label(self.master, text="Sudah Pelayanan?*", font=self.fontStyle)
        self.sudah_pel_label.grid(row=10, column=0, padx=7, sticky=W)
        self.jenis_pel_label = Label(self.master, text="Kalau sudah, tolong masukan jenis Pelayanan",
                                     font=self.fontStyle)
        self.jenis_pel_label.grid(row=11, column=0, padx=7, sticky=W)
        self.som1_button_label = Label(self.master, text="Sudah ikut SOM 1?", font=self.fontStyle)
        self.som1_button_label.grid(row=12, column=0, padx=7, sticky=W)
        self.som2_button_label = Label(self.master, text="Sudah ikut SOM 2?", font=self.fontStyle)
        self.som2_button_label.grid(row=13, column=0, padx=7, sticky=W)
        self.som3_button_label = Label(self.master, text="Sudah ikut SOM 3?", font=self.fontStyle)
        self.som3_button_label.grid(row=14, column=0, padx=7, sticky=W)
        self.gabung_komisi_label = Label(self.master, text="Sudah gabung komisi?", font=self.fontStyle)
        self.gabung_komisi_label.grid(row=15, column=0, padx=7, sticky=W)
        self.nama_komisi_label = Label(self.master, text="Nama komisi?", font=self.fontStyle)
        self.nama_komisi_label.grid(row=16, column=0, padx=7, sticky=W)

        # Upload photo & submit button
        self.gettingphoto_button = Button(self.master, text="Click untuk masukan photo*", command=self.uploadAction)
        self.gettingphoto_button.grid(row=19, column=1, columnspan=2, pady=10, padx=10, ipadx=100)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.insertData)
        self.sumbitButton.grid(row=20, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.master.grid_rowconfigure(1, minsize=20)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def insertData(self):
        global informan, database_file
        inserting = []
        nama = informan[0]
        tanggal_lahir = informan[1]
        inserting.append(nama)
        inserting.append(tanggal_lahir)

        # Getting values to store to variables
        tempat = str(self.tempat_lahir.get())
        address = str(self.alamat.get())
        telpon = str(self.telpon.get())
        gender = str(self.kelamin.get())
        ortu = str(self.ortu.get())
        sudah_baptis = str(self.sudah_baptisan.get())
        tanggal_baptis = str(self.tanggal_baptis.get())
        sudah_pelayanan = str(self.sudah_pelayanan.get())
        jenis_pelayanan = str(self.jenis_pel.get())
        gabung_komisi = str(self.sudah_gabung_komisi.get())
        nama_komisi = str(self.komisi_nama.get())
        photo_name = str(self.photo_loc)

        # Check required entry
        if address == "":
            showerror(title="Textbox wajib kosong", message="Tolong isi data wajib")
            return

        if photo_name == "" or photo_name == os.path.dirname(os.path.abspath("jemaatElim.db")):
            photo_insert = ""
        else:
            # Getting photo to variable
            with open(photo_name, 'rb') as pic:
                photo_insert = pic.read()

        # inserting to list to insert
        inserting.append(tempat)
        inserting.append(address)
        inserting.append(telpon)
        inserting.append(gender)
        inserting.append(ortu)
        inserting.append(sudah_baptis)
        inserting.append(tanggal_baptis)
        inserting.append(sudah_pelayanan)
        inserting.append(jenis_pelayanan)

        if self.som1.get() == 2:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        if self.som2.get() == 4:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        if self.som3.get() == 6:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        inserting.append(gabung_komisi)
        inserting.append(nama_komisi)
        inserting.append(photo_insert)

        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            # Insert name to Remaja
            insert_string = "INSERT INTO Remaja(nama, `tanggal lahir`, `tempat lahir`, alamat, `nomor telpon`, " \
                            "`jenis kelamin`, ortu, `sudah baptis`, `tanggal baptis`, `sudah pelayanan`, " \
                            "`jenis pelayanan`, `SOM 1`, `SOM 2`, `SOM 3`, `gabung komisi`, `nama komisi`, " \
                            "photo) " \
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_string, inserting)
            conn.commit()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")

        finally:
            if conn:
                conn.close()

            informan.clear()
            self.closeWindow()

        # myEntry = Label(text=data)
        # myEntry.pack()
        # print("Finish pack")

    def uploadAction(self):
        file = filedialog.askopenfilename()  # opens file dialog
        self.filename = file  # saves the file location/name
        self.photo_loc = os.path.abspath(file)
        filename = self.filename[::-1]
        name_of_pic = ""

        for i in filename:
            if i == "/":
                break
            name_of_pic += i

        self.foto = name_of_pic


class Dewasa:
    def __init__(self):
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        genders = ["P", "W"]
        status = ["Lajang", "Menikah", "Cerai Hidup/Mati"]
        status_pel = ["Sudah", "Belum, tapi bersedia", "Belum, dan belum bersedia"]

        self.alamat = StringVar()
        self.tempat = StringVar()
        self.telpon = StringVar()
        self.kelamin = StringVar()
        self.kelamin.set(genders[0])
        self.ortu = StringVar()
        self.sudah_bap = StringVar()
        self.sudah_bap.set(status_pel[2])
        self.tanggal_baptis = StringVar()
        self.sudah_pelayan = StringVar()
        self.sudah_pelayan.set(status_pel[2])
        self.jenis_pel = StringVar()
        self.anggota = StringVar()
        self.anggota.set(status_pel[2])
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()
        self.som1.set(3)
        self.som2.set(5)
        self.som3.set(7)
        self.gabung_komi = StringVar()
        self.gabung_komi.set(status_pel[2])
        self.nama_komisi = StringVar()
        self.gabung_jdmm = StringVar()
        self.gabung_jdmm.set(status_pel[2])
        self.nama_jdm = StringVar()
        self.nikah = StringVar()
        self.nikah.set(status[0])
        self.filename = StringVar()
        self.sosial_member = IntVar()
        self.sosial_member.set(3)
        self.foto = ""
        self.photo_loc = ""

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        # Create Text Boxes for personal info
        self.tempat_lahir = Entry(self.master, width=20)
        self.tempat_lahir.grid(row=3, column=1, padx=7)
        self.alamat = Entry(self.master, width=20)
        self.alamat.grid(row=4, column=1, padx=7)
        self.telpon = Entry(self.master, width=20)
        self.telpon.grid(row=5, column=1, padx=7)
        self.gender = OptionMenu(self.master, self.kelamin, *genders)
        self.gender.grid(row=6, column=1)
        self.job = Entry(self.master, width=20)
        self.job.grid(row=7, column=1)
        self.status_nikah = OptionMenu(self.master, self.nikah, *status)
        self.status_nikah.grid(row=8, column=1)
        self.ortu = Entry(self.master, width=30)
        self.ortu.grid(row=9, column=1, padx=7)
        self.pasangan = Entry(self.master, width=30)
        self.pasangan.grid(row=10, column=1, padx=7)

        self.anak1_nama = Entry(self.master, width=30)
        self.anak1_umur = Entry(self.master, width=5)
        self.anak1_nama.grid(row=11, column=1, padx=7)
        self.anak1_umur.grid(row=11, column=3, padx=7)

        self.anak2_nama = Entry(self.master, width=30)
        self.anak2_umur = Entry(self.master, width=5)
        self.anak2_nama.grid(row=12, column=1, padx=7)
        self.anak2_umur.grid(row=12, column=3, padx=7)

        self.anak3_nama = Entry(self.master, width=30)
        self.anak3_umur = Entry(self.master, width=5)
        self.anak3_nama.grid(row=13, column=1, padx=7)
        self.anak3_umur.grid(row=13, column=3, padx=7)

        self.anak4_nama = Entry(self.master, width=30)
        self.anak4_umur = Entry(self.master, width=5)
        self.anak4_nama.grid(row=14, column=1, padx=7)
        self.anak4_umur.grid(row=14, column=3, padx=7)

        self.anak5_nama = Entry(self.master, width=30)
        self.anak5_umur = Entry(self.master, width=5)
        self.anak5_nama.grid(row=15, column=1, padx=7)
        self.anak5_umur.grid(row=15, column=3, padx=7)

        # Create text boxes for Church Info
        self.member = OptionMenu(self.master, self.anggota, *status_pel)
        self.member.grid(row=3, column=7, padx=7)
        self.sudah_baptis = OptionMenu(self.master, self.sudah_bap, *status_pel)
        self.sudah_baptis.grid(row=4, column=7)
        self.tanggal_baptis = Entry(self.master, width=30)
        self.tanggal_baptis.grid(row=5, column=7)
        self.sudah_pel = OptionMenu(self.master, self.sudah_pelayan, *status_pel)
        self.sudah_pel.grid(row=6, column=7)
        self.jenis_pel = Entry(self.master, width=30)
        self.jenis_pel.grid(row=7, column=7, padx=7)

        self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
        self.som1_button.grid(row=8, column=7, padx=7)
        self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
        self.som1_button2.grid(row=8, column=8, padx=7)

        self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
        self.som2_button.grid(row=9, column=7, padx=7)
        self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
        self.som2_button2.grid(row=9, column=8, padx=7)

        self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
        self.som3_button.grid(row=10, column=7, padx=7)
        self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
        self.som3_button2.grid(row=10, column=8, padx=7)
        self.gabung_komisi = OptionMenu(self.master, self.gabung_komi, *status_pel)
        self.gabung_komisi.grid(row=11, column=7)
        self.komisi_nama = Entry(self.master, width=30)
        self.komisi_nama.grid(row=12, column=7, padx=7)
        self.gabung_jdm = OptionMenu(self.master, self.gabung_jdmm, *status_pel)
        self.gabung_jdm.grid(row=13, column=7)
        self.nama_jdm = Entry(self.master, width=30)
        self.nama_jdm.grid(row=14, column=7, padx=7)
        self.sosial_mati_member = Radiobutton(self.master, text="Sudah", variable=self.sosial_member, value=2)
        self.sosial_mati_member.grid(row=15, column=7, padx=7)
        self.sosial_mati_member2 = Radiobutton(self.master, text="Belum", variable=self.sosial_member, value=3)
        self.sosial_mati_member2.grid(row=15, column=8, padx=7)

        # Create Label for text boxes personal info
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.tempat_lahir_label = Label(self.master, text="Tempat Lahir", font=self.fontStyle)
        self.tempat_lahir_label.grid(row=3, column=0)
        self.alamat_label = Label(self.master, text="Alamat*", font=self.fontStyle)
        self.alamat_label.grid(row=4, column=0)
        self.telpon_label = Label(self.master, text="Nomor telpon", font=self.fontStyle)
        self.telpon_label.grid(row=5, column=0)
        self.gender_label = Label(self.master, text="Jenis Kelamin", font=self.fontStyle)
        self.gender_label.grid(row=6, column=0)
        self.job_label = Label(self.master, text="Pekerjaan", font=self.fontStyle)
        self.job_label.grid(row=7, column=0)
        self.status_nikah_label = Label(self.master, text="Status nikah", font=self.fontStyle)
        self.status_nikah_label.grid(row=8, column=0)
        self.ortu_label = Label(self.master, text="Nama orang tua", font=self.fontStyle)
        self.ortu_label.grid(row=9, column=0)
        self.pasangan_label = Label(self.master, text="Nama suami/istri", font=self.fontStyle)
        self.pasangan_label.grid(row=10, column=0)
        self.son1name_label = Label(self.master, text="Nama anak pertama", font=self.fontStyle)
        self.son1age_label = Label(self.master, text="Umur")
        self.son1name_label.grid(row=11, column=0)
        self.son1age_label.grid(row=11, column=2)

        self.son2name_label = Label(self.master, text="Nama anak kedua", font=self.fontStyle)
        self.son2age_label = Label(self.master, text="Umur")
        self.son2name_label.grid(row=12, column=0)
        self.son2age_label.grid(row=12, column=2)

        self.son3name_label = Label(self.master, text="Nama anak ketiga", font=self.fontStyle)
        self.son3age_label = Label(self.master, text="Umur")
        self.son3name_label.grid(row=13, column=0)
        self.son3age_label.grid(row=13, column=2)

        self.son4name_label = Label(self.master, text="Nama anak keempat", font=self.fontStyle)
        self.son4age_label = Label(self.master, text="Umur")
        self.son4name_label.grid(row=14, column=0)
        self.son4age_label.grid(row=14, column=2)

        self.son5name_label = Label(self.master, text="Nama anak kelima", font=self.fontStyle)
        self.son5age_label = Label(self.master, text="Umur")
        self.son5name_label.grid(row=15, column=0)
        self.son5age_label.grid(row=15, column=2)

        # Create Label for text box Church info
        self.member_label = Label(self.master, text="Sudah anggota?*", font=self.fontStyle)
        self.member_label.grid(row=3, column=6)
        self.sudah_baptis_label = Label(self.master, text="Sudah dibaptis?*", font=self.fontStyle)
        self.sudah_baptis_label.grid(row=4, column=6)
        self.tanggal_baptis_label = Label(self.master, text="Tanggal dibaptis?",
                                          font=self.fontStyle)
        self.tanggal_baptis_label.grid(row=5, column=6)
        self.sudah_pel_label = Label(self.master, text="Sudah Pelayanan?*", font=self.fontStyle)
        self.sudah_pel_label.grid(row=6, column=6)
        self.jenis_pel_label = Label(self.master, text="Jenis Pelayanan",
                                     font=self.fontStyle)
        self.jenis_pel_label.grid(row=7, column=6)
        self.som1_button_label = Label(self.master, text="Sudah ikut SOM 1?", font=self.fontStyle)
        self.som1_button_label.grid(row=8, column=6)
        self.som2_button_label = Label(self.master, text="Sudah ikut SOM 2?", font=self.fontStyle)
        self.som2_button_label.grid(row=9, column=6)
        self.som3_button_label = Label(self.master, text="Sudah ikut SOM 3?", font=self.fontStyle)
        self.som3_button_label.grid(row=10, column=6)
        self.gabung_komisi_label = Label(self.master, text="Sudah gabung komisi?*", font=self.fontStyle)
        self.gabung_komisi_label.grid(row=11, column=6)
        self.nama_komisi_label = Label(self.master, text="Nama komisi?", font=self.fontStyle)
        self.nama_komisi_label.grid(row=12, column=6)
        self.gabung_jdm_label = Label(self.master, text="Sudah gabung JDM?*", font=self.fontStyle)
        self.gabung_jdm_label.grid(row=13, column=6)
        self.nama_jdm_label = Label(self.master, text="Nama JDM?", font=self.fontStyle)
        self.nama_jdm_label.grid(row=14, column=6)
        self.sosial_mati_member_label = Label(self.master, text="Sudah jadi anggota sosial mati?*", font=self.fontStyle)
        self.sosial_mati_member_label.grid(row=15, column=6)

        # Upload photo & submit button
        self.gettingphoto_button = Button(self.master, text="Click untuk masukan photo*", font=self.fontStyle,
                                          command=self.uploadAction)
        self.gettingphoto_button.grid(row=17, column=6, columnspan=2, pady=10, padx=10, ipadx=100)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.insertData)
        self.sumbitButton.grid(row=17, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        self.master.grid_columnconfigure(5, minsize=200)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def insertData(self):
        global informan, database_file
        inserting = []

        nama = informan[0]
        tanggal_lahir = informan[1]
        inserting.append(nama)
        inserting.append(tanggal_lahir)

        # Getting values to store to variables
        photo_name = str(self.photo_loc)

        # Check required entry
        if self.alamat.get() == "":
            showerror(title="Textbox wajib kosong", message="Tolong isi data wajib")
            return

        if photo_name == "" or photo_name == os.path.dirname(os.path.abspath("jemaatElim.db")):
            photo_insert = ""
        else:
            # Getting photo to variable
            with open(photo_name, 'rb') as pic:
                photo_insert = pic.read()

        # inserting to list to insert
        inserting.append(str(self.tempat_lahir.get().lower()))
        inserting.append(str(self.alamat.get().lower()))
        inserting.append(str(self.telpon.get()))
        inserting.append(str(self.kelamin.get().lower()))
        inserting.append(str(self.job.get().lower()))
        inserting.append(str(self.nikah.get().lower()))
        inserting.append(str(self.ortu.get().lower()))
        inserting.append(str(self.pasangan.get().lower()))
        inserting.append(str(self.anak1_nama.get().lower()))
        inserting.append(str(self.anak1_umur.get()))
        inserting.append(str(self.anak2_nama.get().lower()))
        inserting.append(str(self.anak2_umur.get()))
        inserting.append(str(self.anak3_nama.get().lower()))
        inserting.append(str(self.anak3_umur.get()))
        inserting.append(str(self.anak4_nama.get().lower()))
        inserting.append(str(self.anak4_umur.get()))
        inserting.append(str(self.anak5_nama.get().lower()))
        inserting.append(str(self.anak5_umur.get()))
        inserting.append(str(self.anggota.get().lower()))
        inserting.append(str(self.sudah_bap.get()))
        inserting.append(str(self.tanggal_baptis.get()))
        inserting.append(str(self.sudah_pelayan.get()))
        inserting.append(str(self.jenis_pel.get().lower()))

        if self.som1.get() == 2:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        if self.som2.get() == 4:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        if self.som3.get() == 6:
            print("Ikut")
            inserting.append("sudah")
        else:
            print("Belum")
            inserting.append("belum")

        inserting.append(str(self.gabung_komi.get()))
        inserting.append(str(self.komisi_nama.get().lower()))
        inserting.append(str(self.gabung_jdmm.get()))
        inserting.append(str(self.nama_jdm.get().lower()))
        print(self.sosial_member)
        if self.sosial_member.get() == 2:
            inserting.append("sudah")
        else:
            inserting.append("belum")

        inserting.append(photo_insert)

        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            # Insert name to Dewasa
            insert_string = "INSERT INTO Dewasa(nama, `tanggal lahir`, `tempat lahir`, alamat, `nomor telpon`, " \
                            "`jenis kelamin`, pekerjaan, `status nikah`, ortu, `nama suami/istri`, " \
                            "`nama anak pertama`, `umur anak pertama`, `nama anak kedua`, `umur anak kedua`, " \
                            "`nama anak ketiga`, `umur anak ketiga`, `nama anak keempat`, `umur anak keempat`, " \
                            "`nama anak kelima`, `umur anak kelima`, anggota, `sudah dibaptis`,  " \
                            "`tanggal dibaptis`, `sudah pelayanan`, `jenis pelayanan`, `SOM 1`, `SOM 2`, `SOM 3`, " \
                            "`gabung komisi`, `nama komisi`, `gabung jdm`, `nama jdm`, `anggota sosial mati`, photo) " \
                            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?," \
                            "?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(insert_string, inserting)
            conn.commit()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")

        finally:
            if conn:
                conn.close()

            informan.clear()
            self.closeWindow()

    def uploadAction(self):
        file = filedialog.askopenfilename()  # opens file dialog
        self.filename = file  # saves the file location/name
        self.photo_loc = os.path.abspath(file)  # saves the path of the photo file to a variable


class Search:
    def __init__(self):
        global search_name, search_jdm, search_komisi, search_som
        search_name = False
        search_jdm = False
        search_som = False
        search_komisi = False
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=13)
        self.mode_label = Label(self.master, text="Kategori apa saja yang mau dicari?", font=self.fontStyle2)
        self.mode_label.grid(row=1, column=0, padx=5, pady=5)

        # Check mode
        self.mode = IntVar()
        self.search_by_name_button = Radiobutton(self.master, text="Cari dengan nama", variable=self.mode, value=2,
                                                 font=self.fontStyle)
        self.search_by_name_button.grid(row=3, column=0, padx=40, sticky=W)

        self.search_by_jdm_button = Radiobutton(self.master, text="Cari dengan JDM", variable=self.mode, value=3,
                                                font=self.fontStyle)
        self.search_by_jdm_button.grid(row=4, column=0, padx=40, sticky=W)

        self.search_by_komisi_button = Radiobutton(self.master, text="Cari dengan komisi", variable=self.mode, value=4,
                                                   font=self.fontStyle)
        self.search_by_komisi_button.grid(row=5, column=0, padx=40, sticky=W)

        self.search_by_som_button = Radiobutton(self.master, text="Cari dengan SOM", variable=self.mode, value=5,
                                                font=self.fontStyle)
        self.search_by_som_button.grid(row=6, column=0, padx=40, sticky=W)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.check_mode)
        self.sumbitButton.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)

        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        self.master.destroy()

    def check_mode(self):
        print("In show")
        global search_name, search_jdm, search_komisi, search_som
        mode = self.mode.get()
        if mode == 2:
            print("Inner")
            search_name = True
            self.closeWindow()
        elif mode == 3:
            search_jdm = True
            self.closeWindow()
        elif mode == 4:
            search_komisi = True
            self.closeWindow()
        elif mode == 5:
            print("In4")
            search_som = True
            self.closeWindow()
        else:
            showerror(title="Error", message="Tolong pilih mode")
            return


class SearchName:
    def __init__(self):
        global database_file
        self.columnnames = []
        self.checkbox_list = []
        self.checkbox_choice = []
        self.checkbox_box = []
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        self.box = None
        self.var = IntVar()
        self.table_name = ""
        self.select_statement = ""
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=13)
        self.mode_label = Label(self.master, text="Kategori apa saja yang mau dicari?", font=self.fontStyle2)
        self.mode_label.grid(row=1, column=0, padx=5, pady=5)

        # Create text box for the search
        self.name = Entry(self.master, width=20)
        self.name.grid(row=3, column=1, padx=7)

        self.name_label = Label(self.master, text="Nama", font=self.fontStyle)
        self.name_label.grid(row=3, column=0, padx=7, sticky=W)

        self.showCategoryButton = Button(self.master, text="Tunjukan kategori", font=self.fontStyle,
                                         command=self.show_categories)
        self.showCategoryButton.grid(row=19, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.searchName)
        self.sumbitButton.grid(row=20, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def checkAge(self, tahun):
        year = datetime.today().year
        tahun = int(tahun)
        if (year - tahun) < 12:
            print("anak")
            return "anak"
        elif 12 <= (year - tahun) < 20:
            print("remaja")
            return "remaja"
        else:
            print("dewasa")
            return "dewasa"

    def showErrorMessage(self):
        showerror(title="No name", message="Nama yang mau dicari tidak ada di database")
        self.name.delete(0, END)
        for i in self.checkbox_list:
            if i.winfo_exists():
                i.grid_forget()

    def show_categories(self):
        # Look what table the name is in and make checkbox of the categories of the table
        if len(self.checkbox_box) != 0:
            self.columnnames.clear()
            for i in self.checkbox_box:
                i.destroy()
        else:
            pass

        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            # Search through jemaat for the dob to determine age
            search_string = "SELECT `tanggal lahir` FROM Jemaat WHERE nama LIKE ?"
            name = self.name.get() + '%'
            print(name)
            cursor.execute(search_string, (name,))
            number = cursor.fetchone()

            if number is None:
                print("Error")
                self.showErrorMessage()
                return

            else:
                print(number)
                for i in number:
                    nomor = i
                print(nomor)

                self.table_name = self.checkAge(nomor[-4:])

                if self.table_name == "anak":
                    cursor.execute("SELECT * FROM Anak")
                    colnames = cursor.description

                    index = 2
                    # Get the column names and put it into a list
                    for row in colnames:
                        self.columnnames.append(row[0])

                    self.columnnames.pop()
                    self.columnnames.pop(0)
                    # Print out the checkbox
                    index = 1
                    self.master.grid_columnconfigure(3, minsize=200)
                    for category in self.columnnames:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=4, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1

                elif self.table_name == "remaja":
                    cursor.execute("SELECT * FROM Remaja")
                    colnames = cursor.description
                    # Get the column names and put it into a dictionary
                    for row in colnames:
                        self.columnnames.append(row[0])
                    self.columnnames.pop()
                    self.columnnames.pop(0)
                    # Print out the checkbox
                    index = 1
                    col = 4
                    make_new_column = False
                    self.master.grid_columnconfigure(3, minsize=200)
                    self.master.grid_columnconfigure(4, minsize=200)

                    for category in self.columnnames:
                        if make_new_column:
                            self.var = IntVar()
                            self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                            self.box.grid(row=index, column=col, sticky=W)
                            self.checkbox_choice.append(self.var)
                            self.checkbox_box.append(self.box)
                            index += 1
                        else:
                            self.var = IntVar()
                            self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                            self.box.grid(row=index, column=col, sticky=W)
                            self.checkbox_choice.append(self.var)
                            self.checkbox_box.append(self.box)
                            index += 1
                            if index > 14:
                                index = 1
                                make_new_column = True
                                col += 1

                elif self.table_name == "dewasa":
                    cursor.execute("SELECT * FROM Dewasa")
                    colnames = cursor.description
                    # Get the column names and put it into a dictionary
                    for row in colnames:
                        self.columnnames.append(row[0])
                    self.columnnames.pop(0)
                    self.columnnames.pop()
                    # Print out the checkbox
                    index = 1
                    col = 4
                    make_new_column = False
                    self.master.grid_columnconfigure(3, minsize=200)
                    for category in self.columnnames:
                        if make_new_column:
                            self.var = IntVar()
                            self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                            self.box.grid(row=index, column=col, sticky=W)
                            self.checkbox_choice.append(self.var)
                            self.checkbox_box.append(self.box)
                            index += 1
                            if index > 14:
                                make_new_column = True
                                index = 1
                                col += 1
                        else:
                            self.var = IntVar()
                            self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                            self.box.grid(row=index, column=col, sticky=W)
                            self.checkbox_choice.append(self.var)
                            self.checkbox_box.append(self.box)
                            index += 1
                            if index > 14:
                                make_new_column = True
                                index = 1
                                col += 1

                conn.commit()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")

        finally:
            if conn:
                conn.close()

    def searchName(self):
        global informan, show, columnPicked
        informan.clear()
        print("Searching")
        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            picked_category = []

            # Search through jemaat for the dob to determine age
            search_string = "SELECT `tanggal lahir` FROM Jemaat WHERE nama LIKE ?"
            name = self.name.get() + '%'
            print(name)
            cursor.execute(search_string, (name,))
            number = cursor.fetchone()

            if number is None:
                self.showErrorMessage()
                return

            else:
                print(number)
                for i in number:
                    nomor = i
                print(nomor)

                self.table_name = self.checkAge(nomor[-4:])

            if len(self.checkbox_choice) == 0:
                search_string = "SELECT * FROM " + self.table_name + " WHERE nama LIKE ?"
                print("Check")
                informan.append(search_string)
                informan.append(name)
                informan.append(self.table_name)

                cursor.execute("SELECT * FROM " + self.table_name)
                colnames = cursor.description
                for row in colnames:
                    columnPicked.append(row[0])

                # Eliminates ID and photo from the column options
                columnPicked.pop(0)
                columnPicked.pop()
                print("POCKET")

            else:
                # Getting the checkbox choices
                for i in range(len(self.checkbox_choice)):
                    if self.checkbox_choice[i].get() == 1:
                        category_name = "`" + self.columnnames[i] + "`"
                        picked_category.append(category_name)

                # Creating the query string
                search_string = "SELECT "
                for i in range(len(picked_category)):
                    search_string += picked_category[i]
                    search_string += ', '

                search_string = search_string.rstrip(" ")
                self.select_statement = search_string.rstrip(',')
                self.select_statement += " FROM " + self.table_name
                self.select_statement += " WHERE nama LIKE ?"
                informan.append(self.select_statement)
                informan.append(name)
                informan.append(self.table_name)
                columnPicked = picked_category

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")
            show = True
            self.closeWindow()

        finally:
            if conn:
                conn.close()


class SearchJDM:
    def __init__(self):
        global database_file
        self.columnnames = []
        self.checkbox_list = []
        self.checkbox_choice = []
        self.checkbox_box = []
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        self.box = None
        self.var = IntVar()
        self.table_name = ""
        self.select_statement = ""
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=13)
        self.mode_label = Label(self.master, text="Kategori apa saja yang mau dicari?", font=self.fontStyle2)
        self.mode_label.grid(row=1, column=0, padx=5, pady=5)

        # Create text box for the search
        self.jdm = Entry(self.master, width=20)
        self.jdm.grid(row=3, column=1, padx=7)

        self.jdm_label = Label(self.master, text="Nama JDM", font=self.fontStyle)
        self.jdm_label.grid(row=3, column=0, padx=7, sticky=W)

        self.showCategoryButton = Button(self.master, text="Tunjukan kategori", font=self.fontStyle,
                                         command=self.show_categories)
        self.showCategoryButton.grid(row=19, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.searchjdm)
        self.sumbitButton.grid(row=20, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):  # overrides the x button
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def showErrorMessage(self):
        showerror(title="No name", message="Tidak ada yang ikut JDM ini di database")
        self.jdm.delete(0, END)
        for i in self.checkbox_list:
            if i.winfo_exists():
                i.grid_forget()

    def show_categories(self):
        if len(self.checkbox_box) != 0:
            self.columnnames.clear()
            for i in self.checkbox_box:
                i.destroy()
        else:
            pass
        # Look what table the name is in and make checkbox of the categories of the table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            search_string = "SELECT * FROM Dewasa WHERE `nama jdm` = ?"
            cursor.execute(search_string, (self.jdm.get(),))
            colnames = cursor.description
            index = 1
            # Get the column names and put it into a dictionary
            for row in colnames:
                self.columnnames.append(row[0])

            # Print out the checkbox
            index = 1
            col = 4
            make_new_column = False
            self.master.grid_columnconfigure(3, minsize=200)
            for category in self.columnnames:
                if make_new_column:
                    self.var = IntVar()
                    self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                    self.box.grid(row=index, column=col, sticky=W)
                    self.checkbox_choice.append(self.var)
                    self.checkbox_box.append(self.box)
                    index += 1
                    if index > 14:
                        make_new_column = True
                        index = 1
                        col += 1
                else:
                    self.var = IntVar()
                    self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                    self.box.grid(row=index, column=col, sticky=W)
                    self.checkbox_choice.append(self.var)
                    self.checkbox_box.append(self.box)
                    index += 1
                    if index > 14:
                        make_new_column = True
                        index = 1
                        col += 1

            conn.commit()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")

        finally:
            if conn:
                conn.close()

    def searchjdm(self):
        global informan, show, columnPicked, database_file
        informan.clear()
        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            picked_category = []
            print("Before")

            if len(self.checkbox_choice) == 0:
                self.table_name = "Dewasa"
                search_string = "SELECT * FROM " + self.table_name + " WHERE `nama jdm` = ?"
                print(search_string)
                informan.append(search_string)
                informan.append(self.jdm.get())
                informan.append(self.table_name)

                cursor.execute("SELECT * FROM " + self.table_name)
                colnames = cursor.description
                for row in colnames:
                    columnPicked.append(row[0])

                columnPicked.pop(0)
                columnPicked.pop()

            else:
                for i in range(len(self.checkbox_choice)):
                    if self.checkbox_choice[i].get() == 1:
                        category_name = "`" + self.columnnames[i] + "`"
                        picked_category.append(category_name)

                search_string = "SELECT "
                for i in range(len(picked_category)):
                    search_string += picked_category[i]
                    search_string += ', '

                search_string = search_string.rstrip(" ")
                self.select_statement = search_string.rstrip(',')
                self.select_statement += " FROM " + self.table_name
                self.select_statement += " WHERE nama = ?"
                informan.append(self.select_statement)
                informan.append(self.name.get())
                informan.append(self.table_name)
                columnPicked = picked_category

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")
            show = True
            self.closeWindow()

        finally:
            if conn:
                conn.close()


class SearchKomisi:
    def __init__(self):
        global search_name, search_jdm, search_komisi, search_som, database_file
        self.columnnames = []
        self.checkbox_list = []
        self.checkbox_choice = []
        self.checkbox_box = []
        search_name = False
        search_jdm = False
        search_som = False
        search_komisi = False
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        self.box = None
        self.var = IntVar()
        self.table_name = ""
        self.select_statement = ""
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=13)
        self.mode_label = Label(self.master, text="Kategori apa saja yang mau dicari?", font=self.fontStyle2)
        self.mode_label.grid(row=1, column=0, padx=5, pady=5)

        # Create text box for the search
        self.komisi = Entry(self.master, width=20)
        self.komisi.grid(row=3, column=1, padx=7)

        self.komisi_label = Label(self.master, text="Nama komisi", font=self.fontStyle)
        self.komisi_label.grid(row=3, column=0, padx=7, sticky=W)

        # Radio button for determining age group
        self.mode = IntVar()
        self.remaja_button = Radiobutton(self.master, text="Remaja", variable=self.mode, value=2,
                                         font=self.fontStyle)
        self.remaja_button.grid(row=3, column=3, padx=40, sticky=W)

        self.dewasa_button = Radiobutton(self.master, text="Dewasa", variable=self.mode, value=3,
                                         font=self.fontStyle)
        self.dewasa_button.grid(row=4, column=3, padx=40, sticky=W)

        self.showCategoryButton = Button(self.master, text="Tunjukan kategori", font=self.fontStyle,
                                         command=self.show_categories)
        self.showCategoryButton.grid(row=19, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.searchkomisi)
        self.sumbitButton.grid(row=20, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):  # overrides the x button
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def showErrorMessage(self):
        showerror(title="No name", message="Nama yang mau dicari tidak ada di database")
        self.jdm.delete(0, END)
        for i in self.checkbox_list:
            if i.winfo_exists():
                i.grid_forget()

    def checkmode(self):
        if self.mode.get() == 2:
            return "remaja"
        elif self.mode.get() == 3:
            return "dewasa"

    def show_categories(self):
        if len(self.checkbox_box) != 0:
            self.columnnames.clear()
            for i in self.checkbox_box:
                i.destroy()
        else:
            pass
        # Look what table the name is in and make checkbox of the categories of the table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            print("check")
            self.table_name = self.checkmode()

            if self.table_name == "dewasa":
                search_string = "SELECT * FROM Dewasa WHERE `nama komisi` = ?"
                cursor.execute(search_string, (self.komisi.get().lower(),))
                colnames = cursor.description
                index = 1
                # Get the column names and put it into a dictionary
                for row in colnames:
                    self.columnnames.append(row[0])
                self.columnnames.pop(0)

                # Print out the checkbox
                index = 1
                col = 4
                make_new_column = False
                self.master.grid_columnconfigure(3, minsize=200)
                for category in self.columnnames:
                    if make_new_column:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                        if index > 14:
                            make_new_column = True
                            index = 1
                            col += 1
                    else:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                        if index > 14:
                            make_new_column = True
                            index = 1
                            col += 1

            elif self.table_name == "remaja":
                search_string = "SELECT * FROM Remaja WHERE `nama komisi` = ?"
                cursor.execute(search_string, (self.komisi.get().lower(),))
                colnames = cursor.description
                index = 1
                # Get the column names and put it into a dictionary
                for row in colnames:
                    self.columnnames.append(row[0])
                self.columnnames.pop(0)
                self.columnnames.pop()
                # Print out the checkbox
                index = 1
                col = 4
                make_new_column = False
                self.master.grid_columnconfigure(3, minsize=200)
                self.master.grid_columnconfigure(4, minsize=200)

                for category in self.columnnames:
                    if make_new_column:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                    else:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                        if index > 14:
                            index = 1
                            make_new_column = True
                            col += 1

            conn.commit()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")

        finally:
            if conn:
                conn.close()

    def searchkomisi(self):
        global informan, show, columnPicked
        informan.clear()
        print("Searching")

        self.table_name = self.checkmode().capitalize()
        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            picked_category = []
            print("Before")

            # Search for komisi to check if it is in the table
            search_string = "SELECT `nama komisi` FROM " + self.table_name + " WHERE `nama komisi` = ?"
            cursor.execute(search_string, (self.komisi.get().lower(),))
            number = cursor.fetchone()

            if number is None:
                self.showErrorMessage()
                return

            if len(self.checkbox_choice) == 0:
                search_string = "SELECT * FROM " + self.table_name + " WHERE `nama komisi` = ?"
                informan.append(search_string)
                informan.append(self.komisi.get().lower())
                informan.append(self.table_name)

                cursor.execute("SELECT * FROM " + self.table_name)
                colnames = cursor.description
                for row in colnames:
                    columnPicked.append(row[0])

                columnPicked.pop(0)
                columnPicked.pop()

            else:
                zeroes = True
                for i in range(len(self.checkbox_choice)):
                    if self.checkbox_choice[i].get() != 0:
                        zeroes = False

                if not zeroes:
                    for i in range(len(self.checkbox_choice)):
                        if self.checkbox_choice[i].get() == 1:
                            category_name = "`" + self.columnnames[i] + "`"
                            picked_category.append(category_name)

                    search_string = "SELECT "
                    for i in range(len(picked_category)):
                        search_string += picked_category[i]
                        search_string += ', '

                    search_string = search_string.rstrip(" ")
                    self.select_statement = search_string.rstrip(',')
                    self.select_statement += " FROM " + self.table_name
                    self.select_statement += " WHERE `nama komisi` = ?"
                    informan.append(self.select_statement)
                    informan.append(self.komisi.get().lower())
                    informan.append(self.table_name)
                    columnPicked = picked_category

                elif zeroes:
                    search_string = "SELECT * FROM " + self.table_name + " WHERE `nama komisi` = ?"
                    informan.append(search_string)
                    informan.append(self.komisi.get().lower())
                    informan.append(self.table_name)
                    columnPicked = picked_category

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")
            show = True
            self.closeWindow()

        finally:
            if conn:
                conn.close()


class SearchSOM:
    def __init__(self):
        global search_name, search_jdm, search_komisi, search_som, database_file
        self.columnnames = []
        self.checkbox_list = []
        self.checkbox_choice = []
        self.checkbox_box = []
        search_name = False
        search_jdm = False
        search_som = False
        search_komisi = False
        print("Search")
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        self.box = None
        self.var = IntVar()
        self.table_name = ""
        self.select_statement = ""
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=13)
        self.mode_label = Label(self.master, text="Kategori apa saja yang mau dicari?", font=self.fontStyle2)
        self.mode_label.grid(row=1, column=0, padx=5, pady=5)

        # Radio button for determining age group
        self.mode = IntVar()
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()

        self.som_choice = []
        self.anak_button = Radiobutton(self.master, text="Anak", variable=self.mode, value=2, font=self.fontStyle)
        self.anak_button.grid(row=3, column=1, padx=40, sticky=W)
        self.remaja_button = Radiobutton(self.master, text="Remaja", variable=self.mode, value=3,
                                         font=self.fontStyle)
        self.remaja_button.grid(row=4, column=1, padx=40, sticky=W)

        self.dewasa_button = Radiobutton(self.master, text="Dewasa", variable=self.mode, value=4,
                                         font=self.fontStyle)
        self.dewasa_button.grid(row=5, column=1, padx=40, sticky=W)

        self.ikut_som1 = Checkbutton(self.master, text="Ikut SOM 1", variable=self.som1, font=self.fontStyle2)
        self.ikut_som1.grid(row=3, column=2, padx=40, sticky=W)
        self.som_choice.append(self.som1)

        self.ikut_som2 = Checkbutton(self.master, text="Ikut SOM 2", variable=self.som2, font=self.fontStyle2)
        self.ikut_som2.grid(row=4, column=2, padx=40, sticky=W)
        self.som_choice.append(self.som2)

        self.ikut_som3 = Checkbutton(self.master, text="Ikut SOM 3", variable=self.som3, font=self.fontStyle2)
        self.ikut_som3.grid(row=5, column=2, padx=40, sticky=W)
        self.som_choice.append(self.som3)

        self.showCategoryButton = Button(self.master, text="Tunjukan kategori", font=self.fontStyle,
                                         command=self.show_categories)
        self.showCategoryButton.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.searchsom)
        self.sumbitButton.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def showErrorMessage(self):
        showerror(title="No name", message="Tolong pilih SOM apa yang mau dicari")
        for i in self.checkbox_list:
            if i.winfo_exists():
                i.grid_forget()
        return

    def checkmode(self):
        if self.mode.get() == 2:
            return "anak"
        elif self.mode.get() == 3:
            return "remaja"
        elif self.mode.get() == 4:
            return "dewasa"

    def show_categories(self):
        if len(self.checkbox_box) != 0:
            self.columnnames.clear()
            for i in self.checkbox_box:
                i.destroy()
        else:
            pass
        # Look what table the name is in and make checkbox of the categories of the table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            self.table_name = self.checkmode()

            if self.table_name == "anak":
                cursor.execute("SELECT * FROM Anak")
                colnames = cursor.description

                # Get the column names and put it into a list
                for row in colnames:
                    self.columnnames.append(row[0])

                self.columnnames.pop()
                self.columnnames.pop(0)
                # Print out the checkbox
                index = 1
                self.master.grid_columnconfigure(3, minsize=200)
                for category in self.columnnames:
                    self.var = IntVar()
                    self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                    self.box.grid(row=index, column=4, sticky=W)
                    self.checkbox_choice.append(self.var)
                    index += 1

            elif self.table_name == "remaja":
                search_string = "SELECT * FROM Remaja"
                cursor.execute(search_string)
                colnames = cursor.description
                # Get the column names and put it into a dictionary
                for row in colnames:
                    self.columnnames.append(row[0])

                self.columnnames.pop()
                self.columnnames.pop(0)
                # Print out the checkbox
                index = 1
                col = 4
                make_new_column = False
                self.master.grid_columnconfigure(3, minsize=200)
                self.master.grid_columnconfigure(4, minsize=200)

                for category in self.columnnames:
                    if make_new_column:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                    else:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                        if index > 14:
                            index = 1
                            make_new_column = True
                            col += 1

            elif self.table_name == "dewasa":
                search_string = "SELECT * FROM Dewasa"
                cursor.execute(search_string)
                colnames = cursor.description
                # Get the column names and put it into a dictionary
                for row in colnames:
                    self.columnnames.append(row[0])

                self.columnnames.pop(0)
                self.columnnames.pop()
                # Print out the checkbox
                index = 1
                col = 4
                make_new_column = False
                self.master.grid_columnconfigure(3, minsize=200)
                for category in self.columnnames:
                    if make_new_column:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                        if index > 14:
                            make_new_column = True
                            index = 1
                            col += 1
                    else:
                        self.var = IntVar()
                        self.box = Checkbutton(self.master, text=category, variable=self.var, font=self.fontStyle)
                        self.box.grid(row=index, column=col, sticky=W)
                        self.checkbox_choice.append(self.var)
                        self.checkbox_box.append(self.box)
                        index += 1
                        if index > 14:
                            make_new_column = True
                            index = 1
                            col += 1

            conn.commit()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")

        finally:
            if conn:
                conn.close()

    def searchsom(self):
        global informan, show, columnPicked
        informan.clear()
        print("Searching")
        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            picked_category = []
            print("Before")

            self.table_name = self.checkmode()
            som1 = self.som_choice[0].get()
            som2 = self.som_choice[1].get()
            som3 = self.som_choice[2].get()

            if len(self.checkbox_choice) == 0:  # No specific categories are picked
                if som3 == 1:  # Have taken SOM 3
                    search_string = "SELECT * FROM " + self.table_name + " WHERE `SOM 3` = ?"
                    informan.append(search_string)
                    informan.append('sudah')
                    informan.append(self.table_name)

                    cursor.execute(search_string, ('sudah',))
                    colnames = cursor.description
                    for row in colnames:
                        columnPicked.append(row[0])

                    columnPicked.pop(0)
                    columnPicked.pop()

                elif som2 == 1:  # Have taken SOM 2
                    search_string = "SELECT * FROM " + self.table_name + " WHERE `SOM 2` = ?"
                    informan.append(search_string)
                    informan.append('sudah')
                    informan.append(self.table_name)

                    cursor.execute(search_string, ('sudah',))
                    colnames = cursor.description
                    for row in colnames:
                        columnPicked.append(row[0])

                    columnPicked.pop(0)
                    columnPicked.pop()

                elif som1 == 1:  # Have taken SOM 1
                    search_string = "SELECT * FROM " + self.table_name + " WHERE `SOM 1` = ?"
                    informan.append(search_string)
                    informan.append('sudah')
                    informan.append(self.table_name)

                    cursor.execute(search_string, ('sudah',))
                    colnames = cursor.description
                    for row in colnames:
                        columnPicked.append(row[0])

                    columnPicked.pop(0)
                    columnPicked.pop()

                else:
                    self.showErrorMessage()
                    return

            else:
                som1 = self.som_choice[0].get()
                som2 = self.som_choice[1].get()
                som3 = self.som_choice[2].get()

                for i in range(len(self.checkbox_choice)):
                    if self.checkbox_choice[i].get() == 1:
                        category_name = "`" + self.columnnames[i] + "`"
                        picked_category.append(category_name)

                search_string = "SELECT "
                for i in range(len(picked_category)):
                    search_string += picked_category[i]
                    search_string += ', '

                search_string = search_string.rstrip(" ")
                self.select_statement = search_string.rstrip(',')
                self.select_statement += " FROM " + self.table_name

                if som3 == 1:
                    self.select_statement += " WHERE `SOM 3` = ?"
                    informan.append(self.select_statement)
                    informan.append('sudah')
                    informan.append(self.table_name)
                    columnPicked = picked_category
                elif som2 == 1:
                    self.select_statement += " WHERE `SOM 2` = ?"
                    informan.append(self.select_statement)
                    informan.append('sudah')
                    informan.append(self.table_name)
                    columnPicked = picked_category
                elif som1 == 1:
                    self.select_statement += " WHERE `SOM 1` = ?"
                    informan.append(self.select_statement)
                    informan.append('sudah')
                    informan.append(self.table_name)
                    columnPicked = picked_category

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")
            show = True
            self.closeWindow()

        finally:
            if conn:
                conn.close()


class ShowResults:  # Don't forget to implement a to_print button that makes an excel file to print the data
    def showingPhoto(self):
        global informan
        # get photo from the last entry of row from query
        # cut off the last entry
        # show photo here
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            select_string = "SELECT photo FROM " + informan[2] + " WHERE nama LIKE ?"  # SQL query to get photo
            cursor.execute(select_string, (informan[1],))

            foto = cursor.fetchone()  # Get photo from sqlite db
            photo = foto[0]  # Get the data of the photo stored in db
            name_of_person = informan[1].strip() + ".jpg"  # Make the filename

            with open(name_of_person, "wb") as out_foto:  # Creates the picture file
                out_foto.write(photo)

            image = Image.open(name_of_person)
            image.show()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])
            sys.exit(-1)

        finally:
            if conn:
                conn.close()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def __init__(self):
        global informan, columnPicked, row_data, database_file, printColumn
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.tree = None
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.minsize(1000, 600)
        self._setup_widget()

        # Search and print result
        try:
            global informan
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            # Search data
            search_string = informan[0]
            name = informan[1]
            cursor.execute(search_string, (name,))
            row = cursor.fetchone()
            while row:
                row_no_photo = []
                for i in range(len(row)):
                    row_no_photo.append(row[i])

                if len(row_no_photo) == len(columnPicked):
                    new_row = []
                    tuple_photo = tuple(row_no_photo)
                    new_row.append(tuple_photo)
                    row_data.append(new_row[0])

                    for col in columnPicked:
                        self.tree.heading(col, text=col.title(), command=lambda c=col: sortby(self.tree, c, 0))
                        self.tree.column(col, width=tkFont.Font().measure(col.title()))

                    for item in new_row:
                        self.tree.insert('', 'end', values=item)
                        # adjust column's width if necessary to fit each value
                        for ix, val in enumerate(item):
                            col_w = tkFont.Font().measure(val)
                            if self.tree.column(columnPicked[ix], width=None) < col_w:
                                self.tree.column(columnPicked[ix], width=col_w)

                    row = cursor.fetchone()
                else:
                    row_no_photo.pop(0)
                    row_no_photo.pop()
                    new_row = []
                    tuple_photo = tuple(row_no_photo)
                    new_row.append(tuple_photo)
                    row_data.append(new_row[0])

                    for col in columnPicked:
                        self.tree.heading(col, text=col.title(), command=lambda c=col: sortby(self.tree, c, 0))
                        self.tree.column(col, width=tkFont.Font().measure(col.title()))

                    for item in new_row:
                        self.tree.insert('', 'end', values=item)
                        # adjust column's width if necessary to fit each value
                        for ix, val in enumerate(item):
                            col_w = tkFont.Font().measure(val)
                            if self.tree.column(columnPicked[ix], width=None) < col_w:
                                self.tree.column(columnPicked[ix], width=col_w)
                    row = cursor.fetchone()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])
            sys.exit(-1)
        else:
            for pick in columnPicked:
                printColumn.append(pick)
            columnPicked.clear()
        finally:
            if conn:
                conn.close()

        self.master.mainloop()

    def show_message(self):
        showinfo(title="File Excel sudah dibuat", message="File Excel untuk di print sudah dibuat")
        return

    def printResult(self): # make excel file so result can be printed
        global row_data, printColumn
        print("Col")
        print(printColumn)
        print("row")
        print(row_data)

        workbook = xlrd.open_workbook('elim_print.xls')
        c = workbook.sheet_by_index(0)
        cell_data = c.cell(0, 0).value
        if cell_data is not None:
            file_path = os.getcwd() + "\elim_print.xls"
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                print("Can not delete the file as it doesn't exists")
        else:
            pass

        book = xlwt.Workbook('elim_print.xls')
        sheet1 = book.add_sheet("Sheet 1", cell_overwrite_ok=True)

        i = 0
        for col in printColumn:  # put the column header
            sheet1.write(0, i, col)
            i += 1

        index = 1
        berikut = 0
        for data in row_data:
            for inside in range(len(data)):
                cwidth = sheet1.col(inside).width
                if (len(data[inside]) * 367) > cwidth:
                    sheet1.col(inside).width = (
                                len(data[inside]) * 367)  # (Modify column width to match biggest data in that column)
                sheet1.write(index, berikut, data[inside])
                berikut += 1
            index += 1
            berikut = 0

        book.save("elim_print.xls")
        self.show_message()
        row_data.clear()
        printColumn.clear()

    def _setup_widget(self):
        global columnPicked
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # Scrollbar
        self.tree = ttk.Treeview(columns=columnPicked, show="headings")
        scrollbar_vert = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        scorllbar_hori = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_vert.set, xscrollcommand=scorllbar_hori.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        scrollbar_vert.grid(row=0, column=1, sticky='ns', in_=container)
        scorllbar_hori.grid(row=1, column=0, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.print_result = Button(self.master, text="Print hasil", command=self.printResult)
        self.print_result.pack(side=BOTTOM)
        self.show_photo = Button(self.master, text="Show photo", command=self.showingPhoto)
        self.show_photo.pack(side=BOTTOM)


class Edit:
    def __init__(self):
        self.columnnames = []
        self.checkbox_list = []
        self.checkbox_choice = []
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.width = self.master.winfo_screenwidth()
        self.height = self.master.winfo_screenheight()
        self.master.geometry("1000x600")
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        self.box = None
        self.var = IntVar()
        self.table_name = ""
        self.select_statement = ""
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=13)
        self.mode_label = Label(self.master, text="Kategori apa saja yang mau diganti?", font=self.fontStyle2)
        self.mode_label.grid(row=1, column=0, padx=5, pady=5)
        #self.master.rowconfigure(4, minsize=300)
        # Create text box for the search
        self.name = Entry(self.master, width=20)
        self.name.grid(row=3, column=1, padx=5)

        self.name_label = Label(self.master, text="Nama", font=self.fontStyle)
        self.name_label.grid(row=3, column=0, padx=5, sticky=W)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.edit_data)
        self.sumbitButton.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def checkAge(self, tahun):
        year = datetime.today().year
        tahun = int(tahun)
        if (year - tahun) < 12:
            print("anak")
            return "anak"
        elif 12 <= (year - tahun) < 20:
            print("remaja")
            return "remaja"
        else:
            print("dewasa")
            return "dewasa"

    def showErrorMessage(self):
        showerror(title="No name", message="Nama yang mau diganti tidak ada di database")
        self.name.delete(0, END)
        for i in self.checkbox_list:
            if i.winfo_exists():
                i.grid_forget()

    def edit_data(self):
        global informan, show, columnPicked, anak, remaja, dewasa, database_file
        informan.clear()
        if self.name.get() == "":
            showerror(title="Error", message="Tolong masukan nama")
            return
        print("Searching")
        # insert name to main table
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            picked_category = []
            print("Before")

            # Search through jemaat for the dob to determine age
            search_string = "SELECT `tanggal lahir` FROM Jemaat WHERE nama LIKE ?"
            name = self.name.get().lower() + '%'
            print(name)
            cursor.execute(search_string, (name,))
            number = cursor.fetchone()

            if number is None:
                self.showErrorMessage()
                return

            else:
                print(number)
                for i in number:
                    nomor = i
                print(nomor)

                self.table_name = self.checkAge(nomor[-4:])

            informan.append(self.name.get().lower())
            if self.table_name == "anak":
                print("Anak")
                anak = True

            elif self.table_name == "remaja":
                print("Remaja")
                remaja = True

            elif self.table_name == "dewasa":
                print("Dewasa")
                dewasa = True

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        else:
            print("Passed")
            show = True
            self.closeWindow()

        finally:
            if conn:
                conn.close()


class UpdateAnak:
    def __init__(self):
        print("Edit")
        global informan, database_file
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.master.geometry("1000x600")
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        genders = ["P", "W"]

        self.tempat = StringVar()
        self.telpon = StringVar()
        self.kelamin = StringVar()
        self.ortu = StringVar()
        self.skolah_minggu = StringVar()
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()
        self.skolah_nama = StringVar()
        self.filename = StringVar()
        self.foto = ""
        self.photo_loc = ""

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)

        # Query to get initial values for text box to be edited
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            get_data_string = "SELECT * FROM Anak WHERE nama LIKE ?"
            cursor.execute(get_data_string, (informan[0],))
            row = cursor.fetchone()

            while row:
                new_row = []
                for i in range(len(row)):
                    new_row.append(row[i])

                row = cursor.fetchone()

            new_row.pop(0)
            new_row.pop(0)
            new_row.pop(0)
            new_row.pop()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        finally:
            if conn:
                conn.close()

        if new_row[6] == "belum":
            set_som1 = False
        else:
            set_som1 = True

        if new_row[7] == "belum":
            set_som2 = False
        else:
            set_som2 = True

        if new_row[8] == "belum":
            set_som3 = False
        else:
            set_som3 = True

        self.kelamin.set(new_row[3])
        # Create Text Boxes
        self.tempat_lahir = Entry(self.master, width=30)
        self.tempat_lahir.insert(END, new_row[0])
        self.tempat_lahir.grid(row=2, column=1, padx=5, sticky=W)
        self.alamat = Entry(self.master, width=30)
        self.alamat.insert(END, new_row[1])
        self.alamat.grid(row=3, column=1, padx=5, sticky=W)
        self.telpon = Entry(self.master, width=30)
        self.telpon.insert(END, new_row[2])
        self.telpon.grid(row=4, column=1, padx=5, sticky=W)
        self.gender = OptionMenu(self.master, self.kelamin, *genders)
        self.gender.grid(row=5, column=1)
        self.ortu = Entry(self.master, width=30)
        self.ortu.insert(END, new_row[4])
        self.ortu.grid(row=6, column=1, padx=5, sticky=W)
        self.nama_skolah_minggu = Entry(self.master, width=30)
        self.nama_skolah_minggu.insert(END, new_row[5])
        self.nama_skolah_minggu.grid(row=7, column=1, padx=5, sticky=W)

        if set_som1:
            self.som1.set(2)
            self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
            self.som1_button.grid(row=8, column=1, padx=20)
            self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
            self.som1_button2.grid(row=8, column=2, padx=20)
        else:
            self.som1.set(3)
            self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
            self.som1_button.grid(row=8, column=1, padx=20)
            self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
            self.som1_button2.grid(row=8, column=2, padx=20)

        if set_som2:
            self.som2.set(4)
            self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
            self.som2_button.grid(row=9, column=1, padx=20)
            self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
            self.som2_button2.grid(row=9, column=2, padx=20)
        else:
            self.som2.set(5)
            self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
            self.som2_button.grid(row=9, column=1, padx=20)
            self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
            self.som2_button2.grid(row=9, column=2, padx=20)

        if set_som3:
            self.som3.set(6)
            self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
            self.som3_button.grid(row=10, column=1, padx=20)
            self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
            self.som3_button2.grid(row=10, column=2, padx=20)
        else:
            self.som3.set(7)
            self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
            self.som3_button.grid(row=10, column=1, padx=20)
            self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
            self.som3_button2.grid(row=10, column=2, padx=20)

        self.skolah_nama = Entry(self.master, width=30)
        self.skolah_nama.insert(END, new_row[9])
        self.skolah_nama.grid(row=11, column=1, padx=5, sticky=W)

        # Create Label for text boxes
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=10)
        self.legend_label = Label(self.master, text="Kategori yang memiliki * adalah kategori wajib",
                                  font=self.fontStyle2)
        self.legend_label.grid(row=1, column=0, padx=5, sticky=W)
        self.tempat_lahir_label = Label(self.master, text="Tempat Lahir*", font=self.fontStyle)
        self.tempat_lahir_label.grid(row=2, column=0, padx=5, sticky=W)
        self.alamat_label = Label(self.master, text="Alamat*", font=self.fontStyle)
        self.alamat_label.grid(row=3, column=0, padx=5, sticky=W)
        self.telpon_label = Label(self.master, text="Nomor telpon", font=self.fontStyle)
        self.telpon_label.grid(row=4, column=0, padx=5, sticky=W)
        self.gender_label = Label(self.master, text="Jenis Kelamin", font=self.fontStyle)
        self.gender_label.grid(row=5, column=0, padx=5, sticky=W)
        self.ortu_label = Label(self.master, text="Nama orang tua*", font=self.fontStyle)
        self.ortu_label.grid(row=6, column=0, padx=5, sticky=W)
        self.nama_skolah_minggu_label = Label(self.master, text="Nama sekolah minggu", font=self.fontStyle)
        self.nama_skolah_minggu_label.grid(row=7, column=0, padx=5, sticky=W)
        self.som1_label = Label(self.master, text="Ikut SOM 1?", font=self.fontStyle)
        self.som1_label.grid(row=8, column=0, padx=5, sticky=W)
        self.som2_label = Label(self.master, text="Ikut SOM 2?", font=self.fontStyle)
        self.som2_label.grid(row=9, column=0, padx=5, sticky=W)
        self.som3_label = Label(self.master, text="Ikut SOM 3?", font=self.fontStyle)
        self.som3_label.grid(row=10, column=0, padx=5, sticky=W)
        self.skolah_nama_label = Label(self.master, text="Nama Sekolah?", font=self.fontStyle)
        self.skolah_nama_label.grid(row=11, column=0, padx=5, sticky=W)

        # self.print_button = Button(self.master, text="Print nama foto", command=self.printPhoto)
        # self.print_button.pack()
        # Upload photo & submit button
        self.gettingphoto_button = Button(self.master, text="Click untuk masukan photo*", font=self.fontStyle,
                                          command=self.uploadAction)
        self.gettingphoto_button.grid(row=14, column=2, columnspan=2, pady=10, padx=10, ipadx=10)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.editData)
        self.sumbitButton.grid(row=14, column=0, columnspan=2, pady=10, padx=10, ipadx=10)

        self.master.grid_rowconfigure(1, minsize=20)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def editData(self):
        global informan
        inserting = []
        nama = informan[0]

        if self.photo_loc == "":
            # Getting values to store to variables
            tempat = str(self.tempat_lahir.get().lower())
            address = str(self.alamat.get().lower())
            telpon = str(self.telpon.get())
            gender = str(self.kelamin.get())
            ortu = str(self.ortu.get().lower())
            nama_skolah_minggu = str(self.nama_skolah_minggu.get().lower())
            skolah_nama = str(self.skolah_nama.get().lower())
            # photo_name = str(self.photo_loc)

            # Check required entry
            if tempat == "" or address == "" or ortu == "":
                showerror(title="Textbox wajib kosong", message="Tolong isi data wajib")
                return

            # inserting to list to insert
            inserting.append(tempat)
            inserting.append(address)
            inserting.append(telpon)
            inserting.append(gender)
            inserting.append(ortu)
            inserting.append(nama_skolah_minggu)

            if self.som1.get() == 2:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som2.get() == 4:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som3.get() == 6:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            inserting.append(skolah_nama)
            # inserting.append(photo_insert)
            print(inserting)

            # insert name to main table
            try:
                conn = sqlite3.connect(database_file)
                conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
                cursor = conn.cursor()  # creates cursor

                # Insert name to Anak
                insert_string = "UPDATE Anak SET `tempat lahir` = ?, alamat = ?, `nomor telpon` = ?, " \
                                "`jenis kelamin` = ?,ortu = ?, `nama sekolah minggu` = ?, `SOM 1` = ?, `SOM 2` = ?, " \
                                "`SOM 3` = ?, `nama sekolah` = ?"
                cursor.execute(insert_string, inserting)
                conn.commit()

            except sqlite3.Error as err:
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                print("SQLite Error: %s" % err.args[0])

            else:
                print("Passed")

            finally:
                if conn:
                    conn.close()

                informan.clear()
                self.closeWindow()
        else:
            # Getting values to store to variables
            tempat = str(self.tempat_lahir.get().lower())
            address = str(self.alamat.get().lower())
            telpon = str(self.telpon.get())
            gender = str(self.gender.lower())
            ortu = str(self.ortu.get().lower())
            nama_skolah_minggu = str(self.nama_skolah_minggu.get().lower())
            skolah_nama = str(self.skolah_nama.get().lower())
            photo_name = str(self.photo_loc)

            # Getting photo to variable
            with open(photo_name, 'rb') as pic:
                photo_insert = pic.read()

            # Check required entry
            if tempat == "" or address == "" or ortu == "":
                showerror(title="Textbox wajib kosong", message="Tolong isi data wajib")
                return

            # inserting to list to insert
            inserting.append(tempat)
            inserting.append(address)
            inserting.append(telpon)
            inserting.append(gender)
            inserting.append(ortu)
            inserting.append(nama_skolah_minggu)

            if self.som1.get() == 2:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som2.get() == 4:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som3.get() == 6:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            inserting.append(skolah_nama)
            inserting.append(photo_insert)

            # insert name to main table
            try:
                conn = sqlite3.connect(database_file)
                conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
                cursor = conn.cursor()  # creates cursor

                # Insert name to Anak
                insert_string = "UPDATE Anak SET `tempat lahir` = ?, alamat = ?, `nomor telpon` = ?, " \
                                "`jenis kelamin` = ?,ortu = ?, `nama sekolah minggu` = ?, `SOM 1` = ?, `SOM 2` = ?, " \
                                "`SOM 3` = ?, `nama sekolah` = ?, photo = ?"
                cursor.execute(insert_string, inserting)
                conn.commit()

            except sqlite3.Error as err:
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                print("SQLite Error: %s" % err.args[0])

            else:
                print("Passed")

            finally:
                if conn:
                    conn.close()

                informan.clear()
                self.closeWindow()

        # myEntry = Label(text=data)
        # myEntry.pack()
        # print("Finish pack")

    def uploadAction(self):
        file = filedialog.askopenfilename()  # opens file dialog
        self.filename = file  # saves the file location/name
        self.photo_loc = os.path.abspath(file)
        filename = self.filename[::-1]
        name_of_pic = ""

        for i in filename:
            if i == "/":
                break
            name_of_pic += i

        self.foto = name_of_pic


class UpdateRemaja:
    def __init__(self):
        print("Edit")
        global informan, database_file
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.master.geometry("1000x700")
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        genders = ["P", "W"]

        self.tempat = StringVar()
        self.telpon = StringVar()
        self.kelamin = StringVar()
        self.ortu = StringVar()
        self.skolah_minggu = StringVar()
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()
        self.skolah_nama = StringVar()
        self.filename = StringVar()
        self.foto = ""
        self.photo_loc = ""

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)

        # Query to get initial values for text box to be edited
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            get_data_string = "SELECT * FROM Remaja WHERE nama LIKE ?"
            cursor.execute(get_data_string, (informan[0],))
            row = cursor.fetchone()

            while row:
                new_row = []
                for i in range(len(row)):
                    new_row.append(row[i])

                row = cursor.fetchone()

            new_row.pop(0)
            new_row.pop(0)
            new_row.pop(0)
            new_row.pop()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        finally:
            if conn:
                conn.close()

        status_pel = ["Sudah", "Belum, tapi bersedia", "Belum, dan belum bersedia"]
        if new_row[9] == "belum":
            set_som1 = False
        else:
            set_som1 = True

        if new_row[10] == "belum":
            set_som2 = False
        else:
            set_som2 = True

        if new_row[11] == "belum":
            set_som3 = False
        else:
            set_som3 = True

        self.tempat = StringVar()
        self.alamat = StringVar()
        self.telpon = StringVar()
        self.kelamin = StringVar()
        self.kelamin.set(new_row[3])
        self.ortu = StringVar()
        self.sudah_baptisan = StringVar()
        self.sudah_baptisan.set(new_row[5])
        self.tanggal_baptis = StringVar()
        self.sudah_pelayanan = StringVar()
        self.sudah_pelayanan.set(new_row[7])
        self.jenis_pel = StringVar()
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()
        self.sudah_gabung_komisi = StringVar()
        self.sudah_gabung_komisi.set(new_row[12])
        self.nama_komisi = StringVar()
        self.sudah_gabung_jdm = StringVar()
        self.sudah_gabung_jdm.set(status_pel[2])
        self.nama_jdm = StringVar()
        self.filename = StringVar()
        self.foto = ""
        self.photo_loc = ""

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        # Create Text Boxes
        self.tempat_lahir = Entry(self.master, width=30)
        self.tempat_lahir.insert(END, new_row[0])
        self.tempat_lahir.grid(row=3, column=1, padx=20)
        self.alamat = Entry(self.master, width=30)
        self.alamat.insert(END, new_row[1])
        self.alamat.grid(row=4, column=1, padx=20)
        self.telpon = Entry(self.master, width=30)
        self.telpon.insert(END, new_row[2])
        self.telpon.grid(row=5, column=1, padx=20)
        self.gender = OptionMenu(self.master, self.kelamin, *genders)
        self.gender.grid(row=6, column=1)
        self.ortu = Entry(self.master, width=30)
        self.ortu.insert(END, new_row[4])
        self.ortu.grid(row=7, column=1, padx=20)
        self.sudah_baptis = OptionMenu(self.master, self.sudah_baptisan, *status_pel)
        self.sudah_baptis.grid(row=8, column=1)
        self.tanggal_baptis = Entry(self.master, width=30)
        self.tanggal_baptis.insert(END, new_row[6])
        self.tanggal_baptis.grid(row=9, column=1)
        self.sudah_pel = OptionMenu(self.master, self.sudah_pelayanan, *status_pel)
        self.sudah_pel.grid(row=10, column=1)
        self.jenis_pel = Entry(self.master, width=30)
        self.jenis_pel.insert(END, new_row[8])
        self.jenis_pel.grid(row=11, column=1, padx=20)

        if set_som1:
            self.som1.set(2)
            self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
            self.som1_button.grid(row=12, column=1, padx=20)
            self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
            self.som1_button2.grid(row=12, column=2, padx=20)
        else:
            self.som1.set(3)
            self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
            self.som1_button.grid(row=12, column=1, padx=20)
            self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
            self.som1_button2.grid(row=12, column=2, padx=20)

        if set_som2:
            self.som2.set(4)
            self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
            self.som2_button.grid(row=13, column=1, padx=20)
            self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
            self.som2_button2.grid(row=13, column=2, padx=20)
        else:
            self.som2.set(5)
            self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
            self.som2_button.grid(row=13, column=1, padx=20)
            self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
            self.som2_button2.grid(row=13, column=2, padx=20)

        if set_som3:
            self.som3.set(6)
            self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
            self.som3_button.grid(row=14, column=1, padx=20)
            self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
            self.som3_button2.grid(row=14, column=2, padx=20)
        else:
            self.som3.set(7)
            self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
            self.som3_button.grid(row=14, column=1, padx=20)
            self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
            self.som3_button2.grid(row=14, column=2, padx=20)

        self.gabung_komisi = OptionMenu(self.master, self.sudah_gabung_komisi, *status_pel)
        self.gabung_komisi.grid(row=15, column=1)
        self.komisi_nama = Entry(self.master, width=30)
        self.komisi_nama.insert(END, new_row[13])
        self.komisi_nama.grid(row=16, column=1, padx=20)

        # Create Label for text boxes
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.tempat_lahir_label = Label(self.master, text="Tempat Lahir", font=self.fontStyle)
        self.tempat_lahir_label.grid(row=3, column=0, padx=7, sticky=W)
        self.alamat_label = Label(self.master, text="Alamat*", font=self.fontStyle)
        self.alamat_label.grid(row=4, column=0, padx=7, sticky=W)
        self.telpon_label = Label(self.master, text="Nomor telpon", font=self.fontStyle)
        self.telpon_label.grid(row=5, column=0, padx=7, sticky=W)
        self.gender_label = Label(self.master, text="Jenis Kelamin*", font=self.fontStyle)
        self.gender_label.grid(row=6, column=0, padx=7, sticky=W)
        self.ortu_label = Label(self.master, text="Nama orang tua*", font=self.fontStyle)
        self.ortu_label.grid(row=7, column=0, padx=7, sticky=W)
        self.sudah_baptis_label = Label(self.master, text="Sudah dibaptis?*", font=self.fontStyle)
        self.sudah_baptis_label.grid(row=8, column=0, padx=7, sticky=W)
        self.tanggal_baptis_label = Label(self.master, text="Kalau sudah, tolong masukan tanggal dibaptis?",
                                          font=self.fontStyle)
        self.tanggal_baptis_label.grid(row=9, column=0, padx=7, sticky=W)
        self.sudah_pel_label = Label(self.master, text="Sudah Pelayanan?*", font=self.fontStyle)
        self.sudah_pel_label.grid(row=10, column=0, padx=7, sticky=W)
        self.jenis_pel_label = Label(self.master, text="Kalau sudah, tolong masukan jenis Pelayanan",
                                     font=self.fontStyle)
        self.jenis_pel_label.grid(row=11, column=0, padx=7, sticky=W)
        self.som1_button_label = Label(self.master, text="Sudah ikut SOM 1?", font=self.fontStyle)
        self.som1_button_label.grid(row=12, column=0, padx=7, sticky=W)
        self.som2_button_label = Label(self.master, text="Sudah ikut SOM 2?", font=self.fontStyle)
        self.som2_button_label.grid(row=13, column=0, padx=7, sticky=W)
        self.som3_button_label = Label(self.master, text="Sudah ikut SOM 3?", font=self.fontStyle)
        self.som3_button_label.grid(row=14, column=0, padx=7, sticky=W)
        self.gabung_komisi_label = Label(self.master, text="Sudah gabung komisi?", font=self.fontStyle)
        self.gabung_komisi_label.grid(row=15, column=0, padx=7, sticky=W)
        self.nama_komisi_label = Label(self.master, text="Nama komisi?", font=self.fontStyle)
        self.nama_komisi_label.grid(row=16, column=0, padx=7, sticky=W)

        # self.print_button = Button(self.master, text="Print nama foto", command=self.printPhoto)
        # self.print_button.pack()
        # Upload photo & submit button
        self.gettingphoto_button = Button(self.master, text="Click untuk masukan photo*", command=self.uploadAction)
        self.gettingphoto_button.grid(row=19, column=1, columnspan=2, pady=10, padx=10, ipadx=100)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.editData)
        self.sumbitButton.grid(row=20, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        self.master.grid_rowconfigure(1, minsize=20)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def editData(self):
        global informan
        inserting = []

        # Getting values to store to variables
        tempat = str(self.tempat_lahir.get())
        address = str(self.alamat.get())
        telpon = str(self.telpon.get())
        gender = str(self.kelamin.get())
        ortu = str(self.ortu.get())
        sudah_baptis = str(self.sudah_baptisan.get())
        tanggal_baptis = str(self.tanggal_baptis.get())
        sudah_pelayanan = str(self.sudah_pelayanan.get())
        jenis_pelayanan = str(self.jenis_pel.get())
        gabung_komisi = str(self.sudah_gabung_komisi.get())
        nama_komisi = str(self.komisi_nama.get())
        photo_name = str(self.photo_loc)

        # Check required entry
        if address == "":
            showerror(title="Textbox wajib kosong", message="Tolong isi data wajib")
            return

        if photo_name != "":
            # Getting photo to variable
            with open(photo_name, 'rb') as pic:
                photo_insert = pic.read()

            # inserting to list to insert
            inserting.append(tempat)
            inserting.append(address)
            inserting.append(telpon)
            inserting.append(gender)
            inserting.append(ortu)
            inserting.append(sudah_baptis)
            inserting.append(tanggal_baptis)
            inserting.append(sudah_pelayanan)
            inserting.append(jenis_pelayanan)

            if self.som1.get() == 2:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som2.get() == 4:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som3.get() == 6:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            inserting.append(gabung_komisi)
            inserting.append(nama_komisi)
            inserting.append(photo_insert)

            # insert name to main table
            try:
                conn = sqlite3.connect(database_file)
                conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
                cursor = conn.cursor()  # creates cursor

                # Insert name to Anak
                update_string = "UPDATE Remaja SET `tempat lahir` = ?, alamat = ?, `nomor telpon` = ?, " \
                                "`jenis kelamin` = ?, ortu = ?, `sudah baptis` = ?, `tanggal baptis` = ?, " \
                                "`sudah pelayanan` = ?, `jenis pelayanan` = ?, `SOM 1` = ?, `SOM 2` = ?, " \
                                "`SOM 3` = ?, `gabung komisi` = ?, `nama komisi` = ?, photo = ?"
                cursor.execute(update_string, inserting)
                conn.commit()

            except sqlite3.Error as err:
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                print("SQLite Error: %s" % err.args[0])

            else:
                print("Passed")

            finally:
                if conn:
                    conn.close()

                informan.clear()
                self.closeWindow()

        else:
            print("A")
            # inserting to list to insert
            inserting.append(tempat)
            inserting.append(address)
            inserting.append(telpon)
            inserting.append(gender)
            inserting.append(ortu)
            inserting.append(sudah_baptis)
            inserting.append(tanggal_baptis)
            inserting.append(sudah_pelayanan)
            inserting.append(jenis_pelayanan)

            if self.som1.get() == 2:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som2.get() == 4:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som3.get() == 6:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            inserting.append(gabung_komisi)
            inserting.append(nama_komisi)
            print(inserting)

            # insert name to main table
            try:
                conn = sqlite3.connect(database_file)
                conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
                cursor = conn.cursor()  # creates cursor

                # Insert name to Anak
                update_string = "UPDATE Remaja SET `tempat lahir` = ?, alamat = ?, `nomor telpon` = ?, " \
                                "`jenis kelamin` = ?, ortu = ?, `sudah baptis` = ?, `tanggal baptis` = ?, " \
                                "`sudah pelayanan` = ?, `jenis pelayanan` = ?, `SOM 1` = ?, `SOM 2` = ?, `SOM 3` = ?," \
                                "`gabung komisi` = ?, `nama komisi` = ?"
                cursor.execute(update_string, inserting)
                conn.commit()

            except sqlite3.Error as err:
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                print("SQLite Error: %s" % err.args[0])

            else:
                print("Passed")

            finally:
                if conn:
                    conn.close()

                informan.clear()
                self.closeWindow()
        # myEntry = Label(text=data)
        # myEntry.pack()
        # print("Finish pack")

    def uploadAction(self):
        file = filedialog.askopenfilename()  # opens file dialog
        self.filename = file  # saves the file location/name
        self.photo_loc = os.path.abspath(file)
        filename = self.filename[::-1]
        name_of_pic = ""

        for i in filename:
            if i == "/":
                break
            name_of_pic += i

        self.foto = name_of_pic


class UpdateDewasa:
    def __init__(self):
        global informan, database_file
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        self.master.geometry("1000x700")
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        genders = ["P", "W"]
        status = ["Lajang", "Menikah", "Cerai Hidup/Mati"]
        status_pel = ["Sudah", "Belum, tapi bersedia", "Belum, dan belum bersedia"]

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)

        # Query to get initial values for text box to be edited
        try:
            conn = sqlite3.connect(database_file)
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor

            get_data_string = "SELECT * FROM Dewasa WHERE nama LIKE ?"
            cursor.execute(get_data_string, (informan[0],))
            row = cursor.fetchone()

            while row:
                new_row = []
                for i in range(len(row)):
                    new_row.append(row[i])

                row = cursor.fetchone()

            # make the list consistent with the other list
            new_row.pop(0)
            new_row.pop(0)
            new_row.pop(0)
            new_row.pop()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])

        finally:
            if conn:
                conn.close()

        if new_row[23] == "belum":
            set_som1 = False
        else:
            set_som1 = True

        if new_row[24] == "belum":
            set_som2 = False
        else:
            set_som2 = True

        if new_row[25] == "belum":
            set_som3 = False
        else:
            set_som3 = True

        if new_row[30] == "belum":
            set_sosial = False
        else:
            set_sosial = True

        self.alamat = StringVar()
        self.tempat = StringVar()
        self.telpon = StringVar()
        self.kelamin = StringVar()
        self.kelamin.set(new_row[3])
        self.ortu = StringVar()
        self.sudah_bap = StringVar()
        self.sudah_bap.set(new_row[19])
        self.tanggal_baptis = StringVar()
        self.sudah_pelayan = StringVar()
        self.sudah_pelayan.set(new_row[21])
        self.jenis_pel = StringVar()
        self.anggota = StringVar()
        self.anggota.set(new_row[18])
        self.som1 = IntVar()
        self.som2 = IntVar()
        self.som3 = IntVar()
        self.gabung_komi = StringVar()
        self.gabung_komi.set(new_row[26])
        self.nama_komisi = StringVar()
        self.gabung_jdmm = StringVar()
        self.gabung_jdmm.set(new_row[28])
        self.nama_jdm = StringVar()
        self.nikah = StringVar()
        self.nikah.set(new_row[5])
        self.filename = StringVar()
        self.sosial_member = IntVar()
        self.foto = ""
        self.photo_loc = ""

        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        # Create Text Boxes for personal info
        self.tempat_lahir = Entry(self.master, width=20)
        self.tempat_lahir.insert(END, new_row[0])
        self.tempat_lahir.grid(row=3, column=1, padx=7)
        self.alamat = Entry(self.master, width=20)
        self.alamat.insert(END, new_row[1])
        self.alamat.grid(row=4, column=1, padx=7)
        self.telpon = Entry(self.master, width=20)
        self.telpon.insert(END, new_row[2])
        self.telpon.grid(row=5, column=1, padx=7)
        self.gender = OptionMenu(self.master, self.kelamin, *genders)
        self.gender.grid(row=6, column=1)
        self.job = Entry(self.master, width=20)
        self.job.insert(END, new_row[4])
        self.job.grid(row=7, column=1)
        self.status_nikah = OptionMenu(self.master, self.nikah, *status)
        self.status_nikah.grid(row=8, column=1)
        self.ortu = Entry(self.master, width=30)
        self.ortu.insert(END, new_row[6])
        self.ortu.grid(row=9, column=1, padx=7)
        self.pasangan = Entry(self.master, width=30)
        self.pasangan.insert(END, new_row[7])
        self.pasangan.grid(row=10, column=1, padx=7)

        self.anak1_nama = Entry(self.master, width=30)
        self.anak1_nama.insert(END, new_row[8])
        self.anak1_umur = Entry(self.master, width=5)
        self.anak1_umur.insert(END, new_row[9])
        self.anak1_nama.grid(row=11, column=1, padx=7)
        self.anak1_umur.grid(row=11, column=3, padx=7)

        self.anak2_nama = Entry(self.master, width=30)
        self.anak2_nama.insert(END, new_row[10])
        self.anak2_umur = Entry(self.master, width=5)
        self.anak2_umur.insert(END, new_row[11])
        self.anak2_nama.grid(row=12, column=1, padx=7)
        self.anak2_umur.grid(row=12, column=3, padx=7)

        self.anak3_nama = Entry(self.master, width=30)
        self.anak3_nama.insert(END, new_row[12])
        self.anak3_umur = Entry(self.master, width=5)
        self.anak3_umur.insert(END, new_row[13])
        self.anak3_nama.grid(row=13, column=1, padx=7)
        self.anak3_umur.grid(row=13, column=3, padx=7)

        self.anak4_nama = Entry(self.master, width=30)
        self.anak4_nama.insert(END, new_row[14])
        self.anak4_umur = Entry(self.master, width=5)
        self.anak4_umur.insert(END, new_row[15])
        self.anak4_nama.grid(row=14, column=1, padx=7)
        self.anak4_umur.grid(row=14, column=3, padx=7)

        self.anak5_nama = Entry(self.master, width=30)
        self.anak5_nama.insert(END, new_row[16])
        self.anak5_umur = Entry(self.master, width=5)
        self.anak5_umur.insert(END, new_row[17])
        self.anak5_nama.grid(row=15, column=1, padx=7)
        self.anak5_umur.grid(row=15, column=3, padx=7)

        # Create text boxes for Church Info
        self.member = OptionMenu(self.master, self.anggota, *status_pel)
        self.member.grid(row=3, column=7, padx=7)
        self.sudah_baptis = OptionMenu(self.master, self.sudah_bap, *status_pel)
        self.sudah_baptis.grid(row=4, column=7)
        self.tanggal_baptis = Entry(self.master, width=30)
        self.tanggal_baptis.insert(END, new_row[20])
        self.tanggal_baptis.grid(row=5, column=7)
        self.sudah_pel = OptionMenu(self.master, self.sudah_pelayan, *status_pel)
        self.sudah_pel.grid(row=6, column=7)
        self.jenis_pel = Entry(self.master, width=30)
        self.jenis_pel.insert(END, new_row[22])
        self.jenis_pel.grid(row=7, column=7, padx=7)

        if set_som1:
            self.som1.set(2)
            self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
            self.som1_button.grid(row=8, column=7, padx=7)
            self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
            self.som1_button2.grid(row=8, column=8, padx=7)
        else:
            self.som1.set(3)
            self.som1_button = Radiobutton(self.master, text="Sudah", variable=self.som1, value=2)
            self.som1_button.grid(row=8, column=7, padx=7)
            self.som1_button2 = Radiobutton(self.master, text="Belum", variable=self.som1, value=3)
            self.som1_button2.grid(row=8, column=8, padx=7)

        if set_som2:
            self.som2.set(4)
            self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
            self.som2_button.grid(row=9, column=7, padx=7)
            self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
            self.som2_button2.grid(row=9, column=8, padx=7)
        else:
            self.som2.set(5)
            self.som2_button = Radiobutton(self.master, text="Sudah", variable=self.som2, value=4)
            self.som2_button.grid(row=9, column=7, padx=7)
            self.som2_button2 = Radiobutton(self.master, text="Belum", variable=self.som2, value=5)
            self.som2_button2.grid(row=9, column=8, padx=7)

        if set_som3:
            self.som3.set(6)
            self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
            self.som3_button.grid(row=10, column=7, padx=7)
            self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
            self.som3_button2.grid(row=10, column=8, padx=7)
        else:
            self.som3.set(7)
            self.som3_button = Radiobutton(self.master, text="Sudah", variable=self.som3, value=6)
            self.som3_button.grid(row=10, column=7, padx=7)
            self.som3_button2 = Radiobutton(self.master, text="Belum", variable=self.som3, value=7)
            self.som3_button2.grid(row=10, column=8, padx=7)

        self.gabung_komisi = OptionMenu(self.master, self.gabung_komi, *status_pel)
        self.gabung_komisi.grid(row=11, column=7)
        self.komisi_nama = Entry(self.master, width=30)
        self.komisi_nama.insert(END, new_row[27])
        self.komisi_nama.grid(row=12, column=7, padx=7)
        self.gabung_jdm = OptionMenu(self.master, self.gabung_jdmm, *status_pel)
        self.gabung_jdm.grid(row=13, column=7)
        self.nama_jdm = Entry(self.master, width=30)
        self.nama_jdm.insert(END, new_row[29])
        self.nama_jdm.grid(row=14, column=7, padx=7)

        if set_sosial:
            self.sosial_member.set(2)
            self.sosial_mati_member = Radiobutton(self.master, text="Sudah", variable=self.sosial_member, value=2)
            self.sosial_mati_member.grid(row=15, column=7, padx=7)
            self.sosial_mati_member2 = Radiobutton(self.master, text="Belum", variable=self.sosial_member, value=3)
            self.sosial_mati_member2.grid(row=15, column=8, padx=7)
        else:
            self.sosial_member.set(3)
            self.sosial_mati_member = Radiobutton(self.master, text="Sudah", variable=self.sosial_member, value=2)
            self.sosial_mati_member.grid(row=15, column=7, padx=7)
            self.sosial_mati_member2 = Radiobutton(self.master, text="Belum", variable=self.sosial_member, value=3)
            self.sosial_mati_member2.grid(row=15, column=8, padx=7)

        # Create Label for text boxes personal info
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.tempat_lahir_label = Label(self.master, text="Tempat Lahir", font=self.fontStyle)
        self.tempat_lahir_label.grid(row=3, column=0)
        self.alamat_label = Label(self.master, text="Alamat*", font=self.fontStyle)
        self.alamat_label.grid(row=4, column=0)
        self.telpon_label = Label(self.master, text="Nomor telpon", font=self.fontStyle)
        self.telpon_label.grid(row=5, column=0)
        self.gender_label = Label(self.master, text="Jenis Kelamin", font=self.fontStyle)
        self.gender_label.grid(row=6, column=0)
        self.job_label = Label(self.master, text="Pekerjaan", font=self.fontStyle)
        self.job_label.grid(row=7, column=0)
        self.status_nikah_label = Label(self.master, text="Status nikah", font=self.fontStyle)
        self.status_nikah_label.grid(row=8, column=0)
        self.ortu_label = Label(self.master, text="Nama orang tua", font=self.fontStyle)
        self.ortu_label.grid(row=9, column=0)
        self.pasangan_label = Label(self.master, text="Nama suami/istri", font=self.fontStyle)
        self.pasangan_label.grid(row=10, column=0)
        self.son1name_label = Label(self.master, text="Nama anak pertama", font=self.fontStyle)
        self.son1age_label = Label(self.master, text="Umur")
        self.son1name_label.grid(row=11, column=0)
        self.son1age_label.grid(row=11, column=2)

        self.son2name_label = Label(self.master, text="Nama anak kedua", font=self.fontStyle)
        self.son2age_label = Label(self.master, text="Umur")
        self.son2name_label.grid(row=12, column=0)
        self.son2age_label.grid(row=12, column=2)

        self.son3name_label = Label(self.master, text="Nama anak ketiga", font=self.fontStyle)
        self.son3age_label = Label(self.master, text="Umur")
        self.son3name_label.grid(row=13, column=0)
        self.son3age_label.grid(row=13, column=2)

        self.son4name_label = Label(self.master, text="Nama anak keempat", font=self.fontStyle)
        self.son4age_label = Label(self.master, text="Umur")
        self.son4name_label.grid(row=14, column=0)
        self.son4age_label.grid(row=14, column=2)

        self.son5name_label = Label(self.master, text="Nama anak kelima", font=self.fontStyle)
        self.son5age_label = Label(self.master, text="Umur")
        self.son5name_label.grid(row=15, column=0)
        self.son5age_label.grid(row=15, column=2)

        # Create Label for text box Church info
        self.member_label = Label(self.master, text="Sudah anggota?*", font=self.fontStyle)
        self.member_label.grid(row=3, column=6)
        self.sudah_baptis_label = Label(self.master, text="Sudah dibaptis?*", font=self.fontStyle)
        self.sudah_baptis_label.grid(row=4, column=6)
        self.tanggal_baptis_label = Label(self.master, text="Tanggal dibaptis?",
                                          font=self.fontStyle)
        self.tanggal_baptis_label.grid(row=5, column=6)
        self.sudah_pel_label = Label(self.master, text="Sudah Pelayanan?*", font=self.fontStyle)
        self.sudah_pel_label.grid(row=6, column=6)
        self.jenis_pel_label = Label(self.master, text="Jenis Pelayanan",
                                     font=self.fontStyle)
        self.jenis_pel_label.grid(row=7, column=6)
        self.som1_button_label = Label(self.master, text="Sudah ikut SOM 1?", font=self.fontStyle)
        self.som1_button_label.grid(row=8, column=6)
        self.som2_button_label = Label(self.master, text="Sudah ikut SOM 2?", font=self.fontStyle)
        self.som2_button_label.grid(row=9, column=6)
        self.som3_button_label = Label(self.master, text="Sudah ikut SOM 3?", font=self.fontStyle)
        self.som3_button_label.grid(row=10, column=6)
        self.gabung_komisi_label = Label(self.master, text="Sudah gabung komisi?*", font=self.fontStyle)
        self.gabung_komisi_label.grid(row=11, column=6)
        self.nama_komisi_label = Label(self.master, text="Nama komisi?", font=self.fontStyle)
        self.nama_komisi_label.grid(row=12, column=6)
        self.gabung_jdm_label = Label(self.master, text="Sudah gabung JDM?*", font=self.fontStyle)
        self.gabung_jdm_label.grid(row=13, column=6)
        self.nama_jdm_label = Label(self.master, text="Nama JDM?", font=self.fontStyle)
        self.nama_jdm_label.grid(row=14, column=6)
        self.sosial_mati_member_label = Label(self.master, text="Sudah jadi anggota sosial mati?*", font=self.fontStyle)
        self.sosial_mati_member_label.grid(row=15, column=6)

        # Upload photo & submit button
        self.gettingphoto_button = Button(self.master, text="Click untuk masukan photo*", font=self.fontStyle,
                                          command=self.uploadAction)
        self.gettingphoto_button.grid(row=17, column=6, columnspan=2, pady=10, padx=10, ipadx=100)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.editData)
        self.sumbitButton.grid(row=17, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        self.master.grid_columnconfigure(5, minsize=200)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self):
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def closeWindow(self):
        global mainmenu
        mainmenu = True
        self.master.destroy()

    def editData(self):
        global informan
        inserting = []
        nama = informan[0]

        # Getting values to store to variables
        photo_name = str(self.photo_loc)

        # Check required entry
        if self.alamat.get() == "":
            showerror(title="Textbox wajib kosong", message="Tolong isi data wajib")
            return

        if photo_name != "":

            # Getting photo to variable
            with open(photo_name, 'rb') as pic:
                photo_insert = pic.read()

            # inserting to list to insert
            inserting.append(str(self.tempat_lahir.get().lower()))
            inserting.append(str(self.alamat.get().lower()))
            inserting.append(str(self.telpon.get()))
            inserting.append(str(self.kelamin.get().lower()))
            inserting.append(str(self.job.get().lower()))
            inserting.append(str(self.nikah.get().lower()))
            inserting.append(str(self.ortu.get().lower()))
            inserting.append(str(self.pasangan.get().lower()))
            inserting.append(str(self.anak1_nama.get().lower()))
            inserting.append(str(self.anak1_umur.get()))
            inserting.append(str(self.anak2_nama.get().lower()))
            inserting.append(str(self.anak2_umur.get()))
            inserting.append(str(self.anak3_nama.get().lower()))
            inserting.append(str(self.anak3_umur.get()))
            inserting.append(str(self.anak4_nama.get().lower()))
            inserting.append(str(self.anak4_umur.get()))
            inserting.append(str(self.anak5_nama.get().lower()))
            inserting.append(str(self.anak5_umur.get()))
            inserting.append(str(self.anggota.get().lower()))
            inserting.append(str(self.sudah_bap.get()))
            inserting.append(str(self.tanggal_baptis.get()))
            inserting.append(str(self.sudah_pelayan.get()))
            inserting.append(str(self.jenis_pel.get().lower()))

            if self.som1.get() == 2:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som2.get() == 4:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som3.get() == 6:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            inserting.append(str(self.gabung_komi.get()))
            inserting.append(str(self.komisi_nama.get().lower()))
            inserting.append(str(self.gabung_jdmm.get()))
            inserting.append(str(self.nama_jdm.get().lower()))

            if self.sosial_mati_member == 2:
                inserting.append("sudah")
            else:
                inserting.append("belum")

            inserting.append(photo_insert)

            # insert name to main table
            try:
                conn = sqlite3.connect(database_file)
                conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
                cursor = conn.cursor()  # creates cursor

                # Insert name to Anak
                update_string = "UPDATE Dewasa SET `tempat lahir` = ?, alamat = ?, `nomor telpon` = ?, " \
                                "`jenis kelamin` = ?, pekerjaan = ?, `status nikah` = ?, ortu = ?, " \
                                "`nama suami/istri` = ?, `nama anak pertama` = ?, `umur anak pertama` = ?, " \
                                "`nama anak kedua` = ?, `umur anak kedua` = ?, `nama anak ketiga` = ?, " \
                                "`umur anak ketiga` = ?, `nama anak keempat` = ?, `umur anak keempat` = ?, " \
                                "`nama anak kelima` = ?, `umur anak kelima` = ?, anggota = ?, `sudah dibaptis` = ?, " \
                                "`tanggal dibaptis` = ?, `sudah pelayanan` = ?, `jenis pelayanan` = ?, `SOM 1` = ?, " \
                                "`SOM 2` = ?, `SOM 3` = ?, `gabung komisi` = ?, `nama komisi` = ?, `gabung jdm` = ?, " \
                                "`nama jdm` = ?, `anggota sosial mati` = ?, photo = ?"
                cursor.execute(update_string, inserting)
                conn.commit()

            except sqlite3.Error as err:
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                print("SQLite Error: %s" % err.args[0])

            else:
                print("Passed")

            finally:
                if conn:
                    conn.close()

                informan.clear()
                self.closeWindow()

        else:
            # inserting to list to insert
            inserting.append(str(self.tempat_lahir.get().lower()))
            inserting.append(str(self.alamat.get().lower()))
            inserting.append(str(self.telpon.get()))
            inserting.append(str(self.kelamin.get().lower()))
            inserting.append(str(self.job.get().lower()))
            inserting.append(str(self.nikah.get().lower()))
            inserting.append(str(self.ortu.get().lower()))
            inserting.append(str(self.pasangan.get().lower()))
            inserting.append(str(self.anak1_nama.get().lower()))
            inserting.append(str(self.anak1_umur.get()))
            inserting.append(str(self.anak2_nama.get().lower()))
            inserting.append(str(self.anak2_umur.get()))
            inserting.append(str(self.anak3_nama.get().lower()))
            inserting.append(str(self.anak3_umur.get()))
            inserting.append(str(self.anak4_nama.get().lower()))
            inserting.append(str(self.anak4_umur.get()))
            inserting.append(str(self.anak5_nama.get().lower()))
            inserting.append(str(self.anak5_umur.get()))
            inserting.append(str(self.anggota.get().lower()))
            inserting.append(str(self.sudah_bap.get()))
            inserting.append(str(self.tanggal_baptis.get()))
            inserting.append(str(self.sudah_pelayan.get()))
            inserting.append(str(self.jenis_pel.get().lower()))

            if self.som1.get() == 2:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som2.get() == 4:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            if self.som3.get() == 6:
                print("Ikut")
                inserting.append("sudah")
            else:
                print("Belum")
                inserting.append("belum")

            inserting.append(str(self.gabung_komi.get()))
            inserting.append(str(self.komisi_nama.get().lower()))
            inserting.append(str(self.gabung_jdmm.get()))
            inserting.append(str(self.nama_jdm.get().lower()))

            if self.sosial_mati_member == 2:
                inserting.append("sudah")
            else:
                inserting.append("belum")

            # insert name to main table
            try:
                conn = sqlite3.connect(database_file)
                conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
                cursor = conn.cursor()  # creates cursor

                # Insert name to Anak
                update_string = "UPDATE Dewasa SET `tempat lahir` = ?, alamat = ?, `nomor telpon` = ?, " \
                                "`jenis kelamin` = ?, pekerjaan = ?, `status nikah` = ?, ortu = ?, " \
                                "`nama suami/istri` = ?, `nama anak pertama` = ?, `umur anak pertama` = ?, " \
                                "`nama anak kedua` = ?, `umur anak kedua` = ?, `nama anak ketiga` = ?, " \
                                "`umur anak ketiga` = ?, `nama anak keempat` = ?, `umur anak keempat` = ?, " \
                                "`nama anak kelima` = ?, `umur anak kelima` = ?, anggota = ?, `sudah dibaptis` = ?, " \
                                "`tanggal dibaptis` = ?, `sudah pelayanan` = ?, `jenis pelayanan` = ?, `SOM 1` = ?, " \
                                "`SOM 2` = ?, `SOM 3` = ?, `gabung komisi` = ?, `nama komisi` = ?, `gabung jdm` = ?, " \
                                "`nama jdm` = ?, `anggota sosial mati` = ?"
                cursor.execute(update_string, inserting)
                conn.commit()

            except sqlite3.Error as err:
                if conn:
                    conn.rollback()  # reverse any changes before the commit

                print("SQLite Error: %s" % err.args[0])

            else:
                print("Passed")

            finally:
                if conn:
                    conn.close()

                informan.clear()
                self.closeWindow()
        # myEntry = Label(text=data)
        # myEntry.pack()
        # print("Finish pack")

    def uploadAction(self):
        file = filedialog.askopenfilename()  # opens file dialog
        self.filename = file  # saves the file location/name
        self.photo_loc = os.path.abspath(file)
        filename = self.filename[::-1]
        name_of_pic = ""

        for i in filename:
            if i == "/":
                break
            name_of_pic += i

        self.foto = name_of_pic


class Delete:
    def __init__(self):
        self.master = Tk()  # blank window
        self.master.title("Elim DB")
        self.master.iconbitmap()
        # self.width = self.master.winfo_screenwidth()
        # self.height = self.master.winfo_screenheight()
        # self.master.geometry("%dx%d+0+0" % (self.width, self.height))
        self.master.geometry("1000x600")
        self.img = Image.open("Logo Elim.jpg")
        self.photo = ImageTk.PhotoImage(self.img)
        self.photo_label = Label(image=self.photo)
        self.photo_label.grid(row=0, column=0, padx=5, pady=5)
        self.fontStyle = tkFont.Font(family="Helvetica", size=16)
        self.fontStyle2 = tkFont.Font(family="Helvetica", size=13)
        self.who_to_delete_label = Label(self.master, text="Tolong masukan nama yang mau di hapus",
                                         font=self.fontStyle2)
        self.who_to_delete_label.grid(row=1, column=0, pady=5, padx=5)

        # configures rows so it can be skipped
        self.master.rowconfigure(2, minsize=20)
        self.master.rowconfigure(4, minsize=100)
        # Create text box
        self.name = Entry(self.master, width=30)
        self.name.grid(row=3, column=1, padx=5)

        self.name_label = Label(self.master, text="Nama lengkap", font=self.fontStyle)
        self.name_label.grid(row=3, column=0, padx=5)

        self.sumbitButton = Button(self.master, text="Submit", font=self.fontStyle, command=self.deleteData)
        self.sumbitButton.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100, sticky=W)
        self.master.protocol("WM_DELETE_WINDOW", self.x_button)
        self.master.mainloop()

    def x_button(self): # overwrite the x button
        global mainmenu
        response = askquestion("Keluar program", "Yakin mau kembali ke menu?")
        if response == "yes":
            mainmenu = True
            self.closeWindow()

    def showErrorMessage(self):
        showerror(title="No name", message="Nama yang mau dihapus tidak ada di database")
        self.name.delete(0, END)

    def deleteData(self):
        global database_file
        try:
            conn = sqlite3.connect(database_file)
            conn.execute("PRAGMA foreign_keys = 1")
            conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
            cursor = conn.cursor()  # creates cursor
            name = (self.name.get().lower(),)
            # Search first to make sure the name exists in database
            search_string = "SELECT COUNT(*) FROM Jemaat WHERE nama = ?"
            cursor.execute(search_string, name)
            number = cursor.fetchone()
            for i in number:
                nomor = i

            if nomor == 0:
                # Clear the textboxes and show messagebox error
                raise notFoundError

            else:
                # Create the delete string
                cursor.execute("DELETE FROM Jemaat WHERE nama = ?", name)
                conn.commit()

        except notFoundError:
            self.showErrorMessage()

        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])
            sys.exit(-1)

        else:
            global mainmenu
            mainmenu = True
            self.closeWindow()

        finally:
            if conn:
                conn.close()

    def closeWindow(self):
        self.master.destroy()


def createDatabase(file_path):
    conn = None
    try:
        conn = sqlite3.connect(file_path)
        conn.execute("PRAGMA foreign_keys = 1")
        conn.row_factory = sqlite3.Row  # fetch each row as a dictionary
        cursor = conn.cursor()  # creates cursor

        # create table for jemaat
        cursor.execute("DROP TABLE IF EXISTS Jemaat")
        create_string = """CREATE TABLE Jemaat(
                            nama TEXT PRIMARY KEY NOT NULL,
                            `tanggal lahir` TEXT NOT NULL,
                            UNIQUE(nama)
                            )"""
        cursor.execute(create_string)

        # anak umur 0-11
        cursor.execute("DROP TABLE IF EXISTS Anak")
        create_string = """CREATE TABLE Anak (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            nama TEXT NOT NULL,
                            `tanggal lahir` TEXT NOT NULL,
                            `tempat lahir` TEXT,
                            alamat TEXT,
                            `nomor telpon` TEXT,
                            `jenis kelamin` TEXT,
                            ortu TEXT,
                            `nama sekolah minggu` TEXT,
                            `SOM 1` TEXT,
                            `SOM 2` TEXT,
                            `SOM 3` TEXT,
                            `nama sekolah` TEXT,
                            photo BLOB,
                            UNIQUE(nama),
                            FOREIGN KEY(nama) REFERENCES Jemaat(nama) 
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                        )"""
        cursor.execute(create_string)

        # remaja umur 12-19
        cursor.execute("DROP TABLE IF EXISTS Remaja")
        create_string = """CREATE TABLE Remaja (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            nama TEXT NOT NULL,
                            `tanggal lahir` TEXT NOT NULL,
                            `tempat lahir` TEXT,
                            alamat TEXT,
                            `nomor telpon` TEXT,
                            `jenis kelamin` TEXT,
                            ortu TEXT,
                            `sudah baptis` TEXT,
                            `tanggal baptis` TEXT,
                            `sudah pelayanan` TEXT,
                            `jenis pelayanan` TEXT,
                            `SOM 1` TEXT,
                            `SOM 2` TEXT,
                            `SOM 3` TEXT,
                            `gabung komisi` TEXT,
                            `nama komisi` TEXT,
                            photo BLOB,
                            UNIQUE(nama),
                            FOREIGN KEY(nama) REFERENCES Jemaat(nama) 
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                            )"""
        cursor.execute(create_string)

        # dewasa umur 20+
        cursor.execute("DROP TABLE IF EXISTS Dewasa")
        create_string = """CREATE TABLE Dewasa (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                nama TEXT NOT NULL, 
                                `tanggal lahir` TEXT NOT NULL,
                                `tempat lahir` TEXT,
                                alamat TEXT,
                                `nomor telpon` TEXT,
                                `jenis kelamin` TEXT,
                                pekerjaan TEXT,
                                `status nikah` TEXT,
                                ortu TEXT,
                                `nama suami/istri` TEXT,
                                `nama anak pertama` TEXT,
                                `umur anak pertama` TEXT,
                                `nama anak kedua` TEXT,
                                `umur anak kedua` TEXT,
                                `nama anak ketiga` TEXT,
                                `umur anak ketiga` TEXT,
                                `nama anak keempat` TEXT,
                                `umur anak keempat` TEXT,
                                `nama anak kelima` TEXT,
                                `umur anak kelima` TEXT,
                                anggota TEXT,
                                `sudah dibaptis` TEXT,
                                `tanggal dibaptis` TEXT,
                                `sudah pelayanan` TEXT,
                                `jenis pelayanan` TEXT,
                                `SOM 1` TEXT,
                                `SOM 2` TEXT,
                                `SOM 3` TEXT,
                                `gabung komisi` TEXT,
                                `nama komisi` TEXT,
                                `gabung jdm` TEXT,
                                `nama jdm` TEXT,
                                `anggota sosial mati` TEXT,
                                photo BLOB,
                                UNIQUE(nama),
                                FOREIGN KEY(nama) REFERENCES Jemaat(nama) 
                                    ON UPDATE CASCADE
                                    ON DELETE CASCADE
                                )"""
        cursor.execute(create_string)

    except sqlite3.Error as err:
        if conn:
            conn.rollback()  # reverse any changes before the commit

        print("SQLite Error: %s" % err.args[0])
        sys.exit(-1)

    finally:

        if conn:
            conn.close()


def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    # data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))


def get_database_file():
    dir_path = os.path.join(os.environ['USERPROFILE'], 'Elim_data')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, 'jemaatElim.db')
    if not os.path.exists(file_path):
        try:
            conn = sqlite3.connect(file_path)
            conn.execute("PRAGMA foreign_keys = 1")
        except sqlite3.Error as err:
            if conn:
                conn.rollback()  # reverse any changes before the commit

            print("SQLite Error: %s" % err.args[0])
            sys.exit(-1)
        else:
            createDatabase(file_path)
        finally:
            if conn:
                conn.close()
    else:
        return file_path


if __name__ == '__main__':
    # createDatabase()
    database_file = get_database_file()
    mainmenu = True
    keluar = False
    search_name = False
    search_jdm = False
    search_som = False
    search_komisi = False
    columnPicked.clear()
    printColumn.clear()
    while True:
        print("Main menu")
        insert = False
        search = False
        edit = False
        delete = False
        anak = False
        remaja = False
        dewasa = False
        show = False
        if mainmenu:
            print("Masuk")
            Choice()
            if insert:
                Jemaat()
                if anak:
                    Anak()
                elif remaja:
                    Remaja()
                elif dewasa:
                    Dewasa()
            elif search:
                Search()
                if search_name:
                    SearchName()
                    if show:
                        ShowResults()
                    print("Show")
                elif search_jdm:
                    SearchJDM()
                    if show:
                        ShowResults()
                elif search_komisi:
                    SearchKomisi()
                    if show:
                        ShowResults()
                elif search_som:
                    SearchSOM()
                    if show:
                        ShowResults()
            elif edit:
                Edit()
                if anak:
                    UpdateAnak()
                elif remaja:
                    UpdateRemaja()
                elif dewasa:
                    UpdateDewasa()
            elif delete:
                Delete()

        elif keluar:
            print("Keluar")
            break

    sys.exit()
