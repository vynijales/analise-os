from tkinter import StringVar, Label
import customtkinter

from models.frame import *
from models.comboBox import *
from models.switch import *
from models.button import *

from components.controller import Controller
from components.models import Model
from utils.base import resource_path
from utils.constants import TOTALCOLUNAS

from components.models import *


class View:

    def adjust_window_size(self):
        self.window.geometry('849x1')
        self.window.resizable(False, False)

    def adjust_window_height(self):
        self.window.update_idletasks()
        height = self.window.winfo_reqheight()
        self.window.geometry('849x' + str(height))

    def __init__(self):
        self.setup()
        self.createFrames()
        self.variable = StringVar()
        self.createWidgets()
        self.adjust_window_height()

        

    def setup(self):
        self.window = customtkinter.CTk()
        self.adjust_window_size()
        self.window.iconbitmap(resource_path('assets/img/icon.ico'))
        self.title = "ANÁLISE DE OS - SISTEMA OESTE DE COMUNICAÇÃO LTDA"
        self.window.title(self.title)
        self.window.resizable(False, False)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

    def createFrames(self):
        self.HeaderFrame = Frame(master=self.window, title="INÍCIO DA ANALISE")
        self.Payload = Payload(self.window)
        self.OnuFrame = Frame(master=self.window, title="ONU")
        self.RtFrame = Frame(master=self.window, title="RT")
        self.TvFrame = Frame(master=self.window, title="TV")
        self.FinalFrame = Frame(master=self.window, title="FINALIZAÇÃO")
        
        self.HeaderFrame.pack(side="top", fill="both", expand=True)
        self.Payload.pack(side="top", fill="both", expand=True)
        self.createSectionTv()
        self.createSectionInternet()
        self.createSectionFinal()

    def createSectionTv(self):
        self.TvFrame.pack(side="top",fill="both", expand=True)
        self.TvFrame.renderWidgets()

    def createWidgetsOnu(self):
        self.OnuFrame.renderWidgets()

    def createWidgetsRt(self):
        self.RtFrame.renderWidgets(3)

    def createSectionInternet(self):
        self.OnuFrame.pack(side="top", fill="both", expand=True)
        self.RtFrame.pack(side="top", fill="both", expand=True)
        self.createWidgetsOnu()
        self.createWidgetsRt()

    def createSectionFinal(self):
        self.lbRodape = Label(
            master=self.window, text="Contact for support or further information: vynijales@gmail.com.")
        self.lbRodape.pack(side="bottom", fill="both", expand=True)
        self.FinalFrame.pack(side="bottom", fill="both", expand=True)  # Position at the bottom

    def createWidgets(self):
        self.comboBoxProblema = ComboBoxProblema(
            self.HeaderFrame, command=lambda value: Controller.atualizar(self, value))
        self.comboBoxUser = ComboBoxUser(
            self.HeaderFrame, command=lambda value: Controller.atualizar(self, value))
        self.HeaderFrame.renderWidgets()
        self.comboBoxUser.pack(side="right")

        self.comboBoxOnu = [ComboBoxOnu(self.OnuFrame, combo, command=lambda value: Controller.atualizar(
            self, value)) for combo in list(Model.data["INTERNET"]["ONU"].keys())]

        self.comboBoxRt = [ComboBoxRT(self.RtFrame, combo, command=lambda value: Controller.atualizar(
            self, value)) for combo in list(Model.data["INTERNET"]["RT"].keys())]
        self.comboBoxTecnologia = ComboBoxTecnologia(
            self.TvFrame, command=lambda value: Controller.atualizar(self, value))
        self.comboBoxTV2 = ComboBoxTV2(
            self.TvFrame, command=lambda value: Controller.atualizar(self, value))
        self.swLentidao = Switch(
            self.RtFrame, command=lambda: Controller.atualizar(self, self))
        
        self.radioButtonRetida = RadioButtonRetida(
            self.FinalFrame, self.variable, lambda: Controller.atualizar(self, 'retida'))
        self.radioButtonAssistencia = RadioButtonAssistencia(
            self.FinalFrame, self.variable, lambda: Controller.atualizar(self, 'assistencia'))
        self.radioButtonCancelada = RadioButtonCancelada(
            self.FinalFrame, self.variable, lambda: Controller.atualizar(self, 'cancelada'))
        self.buttonClear = ButtonClear(self.FinalFrame, command=self.reset)
        self.buttonCopy = ButtonCopy(
            self.FinalFrame, command=lambda: Controller.ctrlc(self))
        
        self.FinalFrame.renderWidgets(3)


    def getInternet(self):
        text = ""
        INTERNET = Model.data["INTERNET"]

        for comboBox in (self.comboBoxOnu):
            for key in Model.data["INTERNET"]["ONU"].keys():
                for element in INTERNET["ONU"][key]:
                    if comboBox.get() == element:
                        text += " " + INTERNET["ONU"][key][element]

        # Checando as entradas de todos os COMBOBOX do Frame PPPoE e gerando o texto da internet
        for comboBox in (self.comboBoxRt):
            for key in Model.data["INTERNET"]["RT"].keys():
                for element in INTERNET["RT"][key]:
                    if comboBox.get() == element:
                        text += " " + INTERNET["RT"][key][element]

        text += Model.data["LENTIDÃO"]["C/ LENTIDÃO" if self.swLentidao.get()
                                              else "S/ LENTIDÃO"]

        return text

    def getTv(self):
        text = ""
        TV = Model.data["TV"]
        tecnologia = self.comboBoxTecnologia.get()
        if tecnologia in TV:
            self.comboBoxTV2.configure(values=list(TV[tecnologia].keys()))
            if self.comboBoxTV2.get() not in TV[tecnologia].keys():
                self.comboBoxTV2.set(list(TV[tecnologia].keys())[0])

        for comboBox in [self.comboBoxTV2]:
            for key in TV.keys():
                for element in TV[key]:
                    if comboBox.get() == element:
                        text += " " + TV[key][element]

        return text

    def deselect_all_radio_buttons(self, variable):
        for widget in self.FinalFrame.winfo_children():
            if isinstance(widget, customtkinter.CTkRadioButton):
                widget.deselect()
        

    def reset(self):
        self.comboBoxProblema.set("")
        self.comboBoxUser.set("")
        self.Payload.delete("1.0", "end")

        # Deselect all radio buttons associated with the same variable
        self.deselect_all_radio_buttons(self.variable)

        Model.data["ANALISE"]["FINALIZACAO"] = ""

        self.swLentidao.deselect()
        self.OnuFrame.pack_forget()
        self.RtFrame.pack_forget()
        self.TvFrame.pack_forget()
        self.adjust_window_height()
