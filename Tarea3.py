#To-do:
#Fill classes (One is mostly ready)
#Design GUI (Kinda ready)
#Program interactions (Some are working)
#Do optimized backtracking (maybe DP)(Haven't even started)
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
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
        self.load()
        self.character = Personaje(self, self.puntos, self.base, self.tiempo)
        for i in range(6):
            temp = self.info[i].get()
            temp = temp.split(" ")
            self.info[i].set(temp[0]+" "+str(self.character.atributos[i]))
        for equip in self.equipment:
            self.cons.insert(tk.END, equip)

    def load(self):
        file = askopenfilename()
        if file == "":
            return
        if len(file)<5:
            messagebox.showerror("Error", "Archivo seleccionado no válido.")
            file = askopenfilename()
        if file[-4:]!=".txt":
            messagebox.showerror("Error", "Archivo seleccionado no válido.")
            file = askopenfilename()
        
        with open(file, 'r') as f:
            data = f.readlines()
        temp = data[0][:-1].split(',')
        self.base = temp[0]
        self.tiempo = temp[1]
        self.puntos = temp[2]
        temp = data[1][:-1].split(',')
        self.consumables = []
        self.equipment = []
        self.tests = []
        for i in range(2,int(temp[0])+2):
            a = data[i][:-1].split(',')
            con = Consumible([a[0]]+a[2:])
            self.consumables += int(a[1])*[con]
        
        for i in range(2+int(temp[0]),2+int(temp[0])+int(temp[1])):
            a = data[i][:-1].split(',')
            equip = Equipamiento(a)
            self.equipment.append(equip)
        for i in range(-3,0):
            a = data[i][:-1].split(',')
            test = Prueba(a)
            self.tests.append(test)

    def save(self):
        pass

    def build_GUI(self):
        self.info = []
        buttons = tk.Frame(self, pady=5, padx=10)
        self.con = tk.Button(buttons, text="Consumir", state = tk.DISABLED, command=self.consume)
        self.equip = tk.Button(buttons, text="Equipar", command = self._equip)
        self.Test = tk.Button(buttons, text="Dar Interrogación", state = tk.DISABLED, command=self.test)
        self.Test.pack(side="right")
        self.equip.pack(side="right")
        self.con.pack(side="right")
        buttons.pack(side="bottom")
        frame = tk.Frame(self, padx=20)
        stats = tk.LabelFrame(master=self, text="Stats", pady=5, padx=20)
        var = tk.StringVar()
        var.set("Nombre: ")
        label = tk.Label(stats, justify=tk.LEFT, pady=5, padx=10, textvariable=var)
        self.info.append(var)
        label.pack(side="top")
        for i in range(5):
            var = tk.StringVar()
            var.set(self.stats[i]+": ")
            label = tk.Label(stats, justify=tk.LEFT, pady=5, padx=10, textvariable=var)
            self.info.append(var)
            label.pack(side="top")

        stats.pack(side="left")
        yScroll = tk.Scrollbar(frame, orient=tk.VERTICAL)
        yScroll.pack(side="right")
        self.cons = tk.Listbox(frame, selectmode=tk.SINGLE, height=11, yscrollcommand=yScroll, width = 40)
        self.cons.pack(side="left")
        frame.pack(side="right")

    def test(self):
        test = self.tests.pop(0)
        self.character.taketest(test)
        if self.character.atributos[1]<=0:
            messagebox.showinfo(message="Perdiste")
            self.quit()
        elif len(self.tests)>1:
            if self.character.delta:
                messagebox.showinfo("Resumen de la Interrogación","Lo lograste, pero perdiste "+str(self.character.delta)+" puntos de vida")
            else:
                messagebox.showinfo("Resumen de la Interrogación","Lo lograste, te sacaste un 7!")
            

    def consume(self):
        pass

    def _equip(self):
        pass

    def updatestats(self):
        for i in range(6):
            temp = self.info[i].get()
            temp = temp.split(" ")
            self.info[i].set(temp[0]+" "+str(self.character.atributos[i]))

class Personaje:

    def __init__(self, master, puntos, vida, tiempo, quick=False):
        self.vida = int(vida)
        self.tiempo = int(tiempo)
        self.puntos = int(puntos)
        self.master = master
        self.delta = 0
        if quick:
            pass
        else:
            self.new()

    def new(self):
        self.atributos = 6*[None]
        self.temp = 4*[0]
        self.bon = 4*[1]
        self.equipment = []
        self.consumables = []
        self.ask = tk.Toplevel(self.master)
        self.stats = self.master.stats
        #for a,b in self.stats.items():
            #print(a,b)
        self.atributos[0] = simpledialog.askstring("Nombre", "Por favor ingrese el nombre del personaje")
        while self.atributos[0] == None or self.atributos[0] == "":
            self.atributos[0] = simpledialog.askstring("Nombre", "Por favor ingrese el nombre del personaje")

        messagebox.showinfo("Información","Distribuye los puntos en los stats iniciales (Tienes: "+str(self.puntos)+" puntos,"+str(self.vida)+" vida base)")
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
                #print(self.atributos[i])
            #messagebox.showinfo(message = str(sum)+" "+str(self.puntos))
            if sum!=self.puntos:
                messagebox.showerror("Error","Puntos mal distribuidos")
            else:
                self.atributos[1]+=self.vida
                self.ask.destroy()
                self.master.focus_set()
    
    def taketest(self, test):
        self.delta=0
        temp = 0
        temp += floor(self.bon[0]*self.atributos[2])+self.temp[0]-test.destreza
        temp += floor(self.bon[1]*self.atributos[3])+self.temp[1]-test.resistencia
        temp += floor(self.bon[2]*self.atributos[4])+self.temp[2]-test.suerte
        temp += floor(self.bon[3]*self.atributos[5])+self.temp[3]-test.inteligencia
        if temp<0:
            self.delta = temp*(test.vida//self.atributos[self.stats[test.debilidad]])
            self.atributos[1]+=self.delta
        self.temp = 4*[0]
        self.consumables = []
            
    def consume(self, consumable):
        self.temp[self.stats[consumable.atributo]-1]+=consumable.tempbon
        self.consumables.append(consumable)

    def equip(self, equipment):
        self.bon[self.stats[equipment.atributo]-1]+=equipment.bon
        self.equipment.append(equipment)

class Prueba:
    def __init__(self, parameter_list):
        self.nombre = parameter_list[0]
        self.vida = parameter_list[1]
        self.destreza = parameter_list[2]
        self.resistencia = parameter_list[3]
        self.inteligencia = parameter_list[4]
        self.suerte = parameter_list[5]
        self.debilidad = parameter_list[6]

class Consumible:
    def __init__(self, parameter_list):
        self.nombre = parameter_list[0]
        self.atributo = parameter_list[1]
        self.tempbon = int(parameter_list[2])
        self.costo = int(parameter_list[3])

class Equipamiento:
    def __init__(self, parameter_list):
        self.nombre = parameter_list[0]
        self.atributo = parameter_list[1]
        self.bon = float(parameter_list[2])

    def __str__(self):
        return str(self.nombre)+": Bonificador "+str(self.bon)+" a "+self.atributo

sim = Simulacion()
sim.mainloop()
