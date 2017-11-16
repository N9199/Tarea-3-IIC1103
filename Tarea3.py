#To-do:
#Do save method
#Do optimized backtracking (maybe DP)(Haven't even started)
import tkinter as tk
import math
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
            c = b.lower()
            self.stats[a] = b
            self.stats[b] = a
            self.stats[c] = a
        self.build_GUI()
        self.start()

    def start(self):
        self.count = 3
        self.load()
        self.character = Personaje(self, self.puntos, self.base, self.tiempo, quick=True)
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
        while len(file)<5:
            messagebox.showerror("Error", "Archivo seleccionado no válido.")
            file = askopenfilename()
        while file[-4:]!=".txt":
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
        self.saved = self.tests+self.consumables+self.equipment

    def save(self):
        file = simpledialog.askstring("Guardar estadísticas","Como desea que se llame el archivo de las estadísticas?")
        if len(file)<4:
            file+=".txt"
        elif file[-4:]!=".txt":
            file+=".txt"
        with open(file, mode='w') as f:
            f.write(self.character.atributos[0]+'\n')
            f.write(str(self.character.vida)+",")
            for i in range(2,len(self.character.atributos)):
                f.write(str(self.character.atributos[i])+",")
            f.write(str(self.character.tiempo)+'\n')
            for item in self.character.atributos:
                if item==self.character.atributos[0]:
                    continue
                if item!=self.character.atributos[-1]:
                    f.write(str(item)+",")
                else:
                    f.write(str(item)+"\n")
            f.write(str(self.atributos[1]-self.character.vida)+'\n')
            for i in range(3):
                if i<2:
                    f.write(self.saved[i].nombre+",")
                else:
                    f.write(self.saved[i].nombre+"\n")
            temp1 = []
            for i in range(3,len(self.saved)):
                if self.saved[i] is Consumible:
                    if not(self.saved[i] in temp1):
                        temp1.append(self.saved[i])
                        f.write(str(self.saved[i])+","+str(self.saved.count(self.saved[i])-self.consumables.count(self.saved[i]))+"\n")
                elif self.saved[i] is Equipamiento:
                    if not (self.saved[i] in self.equipment):
                        f.write(str(self.saved[i])+"\n")
            f.write(str(self.character.tiempo-self.character.tiempo2))


    def build_GUI(self):
        self.info = []
        buttons = tk.Frame(self, pady=5, padx=10)
        self.turn = tk.Button(buttons, text="Equipar", command = self._equip)
        self.Test = tk.Button(buttons, text="Dar Interrogación", state = tk.DISABLED, command=self.test)
        self.Test.pack(side="right")
        self.turn.pack(side="right")
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
        self.cons = tk.Listbox(frame, selectmode=tk.SINGLE, height=11, yscrollcommand=yScroll, width = 50)
        self.cons.pack(side="left")
        frame.pack(side="right")

    def test(self):
        test = self.tests.pop(0)
        messagebox.showinfo(message=str(test))
        self.character.taketest(test)
        self.updatestats()
        if self.character.atributos[1]<=0:
            messagebox.showinfo(message="Perdiste")
            self.quit()
        else:
            if (-self.character.delta):
                messagebox.showinfo("Resumen de la Interrogación","Lo lograste, pero perdiste "+str(-self.character.delta)+" puntos de vida")
            else:
                messagebox.showinfo("Resumen de la Interrogación","Lo lograste, te sacaste un 7!")
        if len(self.tests)==0:
            messagebox.showinfo("Felicitaciones", "Has ganado!")
        self.turn.config(state = tk.ACTIVE)
        self.count = 3

    def consume(self):
        temp = self.cons.curselection()
        temp = temp[0]
        asdf = self.cons.get(temp)
        if asdf[0]=="1":
            self.cons.delete(temp)
        else:
            self.cons.delete(temp)
            self.cons.insert(temp, str(int(asdf[0])-1)+asdf[1:])
        for i in range(len(self.consumables)):
            if str(self.consumables[i])==asdf[2:]:
                self.character.consume(self.consumables[i])
                del self.consumables[i]
                break
        self.count -= 1
        if self.count <= 0:
            self.turn.config(state = tk.DISABLED)
        self.updatestats()

    def _equip(self):
        temp = self.cons.curselection()
        temp = temp[0]
        self.character.equip(self.equipment[temp])
        self.cons.delete(temp)
        del self.equipment[temp]
        if len(self.character.equipment)>=3:
            self.Test.config(state = tk.ACTIVE)
            self.turn.config(command=self.consume, text="Consumir")
            self.cons.delete(0,tk.END)
            temp = []
            for item in self.consumables:
                b = True
                if len(temp)!=0:
                    for a in temp:
                        if str(item)==str(a[0]):
                            a.append(item)
                            b = False
                            break
                if b:
                    temp.append([item])
            
            asdf = ""
            for item in temp:
                self.cons.insert(tk.END, (str(len(item))+" "+str(item[0])))
        self.updatestats()

    def updatestats(self):
        for i in range(6):
            temp = self.info[i].get()
            temp = temp.split(" ")
            if i>1:
                self.info[i].set(temp[0]+" "+str(math.floor(self.character.atributos[i]*self.character.bon[i-2]))+" Bonus: "+str(self.character.temp[i-2]))
            else:
                self.info[i].set(temp[0]+" "+str(self.character.atributos[i]))

class Personaje:

    def __init__(self, master, puntos, vida, tiempo, quick=False):
        self.vida = int(vida)
        self.tiempo = int(tiempo)
        self.tiempo1 = int(tiempo)
        self.tiempo2 = self.tiempo
        self.puntos = int(puntos)
        self.temp = 4*[0]
        self.bon = 4*[1]
        self.equipment = []
        self.consumables = []
        self.master = master
        self.stats = self.master.stats
        self.delta = 0
        if quick:
            self.atributos = ["a"]+5*[0]
            temp = self.puntos
            for i in range(1,5):
                self.atributos[i]+=math.floor(self.puntos/5)
                temp -= math.floor(self.puntos/5)
            self.atributos[5]+= temp
        else:
            self.new()

    def new(self):
        self.atributos = 6*[None]
        self.ask = tk.Toplevel(self.master)
        self.pointsleft = tk.StringVar(value=str(self.puntos))
        
        #for a,b in self.stats.items():
            #print(a,b)
        self.atributos[0] = simpledialog.askstring("Nombre", "Por favor ingrese el nombre del personaje")
        while self.atributos[0] == None or self.atributos[0] == "":
            self.atributos[0] = simpledialog.askstring("Nombre", "Por favor ingrese el nombre del personaje")

        messagebox.showinfo("Información","Distribuye los puntos en los stats iniciales (Tienes: "+str(self.puntos)+" puntos,"+str(self.vida)+" vida base)")
        asdfhjk = tk.Label(self.ask, text="0", textvariable = self.pointsleft)
        asdfhjk.pack(side="top")
        self.pointsleft.set(value="Puntos restantes: "+str(self.puntos))
        self.values = []
        scales = []
        group_master = tk.Frame(self.ask)
        for i in range(5):
            asdf = tk.Frame(group_master, padx=20)
            b = tk.IntVar()
            a = tk.Scale(asdf, to = 0, from_ = self.puntos, variable = b, command = self.updatelabel)
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
    
    def updatelabel(self, points):
        temp = self.puntos
        for item in self.values:
            temp-=item.get()
        self.pointsleft.set("Puntos restantes: "+str(temp))

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
                self.vida = self.atributos[1]
                self.ask.destroy()
                self.master.focus_set()
    
    def taketest(self, test):
        messagebox.showinfo("Resumen Interrogación","Gastaste "+str(self.tiempo2-self.tiempo)+" puntos de tiempo")
        self.delta=0
        temp = 0
        temp += math.floor(self.bon[0]*self.atributos[2])+self.temp[0]-int(test.destreza)
        temp += math.floor(self.bon[1]*self.atributos[3])+self.temp[1]-int(test.resistencia)
        temp += math.floor(self.bon[2]*self.atributos[4])+self.temp[2]-int(test.suerte)
        temp += math.floor(self.bon[3]*self.atributos[5])+self.temp[3]-int(test.inteligencia)
        
        if temp < 0:
            if self.atributos[int(self.stats[test.debilidad])+1]==0:
                self.delta = temp*int(test.vida)
            else:
                self.delta = temp*(int(test.vida)//self.atributos[int(self.stats[test.debilidad])])
            self.atributos[1]+=self.delta
        self.temp = 4*[0]
        self.consumables = []
        self.tiempo2 = self.tiempo1
            
    def consume(self, consumable):
        self.tiempo1-=consumable.costo
        self.temp[self.stats[consumable.atributo]-1]+=consumable.tempbon
        self.consumables.append(consumable)

    def equip(self, equipment):
        self.bon[self.stats[str(equipment.atributo)]-1]+=equipment.bon
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

    def __str__(self):
        return str(self.nombre)+": V:"+str(self.vida)+" D:"+str(self.destreza)+" R:"+str(self.resistencia)+" I:"+str(self.inteligencia)+" S:"+str(self.suerte)+" Debilidad:"+str(self.debilidad)

class Consumible:
    def __init__(self, parameter_list):
        self.nombre = parameter_list[0]
        self.atributo = parameter_list[1]
        self.tempbon = int(parameter_list[2])
        self.costo = int(parameter_list[3])

    def __str__(self):
        return str(self.nombre)+": Costo de tiempo "+str(self.costo)+" Bonus "+str(self.tempbon)+" a "+self.atributo

class Equipamiento:
    def __init__(self, parameter_list):
        self.nombre = parameter_list[0]
        self.atributo = parameter_list[1]
        self.bon = float(parameter_list[2])

    def __str__(self):
        return str(self.nombre)+": Bonus de "+str(self.bon)+" a "+self.atributo

sim = Simulacion()
sim.mainloop()
