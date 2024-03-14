import customtkinter

from components.controller import Controller

from components.models import Model
from utils.base import resource_path
from utils.constants import TOTALCOLUNAS

from components.models import *


class View:
    def __init__(self):
        self.setup()
        self.createFrames()
        self.variable = StringVar()
        self.createWidgets()

    def createFrames(self):
        self.CabecalhoFrame = CabecalhoFrame(self.window)
        self.OnuFrame = OnuFrame(self.window)
        self.PppoeFrame = PppoeFrame(self.window)
        self.TvFrame = TvFrame(self.window)
        self.FinalFrame = FinalFrame(self.window)
        self.RodapeFrame = RodapeFrame(self.window)

    def setup(self):
        self.window = customtkinter.CTk()
        self.window.iconbitmap(resource_path('assets/img/icon.ico'))
        self.title = "ANÁLISE DE OS - SISTEMA OESTE DE COMUNICAÇÃO LTDA"
        self.window.title(self.title)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")

    def createSectionTv(self):
        self.TvFrame.grid(column=0, row=3, padx=5, pady=5, columnspan=2, sticky="nswe")
        for i, widget in enumerate(self.TvFrame.widgets):
            widget.grid(column=i, row=3, padx=5, pady=5, sticky="nswe")

    def createWidgetsOnu(self):
        for i, widget in enumerate(self.OnuFrame.widgets):
            widget.grid(column=(i + 1), row=0, padx=5, pady=5, sticky="nswe")

    def createWidgetsPppoe(self):
        for i, widget in enumerate(self.PppoeFrame.widgets):
            widget.grid(column=(i + 1), row=0, padx=5, pady=5, sticky="nswe")
    
    def createSectionInternet(self):
        self.OnuFrame.grid(column=0, row=4, padx=5, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe")
        self.PppoeFrame.grid(column=0, row=5, padx=5, pady=5, columnspan=2, sticky="nswe")
        self.createWidgetsOnu()
        self.createWidgetsPppoe()


    def SectionFinal(self):
        self.FinalFrame.grid(column=0, row=9, padx=5, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe")
        for i, widget in enumerate(self.FinalFrame.widgets):
            widget.grid(column=i, row=0, padx=10, pady=5)
        self.lbRodape = Label(master=self.window, text="Contact for support or further information: vynijales@gmail.com.")
        self.lbRodape.grid(row=11, column=0, columnspan=TOTALCOLUNAS, sticky="nsew")

    def createWidgets(self):
        
        self.mainText = MainText(self.window)

        self.gapCabecalho = GapCabecalho(self.CabecalhoFrame)
        self.comboBoxProblema = ComboBoxProblema(self.CabecalhoFrame, command=lambda value: Controller.atualizar(self, value))
        self.comboBoxUser = ComboBoxUser(self.CabecalhoFrame, command=lambda value: Controller.atualizar(self, value))

        self.comboBoxOnu = [ComboBoxOnu(self.OnuFrame, combo, command=lambda value: Controller.atualizar(self, value)) for combo in list(Model.data["INTERNET"]["ONU"].keys())]

        self.comboBoxRt = [ComboBoxRT(self.PppoeFrame, combo, command=lambda value: Controller.atualizar(self, value)) for combo in list(Model.data["INTERNET"]["RT"].keys())]
        self.comboBoxTecnologia = ComboBoxTecnologia(self.TvFrame, command=lambda value: Controller.atualizar(self, value))
        self.comboBoxTV2 = ComboBoxTV2(self.TvFrame, command=lambda value: Controller.atualizar(self, value))
        self.gapInternet = GapInternet(self.PppoeFrame)
        self.swLentidao = Switch(self.PppoeFrame, command= lambda: Controller.atualizar(self, self))

        self.radioButtonRetida = RadioButtonRetida(self.FinalFrame, self.variable, lambda: Controller.atualizar(self, 'retida'))
        self.radioButtonAssistencia = RadioButtonAssistencia(self.FinalFrame, self.variable, lambda: Controller.atualizar(self, 'assistencia'))
        self.radioButtonCancelada = RadioButtonCancelada(self.FinalFrame, self.variable, lambda: Controller.atualizar(self, 'cancelada'))
        self.gapFinal = GapFinal(self.FinalFrame)
        self.buttonClear = ButtonClear(self.FinalFrame, command= self.reset)
        self.buttonCopy = ButtonCopy(self.FinalFrame, command= lambda: Controller.ctrlc(self, self.mainText))


    def getInternet(self):
        situacaoNET = ""
        # Recebendo valores do banco de informação
        INTERNET = Model.data["INTERNET"]

        if "INTERNET" in self.comboBoxProblema.get():
            self.createSectionInternet()  # Organizando os FRAMES de ONU e PPPoE

            # Checando as entradas de todos os COMBOBOX do Frame ONU e gerando o texto da internet
            for comboBox in (self.comboBoxOnu):
                for key in Model.data["INTERNET"]["ONU"].keys():
                    for element in INTERNET["ONU"][key]:
                        if comboBox.get() == element:
                            situacaoNET += " " + INTERNET["ONU"][key][element]

            # Checando as entradas de todos os COMBOBOX do Frame PPPoE e gerando o texto da internet
            for comboBox in (self.comboBoxRt):
                for key in Model.data["INTERNET"]["RT"].keys():
                    for element in INTERNET["RT"][key]:
                        if comboBox.get() == element:
                            situacaoNET += " " + INTERNET["RT"][key][element]

            situacaoNET += Model.data["LENTIDÃO"]["C/ LENTIDÃO" if self.swLentidao.get()
                                                else "S/ LENTIDÃO"]
        else:
            for frame in (self.OnuFrame, self.PppoeFrame):
                frame.grid_remove()
        return situacaoNET

    def getTV(self):
        situacaoTV = ""
        TV = Model.data["TV"]

        if "TV" in self.comboBoxProblema.get():
            self.createSectionTv() 

            tecnologia = self.comboBoxTecnologia.get()
            if tecnologia in TV:
                self.comboBoxTV2.configure(values=list(TV[tecnologia].keys()))
                if self.comboBoxTV2.get() not in TV[tecnologia].keys():
                    self.comboBoxTV2.set(list(TV[tecnologia].keys())[0])

            for comboBox in [self.comboBoxTV2]:
                for key in TV.keys():
                    for element in TV[key]:
                        if comboBox.get() == element:
                            situacaoTV += " " + TV[key][element]

        else:
            self.TvFrame.grid_remove()
        return situacaoTV
    
    def getUser(self):
        return self.comboBoxUser.get()
    

    def deselect_all_radio_buttons(self, variable):
        for widget in self.FinalFrame.winfo_children():
            if isinstance(widget, customtkinter.CTkRadioButton):
                widget.deselect()

    def reset(self):
        self.comboBoxProblema.set("")
        self.comboBoxUser.set("")
        self.mainText.delete("1.0", "end")

        # Deselect all radio buttons associated with the same variable
        self.deselect_all_radio_buttons(self.variable)

        Model.data["ANALISE"]["FINALIZACAO"] = ""

        self.swLentidao.deselect()
        self.OnuFrame.grid_remove()
        self.PppoeFrame.grid_remove()
        self.TvFrame.grid_remove()