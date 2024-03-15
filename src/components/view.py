from tkinter import StringVar, Label
import customtkinter

from models.frame import Frame
from models.comboBox import ComboBox
from models.switch import Switch
from models.button import Button, RadioButton

from components.controller import Controller
from models.models import Model, Payload

from utils.base import resource_path


class View:
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
        self.Header = Frame(master=self.window, title="INÍCIO DA ANALISE")
        self.Payload = Payload(self.window)
        self.Onu = Frame(master=self.window, title="ONU")
        self.Rt = Frame(master=self.window, title="RT")
        self.Tv = Frame(master=self.window, title="TV")
        self.Final = Frame(master=self.window, title="FINALIZAÇÃO")

        self.Header.pack(side="top", fill="both", expand=True)
        self.Payload.pack(side="top", fill="both", expand=True)
        self.create_section_tv()
        self.create_section_internet()
        self.createSectionFinal()

    def create_section_tv(self):
        self.Tv.pack(side="top", fill="both", expand=True)
        self.Tv.renderWidgets()

    def createWidgetsOnu(self):
        self.Onu.renderWidgets()

    def createWidgetsRt(self):
        self.Rt.renderWidgets(3)

    def create_section_internet(self):
        self.Onu.pack(side="top", fill="both", expand=True)
        self.Rt.pack(side="top", fill="both", expand=True)
        self.createWidgetsOnu()
        self.createWidgetsRt()

    def createSectionFinal(self):
        self.lbRodape = Label(master=self.window, text="Contact for support or further information: vynijales@gmail.com.")
        self.lbRodape.pack(side="bottom", fill="both", expand=True)
        self.Final.pack(side="bottom", fill="both", expand=True)  # Position at the bottom

    def createWidgets(self):
        self.cbProblema = ComboBox(master=self.Header, values=Model.data["PROBLEMAS"], view=self)
        self.cbUser = ComboBox(self.Header, values=Model.data["USUÁRIOS"], view=self)
        self.Header.renderWidgets()
        self.cbUser.pack(side="right")

        listOnu = list(Model.data["INTERNET"]["ONU"].keys())
        self.cbOnu = [ComboBox(master=self.Onu, values=list(Model.data["INTERNET"]["ONU"][combo]), view=self) for combo in listOnu]
        
        listRt = list(Model.data["INTERNET"]["RT"].keys())
        self.cbRt = [ComboBox(master=self.Rt, values=list(Model.data["INTERNET"]["RT"][combo].keys()), view=self) for combo in listRt]
        
        self.swLentidao = Switch(self.Rt, command=lambda: Controller.atualizar(self, self))

        listTec = list(Model.data["TV"].keys())
        self.cbTec = ComboBox(master=self.Tv, values=listTec, view=self)
        
        listTv2 = list(Model.data["TV"][listTec[0]].keys())
        self.cbTv2 = ComboBox(self.Tv, values=listTv2, view=self)

        self.radioButtonRetida = RadioButton(master=self.Final, text="SAC N2", view=self)
        self.radioButtonAssistencia = RadioButton(master=self.Final, text="ASSISTÊNCIA", view=self)
        self.radioButtonCancelada = RadioButton(master=self.Final, text="CANCELADA", view=self)
        
        self.buttonClear = Button(master=self.Final, text="LIMPAR", command=self.reset, fg_color="red", hover_color="#d94545")
        self.buttonCopy = Button(master=self.Final, text="COPIAR", command=lambda: Controller.ctrl_c(self))

        self.Final.renderWidgets(3)

    def get_internet(self):
        text = ""
        INTERNET = Model.data["INTERNET"]

        for comboBox in (self.cbOnu):
            for key in Model.data["INTERNET"]["ONU"].keys():
                for element in INTERNET["ONU"][key]:
                    if comboBox.get() == element:
                        text += " " + INTERNET["ONU"][key][element]

        # Checando as entradas de todos os COMBOBOX do Frame PPPoE e gerando o texto da internet
        for comboBox in (self.cbRt):
            for key in Model.data["INTERNET"]["RT"].keys():
                for element in INTERNET["RT"][key]:
                    if comboBox.get() == element:
                        text += " " + INTERNET["RT"][key][element]

        text += Model.data["LENTIDÃO"]["C/ LENTIDÃO" if self.swLentidao.get() else "S/ LENTIDÃO"]

        return text

    def get_tv(self):
        text = ""
        TV = Model.data["TV"]
        tecnologia = self.cbTec.get()
        if tecnologia in TV:
            self.cbTv2.configure(values=list(TV[tecnologia].keys()))
            if self.cbTv2.get() not in TV[tecnologia].keys():
                self.cbTv2.set(list(TV[tecnologia].keys())[0])

        for comboBox in [self.cbTv2]:
            for key in TV.keys():
                for element in TV[key]:
                    if comboBox.get() == element:
                        text += " " + TV[key][element]

        return text

    def deselect_all_radio_buttons(self, variable):
        for widget in self.Final.winfo_children():
            if isinstance(widget, customtkinter.CTkRadioButton):
                widget.deselect()

    def reset(self):
        self.cbProblema.set("")
        self.cbUser.set("")
        self.Payload.delete("1.0", "end")

        # Deselect all radio buttons associated with the same variable
        self.deselect_all_radio_buttons(self.variable)

        Model.data["ANALISE"]["FINALIZACAO"] = ""

        self.swLentidao.deselect()
        self.Onu.pack_forget()
        self.Rt.pack_forget()
        self.Tv.pack_forget()
        self.adjust_window_height()

    def adjust_window_size(self):
        self.window.geometry('849x1')
        self.window.resizable(False, False)

    def adjust_window_height(self):
        self.window.update_idletasks()
        height = self.window.winfo_reqheight()
        self.window.geometry('849x' + str(height))
