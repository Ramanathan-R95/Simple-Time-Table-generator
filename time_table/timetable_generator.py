import random
from tkinter import *
import mysql.connector as sql
from PIL import ImageTk, Image
import PIL.Image
from tkinter import messagebox
from tkinter import ttk
import csv

def gen(sub):
    n = []
    p = sub.copy()
    for i in range(len(sub)):
        e = random.choice(p)
        n.append(e)
        p.remove(e)
        p = sub.copy()
    k = len(sub) - c
    for i in range(k):
        n.pop()
    return n

def multigen(sub, table):
    l = []
    for i in range(6):
        new1 = []
        for j in range(c):
            new = sub.copy()
            if j == 0:
                new1.append(table[i][-1])
            else:
                for b in new1:
                    if b in new:
                        new.remove(b)
                if table[i][j] in new:
                    new.remove(table[i][j])
                e = random.choice(new)
                new1.append(e)
        l.append(new1)
    return l

def saving(n, L=None):
    sch = entrys_1.get()
    if " " in sch:
        sch = sch.replace(" ", "_")
    cls = entrys_2.get()
    con = sql.connect(host="localhost", user="root", password="rama1234", port=3306)
    if con.is_connected():
        cur = con.cursor()
        cur.execute("create database if not exists " + sch + ";")
        cur.execute("use " + sch + " ;")
        cl = "create table if not exists " + cls + "( days varchar(30)) ;"
        cur.execute(cl)
        for i in range(c):
            qu = "alter table " + cls + " add " + "peroid" + str(i) + " varchar(30);"
            cur.execute(qu)
        qu = "insert into " + cls + " values"
        v1 = ("monday",) + tuple(n[0])
        v2 = ("tuesday",) + tuple(n[1])
        v3 = ("wednesday",) + tuple(n[2])
        v4 = ("thursday",) + tuple(n[3])
        v5 = ("friday",) + tuple(n[4])
        v6 = ("saturday",) + tuple(n[5])
        query = qu + str(v1) + "," + str(v2) + "," + str(v3) + "," + str(v4) + "," + str(v5) + "," + str(v6) + ";"
        cur.execute(query)
        con.commit()
        if c > 1:
            qu2 = "insert into " + cls + " values"
            y1 = ("monday",) + tuple(L[0])
            y2 = ("tuesday",) + tuple(L[1])
            y3 = ("wednesday",) + tuple(L[2])
            y4 = ("thursday",) + tuple(L[3])
            y5 = ("friday",) + tuple(L[4])
            y6 = ("saturday",) + tuple(L[5])
            qu2 += str(y1) + "," + str(y2) + "," + str(y3) + "," + str(y4) + "," + str(y5) + "," + str(y6) + ";"
            cur.execute(qu2)
            con.commit()
        messagebox.showinfo("message", "saved successfully")

def view():
    sch = entry_1.get()
    if " " in sch:
        sch = sch.replace(" ", "_")
    cls = entry_2.get()
    con = sql.connect(host="localhost", user="root", password="rama1234", port=3306)
    if con.is_connected():
        try:
            cur = con.cursor()
            qu = "use " + sch + ";"
            cur.execute(qu)
            qu2 = "select * from " + cls + ";"
            cur.execute(qu2)
            screen4 = Tk()
            screen4.geometry("1350x800")
            screen4.config(bg="black")
            screen4.title("time table")
            t_b = cur.fetchall()
            n = t_b[:6]
            L = t_b[6:]
            sr = screen4.winfo_screenwidth()
            f = (sr * (9 / 100)) / (len(t_b[0]))
            Label(screen4, text="Section - A", font=("aharoni", 16), bg="black", fg="white").grid(row=0, column=2)
            for i in range(1, 7):
                for j in range(len(t_b[0])):
                    entry = Entry(screen4, width=int(round(f)), fg='black', font=('Arial', 12, 'bold'))
                    entry.grid(row=i, column=j)
                    entry.insert(END, n[i - 1][j])
            Label(screen4, text="Section - B", font=("aharoni", 16), bg="black", fg="white").grid(row=7, column=2)
            for z in range(6):
                for j in range(len(t_b[0])):
                    entrys = Entry(screen4, width=int(round(f)), fg='black', font=('Arial', 12, 'bold'))
                    entrys.grid(row=9 + z, column=j)
                    entrys.insert(END, L[z][j])
            screen4.mainloop()
        except:
            messagebox.showinfo("error", "no such school or class found")

def inserting():
    if c == 1:
        saving(n)
    else:
        saving(n, L)

def saving_1():
    global entrys_1
    global entrys_2
    screen5 = Tk()
    screen5.config(bg="#0080FE")
    screen5.geometry("500x400")
    screen5.title("database")
    Label(screen5, text="ENTER THE DETAILS", font=("aharoni", 18, "bold"), fg="white", bg="#0080FE").place(x=60, y=50)
    Label(screen5, text="Enter the School name", font=("aharoni", 15, "bold"), fg="white", bg="#0080FE").place(x=20, y=120)
    entrys_1 = Entry(screen5)
    entrys_1.place(x=260, y=120)
    Label(screen5, text="Enter the class ", font=("aharoni", 15, "bold"), fg="white", bg="#0080FE").place(x=20, y=180)
    Label(screen5, text="Enter the class in alphabets ", font=("aharoni", 12, "bold"), fg="white", bg="#0080FE").place(x=20, y=210)
    entrys_2 = Entry(screen5)
    entrys_2.place(x=260, y=180)
    Button(screen5, text=" ok ", font=("aharoni", 12, "bold"), bg="black", fg="white", command=inserting).place(x=190, y=280)
    screen5.mainloop()

def generate():
    global c
    global n
    global L
    subjects = entry1.get()
    try:
        c = int(entry2.get())
        sec = int(entry3.get())
        l = subjects.split()
        n = []
        for i in range(6):
            n.append(gen(l))
        if sec > 1:
            L = multigen(l, n)
        screen3 = Tk()
        screen3.geometry("1350x800")
        screen3.config(bg="black")
        screen3.title("time table ")
        sr = screen3.winfo_screenwidth()
        frame = Frame(screen3)
        frame.config(bg="black")
        frame.place(x=70, y=90, width=sr, height=420)
        Label(frame, text="Section - A", font=("aharoni", 16, "bold"), bg="black", fg="white").grid(row=0, column=2)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        f = (sr * (9 / 100)) / (c)
        for i in range(1, 7):
            entry = Entry(frame, width=int(round(f)), fg='black', font=('Arial', 12, 'bold'))
            entry.grid(row=i, column=0)
            entry.insert(END, days[i - 1])
            for j in range(c):
                entry = Entry(frame, width=int(round(f)), fg='black', font=('Arial', 12, 'bold'))
                entry.grid(row=i, column=1 + j)
                entry.insert(END, n[i - 1][j])
        if sec > 1:
            Label(frame, text="Section - B", font=("aharoni", 15), bg="black", fg="white").grid(row=8, column=2)
            for i in range(6):
                entry = Entry(frame, width=int(round(f)), fg='black', font=('Arial', 12, 'bold'))
                entry.grid(row=9 + i, column=0)
                entry.insert(END, days[i])
                for j in range(c):
                    entry = Entry(frame, width=int(round(f)), fg='black', font=('Arial', 12, 'bold'))
                    entry.grid(row=9 + i, column=1 + j)
                    entry.insert(END, L[i][j])
        Button(screen3, text=" save ", font=("aharoni", 15, "bold"), bg="green", fg="white", command=saving_1).place(x=390, y=450)
        screen3.mainloop()
    except:
        messagebox.showinfo("error", "invalid options")

def yes():
    global entry1
    global entry2
    global entry3
    screen2 = Tk()
    screen2.geometry("550x500")
    screen2.title("time table generator")
    screen2.resizable(False, False)
    screen2.config(bg="#0080FE")
    Label(screen2, text="Time Table \n Generator", font=("aharoni", 25, "bold"), fg="white", bg="#0080FE").place(x=100, y=20)
    Label(screen2, text="Enter the subjects ", font=("aharoni", 15, "bold"), fg="white", bg="#0080FE").place(x=20, y=120)
    Label(screen2, text="(enter the subjects name separated with space)", font=("aharoni", 12, "bold"), fg="white", bg="#0080FE").place(x=190, y=150)
    entry1 = Entry(screen2)
    entry1.place(x=220, y=120)
    Label(screen2, text="Enter no.of periods \n per day", font=("aharoni", 15, "bold"), fg="white", bg="#0080FE").place(x=20, y=200)
    entry2 = Entry(screen2)
    entry2.place(x=220, y=200)
    Label(screen2, text="Enter no of sections ", font=("aharoni", 15, "bold"), fg="white", bg="#0080FE").place(x=20, y=280)
    entry3 = ttk.Combobox(screen2, values=[1, 2], width=20)
    entry3.place(x=220, y=280)
    Button(screen2, text="Generate", font=("aharoni", 16, "bold"), bg="#03AC13", fg="white", command=generate).place(x=210, y=380)
    screen2.mainloop()

def no():
    global entry_1
    global entry_2
    screen3 = Tk()
    screen3.geometry("500x400")
    screen3.config(bg="black")
    screen3.title("time table viewer")
    Label(screen3, text="Enter the details to view TIME TABLE", font=("aharoni", 18, "bold"), bg="black", fg="white").place(x=15, y=23)
    Label(screen3, text="Enter School Name", font=("aharoni", 17, "bold"), fg="white", bg="black").place(x=10, y=70)
    entry_1 = Entry(screen3)
    entry_1.place(x=45, y=100)
    Label(screen3, text="Enter class", font=("aharoni", 17, "bold"), fg="white", bg="black").place(x=10, y=150)
    Label(screen3, text="in alphabets", font=("aharoni", 13), fg="white", bg="black").place(x=40, y=210)
    entry_2 = Entry(screen3)
    entry_2.place(x=45, y=180)
    Button(screen3, text="View", font=("aharoni", 14, "bold"), bg="white", fg="black", command=view).place(x=125, y=250)
    screen3.mainloop()

screen1 = Tk()
screen1.geometry("1350x800")
screen1.title("time table")
screen_width = screen1.winfo_screenwidth()
screen_height = screen1.winfo_screenheight()
canvas = Canvas(screen1, width=600, height=400)
canvas.pack()
img = PIL.Image.open(r"images\backgrd.jpg")
resized_image = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
new_image = ImageTk.PhotoImage(resized_image)
label1 = Label(screen1, image=new_image)
label1.place(x=0, y=0, relwidth=1, relheight=1)
frame1 = Frame(screen1, bg="white")
frame1.place(x=950, y=120, height=440, width=340)
Label(frame1, text="Time Table \n Generator", font=("aharoni", 30, "bold"), fg="#0080FE").place(x=70, y=20)
Button(frame1, text="Generate new", font=("times", 15), fg="white", padx=20, bg="#03AC13", command=yes,width=8).place(x=90, y=180)
Button(frame1, text=" VIEW ", font=("times", 15), fg="white", padx=20, bg="red", command=no,width=8).place(x=90, y=230)

screen1.mainloop()
