try:
    from tkinter import *
    from tkinter import messagebox
except:
    from Tkinter import *
#import pymysql
import sqlite3
try:
    from tkinter.ttk import Treeview
except:
    from Tkinter.ttk import Treeview

class Entry_slowo(Entry):
    def __init__(self, master, *args, **kwargs):
        Entry.__init__(self, master, *args, **kwargs)
        self.master = master
        self.entry =Entry(self.master)
        self.config(validate='focusout', validatecommand = (self.register(self._validate), '%P'))

    def _validate(self, proposed_value):
        if all(x.isalpha or x == "" for x in proposed_value):
            return True
        else:
            messagebox.showwarning("Błąd wprowadzania","Podane imię jest nieprawidłowa")
            return False 

class Entry_pesel(Entry):
    def __init__(self, master, *args, **kwargs):
        Entry.__init__(self, master, *args, **kwargs)
        self.master = master
        self.entry =Entry(self.master)
        self.config(validate='focusout', validatecommand = (self.register(self._validate), '%P'))

    def _validate(self, proposed_value):
        if all(x.isnumeric or x == "" for x in proposed_value) and len(proposed_value)==11:
            return True
        else:
            messagebox.showwarning("Błąd wprowadzania","Podany PESEL jest nieprawidłowa")
            return False 

class Entry_ocena(Entry):
    def __init__(self, master, *args, **kwargs):
        Entry.__init__(self, master, *args, **kwargs)
        self.master = master
        self.entry =Entry(self.master)
        self.config(validate='focusout', validatecommand = (self.register(self._validate), '%P'))

    def _validate(self, proposed_value):
        if len(proposed_value)==3:
            if proposed_value[0].isnumeric() and proposed_value[0].isnumeric() and  proposed_value[0]=='.':
                return True
        elif len(proposed_value)==1:
            if proposed_value.isnumeric():
                return True
        messagebox.showwarning("Błąd wprowadzania","Podany ocena jest nieprawidłowa")
        return False 

class Entry_data(Entry):
    def __init__(self, master, *args, **kwargs):
        Entry.__init__(self, master, *args, **kwargs)
        self.master = master
        self.entry =Entry(self.master)
        self.config(validate='focusout', validatecommand = (self.register(self._validate), '%P'))

    def _validate(self, proposed_value):
        matrix = [1,1,1,1,0,1,1,0,1,1]
        result = True
        if len(proposed_value)==10:
            for i in range(10):
                if matrix[i]:
                    if not proposed_value[i].isnumeric:
                        result=False
                else:
                    if proposed_value[i] != '-':
                        result=False
        else:
            result=False
        if not result:
            messagebox.showwarning("Błąd wprowadzania","Podana data jest nieprawidłowa")
        return result 

class student_list_view(Frame):

    def __init__(self, master):

        Frame.__init__(self,master)
        self.master=master
        self.frame=Frame(self.master)

        self.txt1=Label(self, text="Imie")
        self.txt1.grid(row=1, column=1)

        self.txt2=Label(self, text="Nazwisko")
        self.txt2.grid(row=1,column=2)

        self.txt3=Label(self, text="Nr indeksu")
        self.txt3.grid(row=1,column=3)
        
        self.txt4=Label(self, text="Data urodzenia")
        self.txt4.grid(row=1,column=4)
        
        self.scrlb=Scrollbar(self,orient="vertical")

        self.lista1=Listbox(self,yscrollcommand=self.yscroll1,exportselection=0, selectmode=SINGLE)
        self.lista1.bind('<<ListboxSelect>>', self.on_select1)
        self.lista1.bind('<Double-Button-1>', self.prepare_to_edit)
        self.lista1.grid(row=2,column=1)

        self.lista2=Listbox(self, yscrollcommand=self.yscroll2,exportselection=0, selectmode=SINGLE)
        self.lista2.bind('<<ListboxSelect>>', self.on_select2)
        self.lista2.bind('<Double-Button-1>', self.prepare_to_edit)
        self.lista2.grid(row=2, column=2)

        self.lista3=Listbox(self, yscrollcommand=self.yscroll3,exportselection=0, selectmode=SINGLE)
        self.lista3.bind('<<ListboxSelect>>', self.on_select3)
        self.lista3.bind('<Double-Button-1>', self.prepare_to_edit)
        self.lista3.grid(row=2, column=3)

        self.lista4=Listbox(self, yscrollcommand=self.yscroll4,exportselection=0, selectmode=SINGLE)
        self.lista4.bind('<<ListboxSelect>>', self.on_select4)
        self.lista4.bind('<Double-Button-1>', self.prepare_to_edit)
        self.lista4.grid(row=2, column=4)
        
        self.dodaj1=Entry_slowo(self)
        self.dodaj1.grid(row=4, column=1)

        self.dodaj2=Entry_slowo(self)
        self.dodaj2.grid(row=4, column=2)

        self.dodaj3=Entry_pesel(self)
        self.dodaj3.grid(row=4, column=3)

        self.dodaj4=Entry_data(self)
        self.dodaj4.grid(row=4, column=4)

        self.dodaj_to=Button(self, text="Dodaj",command=self.dodaj_to_method)
        self.dodaj_to.grid(row=3, column=1)
        
        self.zmien_to=Button(self, text="Wyszukaj",command= lambda: self.wyfiltruj_studenci(self.dodaj1.get(),self.dodaj2.get(),self.dodaj3.get(),self.dodaj4.get()) )
        self.zmien_to.grid(row=5, column=1)

        self.zmien_to=Button(self, text="Wyczyść",command= self.czysc_dodaj )
        self.zmien_to.grid(row=5, column=2)
        
        self.zmien_to=Button(self, text="Edytuj",command=self.edytuj_to_method)
        self.zmien_to.grid(row=3, column=3)
        
        self.usun_to=Button(self, text="Usun",command=self.usun_to_method)
        self.usun_to.grid(row=3, column=4)

        self.dodaj_studenta_sql = "insert into studenci(imie,nazwisko,pesel,data_urodzenia) values(?, ?, ?, ?)"
        self.zmien_studenta_sql = "update studenci set imie = ?, nazwisko = ?, pesel = ?, data_urodzenia = ? where imie = ? and nazwisko = ? and  pesel = ? and data_urodzenia = ?"
        self.usun_studenta_sql = "delete from studenci where imie = ? and nazwisko = ? and  pesel = ? and data_urodzenia = ?"
        self.wyszukaj_student_sql = "Select imie, nazwisko, pesel, data_urodzenia, ROWID from studenci"
        self.wyszukaj_student_where_pesel_sql = "Select imie, nazwisko, pesel, data_urodzenia, ROWID from studenci where imie like ? and nazwisko like ? and pesel = ? and data_urodzenia like ?"
        self.wyszukaj_student_where_sql = "Select imie, nazwisko, pesel, data_urodzenia, ROWID from studenci where imie like ? and nazwisko like ? and data_urodzenia like ?"

        try:
            self.conn = sqlite3.connect('student.db')
        except Exception as ex:
            messagebox.showerror("Connect to DB failed", ex.args)
        
        self.zaladuj_studenci()
        
    def zaladuj_studenci(self):
        try:
            self.lista1.delete(0,'end')
            self.lista2.delete(0,'end')
            self.lista3.delete(0,'end')
            self.lista4.delete(0,'end')
            cursor = self.conn.cursor()
            #cursor.execute("drop table studenci")
            #cursor.execute("create table studenci (imie text, nazwisko text, pesel integer unique, data_urodzenia text)")
            #cursor.execute("drop table oceny")
            #cursor.execute("create table oceny (sid integer, kurs text, ocena text, data text, foreign key(sid) references studenci(ROWID))")
            cursor.execute(self.wyszukaj_student_sql)
            self.rows = cursor.fetchall()
            for row in self.rows:
                self.lista1.insert("end",row[0])
                self.lista2.insert("end",row[1])
                self.lista3.insert("end",row[2])
                self.lista4.insert("end",row[3])
                print(row[4])
        except Exception as ex:
            messagebox.showerror("Connect to DB failed", ex.args)
            print(ex)
            """for i in range(18):
                self.lista1.insert("end",i)
            self.lista2.insert("end","hello")
            self.lista2.insert("end","pls")
            self.lista2.insert("end","thanks")
            self.lista2.insert("end","hello")
            self.lista2.insert("end","pls")
            self.lista2.insert("end","thanks")
            self.lista2.insert("end","hello")
            self.lista2.insert("end","pls")
            self.lista2.insert("end","thanks")
            self.lista3.insert("end","world")
            self.lista3.insert("end","help")
            self.lista3.insert("end","alot")
            self.lista3.insert("end","world")
            self.lista3.insert("end","help")
            self.lista3.insert("end","alot")
            self.lista3.insert("end","world")
            self.lista3.insert("end","help")
            self.lista3.insert("end","alot")
            self.lista4.insert("end","world")
            self.lista4.insert("end","help")
            self.lista4.insert("end","alot")
            self.lista4.insert("end","world")
            self.lista4.insert("end","help")
            self.lista4.insert("end","alot")
            self.lista4.insert("end","world")
            self.lista4.insert("end","help")
            self.lista4.insert("end","alot")
            self.lista2.insert("end","hello")
            self.lista2.insert("end","pls")
            self.lista2.insert("end","thanks")
            self.lista2.insert("end","hello")
            self.lista2.insert("end","pls")
            self.lista2.insert("end","thanks")
            self.lista2.insert("end","hello")
            self.lista2.insert("end","pls")
            self.lista2.insert("end","thanks")
            self.lista3.insert("end","world")
            self.lista3.insert("end","help")
            self.lista3.insert("end","alot")
            self.lista3.insert("end","world")
            self.lista3.insert("end","help")
            self.lista3.insert("end","alot")
            self.lista3.insert("end","world")
            self.lista3.insert("end","help")
            self.lista3.insert("end","alot")
            self.lista4.insert("end","world")
            self.lista4.insert("end","help")
            self.lista4.insert("end","alot")
            self.lista4.insert("end","world")
            self.lista4.insert("end","help")
            self.lista4.insert("end","alot")
            self.lista4.insert("end","world")
            self.lista4.insert("end","help")
            self.lista4.insert("end","alot")"""

    def wyfiltruj_studenci(self, imie, nazwisko, pesel, data):
        try:
            self.imie = imie
            self.nazwisko = nazwisko
            self.pesel = pesel
            self.data = data
            self.lista1.delete(0,'end')
            self.lista2.delete(0,'end')
            self.lista3.delete(0,'end')
            self.lista4.delete(0,'end')
            cursor = self.conn.cursor()
            if self.imie is NONE or self.imie=="":
                self.imie = "%"
            if self.nazwisko is NONE or self.nazwisko=="":
                self.nazwisko = "%"
            if self.data is NONE or self.data=="":
                self.data = "%"
            print(self.imie)
            print(self.nazwisko)
            print(self.pesel)
            print(self.data)
            if self.pesel is NONE or self.pesel=="":
                print("pesel is none")
                cursor.execute(self.wyszukaj_student_where_sql,(self.imie, self.nazwisko, self.data))
                
            else:
                cursor.execute(self.wyszukaj_student_where_pesel_sql,(self.imie, self.nazwisko, self.pesel, self.data))
            self.rows = cursor.fetchall()
            for row in self.rows:
                self.lista1.insert("end",row[0])
                self.lista2.insert("end",row[1])
                self.lista3.insert("end",row[2])
                self.lista4.insert("end",row[3])
                print(row[4])
        except Exception as ex:
            messagebox.showerror("Connect to DB failed", ex.args)
            print(ex)

    def czysc_dodaj(self):
        self.dodaj1.delete(0,END)
        self.dodaj2.delete(0,END)
        self.dodaj3.delete(0,END)
        self.dodaj4.delete(0,END)

    def prepare_to_edit(self, event):
        self.czysc_dodaj()
        self.dodaj1.insert(0,self.lista1.get(self.lista1.curselection()))
        self.dodaj2.insert(0,self.lista2.get(self.lista2.curselection()))
        self.dodaj3.insert(0,self.lista3.get(self.lista3.curselection()))
        self.dodaj4.insert(0,self.lista4.get(self.lista4.curselection()))
    
    def edytuj_to_method(self):
        try:
            self.edytuj_studentaW = Toplevel(self)
            self.edytuj_studentaW.title("Student id: " + str(self.rows[(self.lista1.curselection())[0]][4]))
            self.edytuj_studenta = student_view(self.edytuj_studentaW, self.conn, self.rows[(self.lista1.curselection())[0]])
            self.edytuj_studenta.pack()
            self.edytuj_studentaW.grab_set()
            self.edytuj_studentaW.mainloop()
        except IndexError:
            messagebox.showerror("Brak zaznaczonego studenta", "Proszę wybrać studenta z listy")
            self.edytuj_studentaW.destroy()
        except Exception as ex:
            print(ex)
            self.edytuj_studentaW.destroy()

    def dodaj_to_method(self):
        if self.dodaj1.get() != "" and  self.dodaj2.get() != "" and self.dodaj3.get() != "" and self.dodaj4.get() != "":
            try:
                cursor = self.conn.cursor()
                cursor.execute(self.dodaj_studenta_sql, (self.dodaj1.get(), self.dodaj2.get(), self.dodaj3.get(), self.dodaj4.get()))
                self.conn.commit()
                self.zaladuj_studenci()
            except Exception as ex:
                print(ex)
                messagebox.showerror("Connect to DB failed", ex.args)
        else:
            messagebox.showwarning("Puste pola", "Proszę uzupełnić puste pola")

    def usun_to_method(self):
        MsgBox = messagebox.askquestion ('Usuń studenta','Czy jesteś pewien, ze chcesz usunąć studenta?',icon = 'warning')
        if MsgBox == 'yes':
            try:
                cursor = self.conn.cursor()
                cursor.execute(self.usun_studenta_sql, (self.lista1.get(self.lista1.curselection()), self.lista2.get(self.lista2.curselection()), self.lista3.get(self.lista3.curselection()), self.lista4.get(self.lista4.curselection())))
                self.conn.commit()
                self.zaladuj_studenci()
            except IndexError:
                messagebox.showerror("Brak zaznaczonego studenta", "Proszę wybrać studenta z listy")
            except Exception as ex:
                print(ex)
                messagebox.showerror("Connect to DB failed", ex.args)

    def zmien_to_method(self):
        try: #removed for use
            cursor = self.conn.cursor()
            cursor.execute(self.zmien_studenta_sql, (self.dodaj1.get(), self.dodaj2.get(), self.dodaj3.get(), self.dodaj4.get(), self.lista1.get(self.lista1.curselection()), self.lista2.get(self.lista2.curselection()), self.lista3.get(self.lista3.curselection()), self.lista4.get(self.lista4.curselection())))
            self.conn.commit()
            self.zaladuj_studenci()
        except IndexError:
            messagebox.showerror("Brak zaznaczonego studenta", "Proszę wybrać studenta z listy")
        except Exception as ex:
            print(ex)
            messagebox.showerror("Connect to DB failed", ex.args)

   
    def on_select1(self, event):
        index = self.lista1.curselection()[0]
        self.select_others(index, self.lista2, self.lista3, self.lista4)

    def on_select2(self, event):
        index = self.lista2.curselection()[0]
        self.select_others(index, self.lista1, self.lista3, self.lista4)

    def on_select3(self, event):
        index = self.lista3.curselection()[0]
        self.select_others(index, self.lista1, self.lista2, self.lista4)

    def on_select4(self, event):
        index = self
        self.lista4.curselection()[0]
        self.select_others(index, self.lista1, self.lista2, self.lista3)

    def select_others(self, index, *others):
        for listbox in others:
            listbox.selection_clear(0, listbox.size() - 1)
            listbox.selection_set(index)

    def yscroll1(self, *args):
        self.lista2.yview_moveto(args[0])
        self.lista3.yview_moveto(args[0])
        self.lista4.yview_moveto(args[0])
        self.scrlb.set(*args)

    def yscroll2(self, *args):
        self.lista1.yview_moveto(args[0])
        self.lista3.yview_moveto(args[0])
        self.lista4.yview_moveto(args[0])
        self.scrlb.set(*args)

    def yscroll3(self, *args):
        self.lista1.yview_moveto(args[0])
        self.lista2.yview_moveto(args[0])
        self.lista4.yview_moveto(args[0])
        self.scrlb.set(*args)

    def yscroll4(self, *args):
        self.lista1.yview_moveto(args[0])
        self.lista2.yview_moveto(args[0])
        self.lista3.yview_moveto(args[0])
        self.scrlb.set(*args)

    def yview(self, *args):
        self.lista1.yview(*args)
        self.lista2.yview(*args)
        self.lista3.yview(*args)
        self.lista4.yview(*args)

#############################################################################################################
#############################################################################################################

class student_view(Frame):

    def __init__(self, master, conn, student):

        Frame.__init__(self,master)
        self.master=master
        self.frame=Frame(master)
        self.student = student
        self.conn = conn

        self.sql_lista_ocen = "select kurs, ocena, data from oceny where sid = ? order by kurs"
        self.sql_dodaj_ocene = "insert into oceny(kurs, ocena, data, sid) values( ?, ?, ?, ?)"
        self.sql_usun_ocene = "delete from oceny where kurs = ? and ocena = ? and data = ? and sid = ?"
        self.sql_update_studenta = "update studenci set imie = ?, nazwisko = ?, pesel = ?, data_urodzenia = ? where imie = ? and nazwisko = ? and  pesel = ? and data_urodzenia = ?"
        self.sql_update_studenta = "update studenci set imie = ?, nazwisko = ?, pesel = ?, data_urodzenia = ? where ROWID = ?"

        self.txt1=Label(self, text="Imie")
        self.txt1.grid(row=1, column=1)

        self.txt2=Label(self, text="Nazwisko")
        self.txt2.grid(row=1,column=2)

        self.txt3=Label(self, text="PESEL")
        self.txt3.grid(row=1,column=3)
        
        self.txt4=Label(self, text="Data urodzenia")
        self.txt4.grid(row=1,column=4)

        self.imie=Entry_slowo(self)
        self.imie.grid(row=2, column=1)
        self.imie.insert(0,self.student[0])

        self.nazwisko=Entry_slowo(self)
        self.nazwisko.grid(row=2, column=2)
        self.nazwisko.insert(0,self.student[1])

        self.pesel=Entry_pesel(self)
        self.pesel.grid(row=2, column=3)
        self.pesel.insert(0,self.student[2])

        self.data_urodzenia=Entry_data(self)
        self.data_urodzenia.grid(row=2, column=4)
        self.data_urodzenia.insert(0,self.student[3])

        self.txt5=Label(self, text="Kursy")
        self.txt5.grid(row=3,column=1)
        
        self.txt6=Label(self, text="Ocena")
        self.txt6.grid(row=3,column=2)

        self.lista1=Listbox(self,yscrollcommand=self.yscroll1,exportselection=0, selectmode=SINGLE)
        self.lista1.bind('<<ListboxSelect>>', self.on_select1)
        self.lista1.bind('<Double-Button-1>', self.prepare_to_edit)
        self.lista1.grid(row=4,column=1)

        self.lista2=Listbox(self, yscrollcommand=self.yscroll2,exportselection=0, selectmode=SINGLE)
        self.lista2.bind('<<ListboxSelect>>', self.on_select2)
        self.lista2.bind('<Double-Button-1>', self.prepare_to_edit)
        self.lista2.grid(row=4, column=2)

        self.lista3=Listbox(self, yscrollcommand=self.yscroll3,exportselection=0, selectmode=SINGLE)
        self.lista3.bind('<<ListboxSelect>>', self.on_select3)
        self.lista3.bind('<Double-Button-1>', self.prepare_to_edit)
        self.lista3.grid(row=4, column=3)

        self.txt7=Label(self, text="Kurs")
        self.txt7.grid(row=5,column=1)

        self.txt8=Label(self, text="Ocena")
        self.txt8.grid(row=5,column=2)
        
        self.txt9=Label(self, text="Data wystawienia")
        self.txt9.grid(row=5,column=3)

        self.dodaj_ocene1=Entry_slowo(self)
        self.dodaj_ocene1.grid(row=6, column=1)

        self.dodaj_ocene2=Entry_ocena(self)
        self.dodaj_ocene2.grid(row=6, column=2)

        self.dodaj_ocene3=Entry_data(self)
        self.dodaj_ocene3.grid(row=6, column=3)

        self.dodaj_ocene_btn = Button(self, text = "Dodaj ocene", command=self.dodaj_ocene)
        self.dodaj_ocene_btn.grid(row=6, column =4)
        
        self.usun_ocene_btn = Button(self, text = "Usun ocene", command = self.usun_ocene)
        self.usun_ocene_btn.grid(row=4, column=4, sticky=S)
        
        self.usun_ocene_btn = Button(self, text = "Zmien dane", command = self.update_studenta)
        self.usun_ocene_btn.grid(row=3, column=4)

        self.scrlb=Scrollbar(self,orient="vertical")

        self.zaladuj_oceny()

    def zaladuj_oceny(self):
        cursor = self.conn.cursor()
        try:
            self.lista1.delete(0,'end')
            self.lista2.delete(0,'end')
            self.lista3.delete(0,'end')
            cursor.execute(self.sql_lista_ocen, (int(self.student[4]),) )
            self.rows = cursor.fetchall()
            for row in self.rows:
                self.lista1.insert("end",row[0])
                self.lista2.insert("end",row[1])
                self.lista3.insert("end",row[2])
        except Exception as ex:
            messagebox.showerror("Connect to DB failed", ex.args)
            print(ex)

    def update_studenta(self):
        if self.student[0] != self.imie.get():
            MsgBox = messagebox.askquestion ('Zmień imie?','Czy napewno zmienic imię z {} na {}?'.format(self.student[0] , self.imie.get()),icon = 'warning')
            if MsgBox == 'yes':
                self.student[0] = self.imie.get()
        if self.student[1] != self.nazwisko.get():
            MsgBox = messagebox.askquestion ('Zmień nazwisko?','Czy napewno zmienic nazwisko z {} na {}?'.format(self.student[1] , self.nazwisko.get()),icon = 'warning')
            if MsgBox == 'yes':
                self.student[1] = self.nazwisko.get()
        if self.student[2] != self.pesel.get():
            MsgBox = messagebox.askquestion ('Zmień PESEL?','Czy napewno zmienic PESEL z {} na {}?'.format(self.student[2] , self.pesel.get()),icon = 'warning')
            if MsgBox == 'yes':
                self.student[2] = self.pesel.get()
        if self.student[3] != self.data_urodzenia.get():
            MsgBox = messagebox.askquestion ('Zmień datę urodzenia?','Czy napewno zmienic datę urodzenia z {} na {}?'.format(self.student[3] , self.data_urodzenia.get()),icon = 'warning')
            if MsgBox == 'yes':
                self.student[3] = self.data_urodzenia.get()
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.sql_update_studenta,(self.student[0],self.student[1],self.student[2],self.student[3], self.student[4]))
            self.conn.commit()
            print(cursor.fetchall())
        except Exception as ex:
            print(ex)
            messagebox.showerror("Connect to DB failed", ex.args)
        
    def dodaj_ocene(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.sql_dodaj_ocene, (self.dodaj_ocene1.get(), self.dodaj_ocene2.get(), self.dodaj_ocene3.get(), self.student[4]))
            self.conn.commit()
            self.zaladuj_oceny()
        except Exception as ex:
            print(ex)
            messagebox.showerror("Connect to DB failed", ex.args)

    def usun_ocene(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(self.sql_usun_ocene, (self.lista1.get(self.lista1.curselection()), self.lista2.get(self.lista2.curselection()), self.lista3.get(self.lista3.curselection()), self.dodaj_ocene3.get()))
            self.conn.commit()
            self.zaladuj_oceny()
        except Exception as ex:
            print(ex)
            messagebox.showerror("Connect to DB failed????", ex.args)
        
    def prepare_to_edit(self, event):
        self.czysc_dodaj()
        self.dodaj_ocene1.insert(0,self.lista1.get(self.lista1.curselection()))
        self.dodaj_ocene2.insert(0,self.lista2.get(self.lista2.curselection()))
        self.dodaj_ocene3.insert(0,self.lista3.get(self.lista3.curselection()))

    def czysc_dodaj(self):
        self.dodaj_ocene1.delete(0,END)
        self.dodaj_ocene2.delete(0,END)
        self.dodaj_ocene3.delete(0,END)

    def on_select1(self, event):
        index = self.lista1.curselection()[0]
        self.select_others(index, self.lista2, self.lista3)

    def on_select2(self, event):
        index = self.lista2.curselection()[0]
        self.select_others(index, self.lista1, self.lista3)

    def on_select3(self, event):
        index = self.lista3.curselection()[0]
        self.select_others(index, self.lista1, self.lista2)

    def select_others(self, index, *others):
        for listbox in others:
            listbox.selection_clear(0, listbox.size() - 1)
            listbox.selection_set(index)

    def yscroll1(self, *args):
        self.lista2.yview_moveto(args[0])
        self.lista3.yview_moveto(args[0])
        self.scrlb.set(*args)

    def yscroll2(self, *args):
        self.lista1.yview_moveto(args[0])
        self.lista3.yview_moveto(args[0])
        self.scrlb.set(*args)

    def yscroll3(self, *args):
        self.lista1.yview_moveto(args[0])
        self.lista2.yview_moveto(args[0])
        self.scrlb.set(*args)

    def yview(self, *args):
        self.lista1.yview(*args)
        self.lista2.yview(*args)
        self.lista3.yview(*args)

root = Tk()

sv = student_list_view(root)

sv.pack()

root.mainloop()
