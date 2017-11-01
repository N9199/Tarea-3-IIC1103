#To-do:
#Fill classes
#Design GUI
#Program interactions
#Do optimized backtracking (maybe DP)
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

class Simulacion(tk.Frame):

    def __init__(self, parameter_list=None, master=None):
        super().__init__(master)
        self.pack()
        self.stats = {}
        temp = {}
        temp[0] = "Vida"
        temp[1] = "Destreza"
        temp[2] = "Resistencia"
        temp[3] = "Suerte"
        temp[4] = "Inteligencia"

        for a, b in temp.items():
            self.stats[a] = b
            self.stats[b] = a
        self.build_GUI()
        self.start()

    def start(self):
        self.character = Personaje(self, 100)
        for i in range(6):
            temp = self.info[i].get()
            temp = temp.split(" ")
            self.info[i].set(temp[0]+" "+str(self.character.atributos[i]))


    def load(self):
        pass

    def save(self):
        pass
    
    def build_GUI(self):
        self.info = []
        self.Test = tk.Button(self, text="Dar Interrogación")
        self.Test.pack(side="bottom")
        frame = tk.Frame(self, padx=20)
        stats = tk.LabelFrame(master=self, text="Stats", pady=5, padx=20)
        var = tk.StringVar()
        var.set("Nombre: ")
        label = tk.Label(stats,justify = tk.LEFT, pady=5, padx=10, textvariable = var)
        self.info.append(var)
        label.pack(side="top")
        for i in range(5):
            var = tk.StringVar()
            var.set(self.stats[i]+": ")
            label = tk.Label(stats,justify = tk.LEFT, pady=5, padx=10, textvariable = var)
            self.info.append(var)
            label.pack(side="top")
        
        stats.pack(side="left")
        yScroll = tk.Scrollbar(frame, orient=tk.VERTICAL)
        yScroll.pack(side="right")
        self.cons = tk.Listbox(frame, height=11, yscrollcommand=yScroll)
        self.cons.pack(side="left")
        frame.pack(side="right")
    
    def turn(self):
        pass

class Personaje:

    def __init__(self, master, puntos, quick = False):
        self.puntos = puntos
        self.master = master
        if quick:
            pass
        else:
            self.new()
        
    def new(self):
        self.atributos = 6*[None]
        self.ask = tk.Toplevel(self.master)
        self.stats = self.master.stats
        #for a,b in self.stats.items():
            #print(a,b)
        self.atributos[0] = simpledialog.askstring("Nombre", "Por favor ingrese el nombre del personaje")
        while(self.atributos[0] == None or self.atributos[0] == ""):
            self.atributos[0] = simpledialog.askstring("Nombre", "Por favor ingrese el nombre del personaje")
        
        messagebox.showinfo("Información","Distribuya los puntos en sus atributos (Tiene: "+str(self.puntos)+" puntos)")
        self.values = []
        scales = []
        group_master = tk.Frame(self.ask)
        for i in range(5):
            asdf = tk.Frame(group_master, padx=20)
            b = tk.IntVar()
            a = tk.Scale(asdf, to = 0, from_ = self.puntos, variable = b)
            m = tk.Label(asdf, text=self.stats[i])
            a.pack(padx=10, side="bottom")
            m.pack(pady=10, side="bottom")
            asdf.pack(side="left")
            scales.append(a)
            self.values.append(b)
        tempbut = tk.Button(self.ask, text="Confirmar", command=self.check)
        tempbut.pack(side="bottom")
        group_master.pack(side="bottom")
        
        self.ask.protocol("WM_DELETE_WINDOW", self.check)
        self.ask.focus_set()
        self.ask.grab_set()
        self.ask.wait_window(self.ask)
    
    def check(self):
        for i in range(5):
            self.atributos[i+1] = self.values[i].get()

        if None in self.atributos:
            messagebox.showerror("Error","Mal ingresado")
        else:
            sum = 0
            for i in range(1,6):
                sum+=self.atributos[i]
            if sum!=self.puntos:
                messagebox.showerror("Error","Puntos mal distribuidos")
            else:
                self.ask.destroy()
                self.master.focus_set()
    
    def taketest(self, test):
        pass
            
            

class Prueba:
    def __init__(self, parameter_list):
        self.destreza = NotImplemented
        self.resistencia = NotImplemented
        self.suerte = NotImplemented
        self.inteligencia = NotImplemented

class Consumible:
    def __init__(self, parameter_list):
        self.nombre = NotImplemented
        self.atributo = NotImplemented
        self.tempbon = NotImplemented

class Equipamiento:
    def __init__(self, parameter_list):
        self.nombre = NotImplemented
        self.atributo = NotImplemented
        self.bon = NotImplemented

sim = Simulacion()
sim.mainloop()