from tkinter import *
import customtkinter

from utils.base import open_json, resource_path
from utils.constants import TOTALCOLUNAS

class Model:
    data =  open_json(resource_path('data/db.json'))

class Frame(LabelFrame):
    global TOTALCOLUNAS

    def __init__(self, window, title):
        super().__init__(window, text=title, padx=5, pady=5)
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)


class CabecalhoFrame(Frame):
    def __init__(self, window):
        super().__init__(window, "INÍCIO DA ANALISE")
        self.grid(column=0, row=1, padx=5, pady=5, columnspan=2, sticky="nswe")

class MainText(customtkinter.CTkTextbox):
    def __init__(self, window):
        super().__init__(window, height=300, wrap="word", font=customtkinter.CTkFont(size=14))
        self.grid(column=0, row=2, columnspan=TOTALCOLUNAS, sticky="nswe")


class TvFrame(Frame):
    def __init__(self, window):
        super().__init__(window, "TV")
        self.grid(column=0, row=3, padx=5, pady=5, columnspan=2, sticky="nswe")

class OnuFrame(Frame):
    def __init__(self, window):
        super().__init__(window, "ONU")
        self.grid(column=0, row=4, padx=5, pady=5,
                  columnspan=TOTALCOLUNAS, sticky="nswe")

class PppoeFrame(Frame):
    def __init__(self, window):
        super().__init__(window, "PPPoE")

class FinalFrame(Frame):
    def __init__(self, window):
        super().__init__(window, "FINALIZAÇÃO")

class RodapeFrame(Frame):
    def __init__(self, window):
        super().__init__(window, "")
        self.grid(column=0, row=10, padx=10, pady=0,
                  columnspan=TOTALCOLUNAS, sticky="nswe")


class Gap(Label):
    def __init__(self, window, width):
        super().__init__(window, text="", width=width)
        window.add_widget(self)


class GapCabecalho(Gap):
    def __init__(self, window):
        super().__init__(window, width=60)
        self.grid(row=0, column=4)


class GapInternet(Gap):
    def __init__(self, window):
        super().__init__(window, width=23)
        self.grid(row=0, column=TOTALCOLUNAS - 2)


class GapFinal(Gap):
    def __init__(self, window):
        super().__init__(window, width=18)

class ButtonClear(customtkinter.CTkButton):
    def __init__(self, window, command):
        super().__init__(window, text="LIMPAR", command=command, fg_color="red", hover_color="#d94545", width=95)
        window.add_widget(self)

class ButtonCopy(customtkinter.CTkButton):
    def __init__(self, window, command):
        super().__init__(window, text="COPIAR", command=command, width=95)
        window.add_widget(self)


class RadioButton(customtkinter.CTkRadioButton):
    def __init__(self, window, text, variable, value, command):
        super().__init__(window, text=text, variable=variable, value=value, command=command)
        window.add_widget(self)

class RadioButtonRetida(RadioButton):
    def __init__(self, window, variable, command):
        super().__init__(window, text="SAC N2", variable=variable, value=1, command=command)

class RadioButtonAssistencia(RadioButton):
    def __init__(self, window, variable, command):
        super().__init__(window, text="ASSISTÊNCIA", variable=variable, value=2, command=command)

class RadioButtonCancelada(RadioButton):
    def __init__(self, window, variable, command):
        super().__init__(window, text="CANCELADA", variable=variable, value=3, command=command)

class ComboBox(customtkinter.CTkComboBox):
    def __init__(self, window, values, command):
        super().__init__(window, width = 157, values=values, state="readonly", command=command)
        window.add_widget(self)

class ComboBoxProblema(ComboBox):
    def __init__(self, window, command):
        super().__init__(window, values=Model.data["PROBLEMAS"], command=command)
        self.grid(column=0,row=0, padx=5, pady=5)
        

class ComboBoxUser(ComboBox):
    def __init__(self, window, command):
        super().__init__(window, values=Model.data["USUÁRIOS"], command=command)
        self.set(Model.data["USUÁRIOS"][7])
        self.grid(column=TOTALCOLUNAS - 1, row=0, padx=5, pady=5, sticky="e")

class ComboBoxOnu(ComboBox):
    def __init__(self, window, combo, command):
        super().__init__(window, values=list(Model.data["INTERNET"]["ONU"][combo].keys()), command=command)
        self.set(list(Model.data["INTERNET"]["ONU"][combo].keys())[0])

class ComboBoxRT(ComboBox):
    def __init__(self, window, combo, command):
        super().__init__(window, values=list(Model.data["INTERNET"]["RT"][combo].keys()), command=command)
        self.set(list(Model.data["INTERNET"]["RT"][combo].keys())[0])

class ComboBoxTecnologia(ComboBox):
    def __init__(self, window, command):
        super().__init__(window, values=list(Model.data["TV"].keys()), command=command)
        self.set(list(Model.data["TV"].keys())[0])

class ComboBoxTV2(ComboBox):
    def __init__(self, window, command, tec = "COAXIAL"):
        super().__init__(window, values=list(Model.data["TV"][tec].keys()), command=command)
        self.set(list(Model.data["TV"]["COAXIAL"].keys())[0])

class Switch(customtkinter.CTkSwitch):
    def __init__(self, window, command):
        super().__init__(window, command=command, text="LENTIDÃO", state="disable")
        window.add_widget(self)