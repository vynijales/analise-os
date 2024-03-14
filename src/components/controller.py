import pyperclip as pc

from components.models import Model
from utils.base import get_date_time

class Controller:
    def __init__(self):
        self.setor = ""
        self.internet = ""
        self.tv = ""
        self.finalizacao = ""
        self.user = ""

    def setInternet(self, view):
        self.internet = ""
        INTERNET = Model.data["INTERNET"]

        if "INTERNET" in view.comboBoxProblema.get():
            for comboBox in (view.comboBoxOnu):
                for key in Model.data["INTERNET"]["ONU"].keys():
                    for element in INTERNET["ONU"][key]:
                        if comboBox.get() == element:
                            self.internet += " " + INTERNET["ONU"][key][element]

            for comboBox in (view.comboBoxPppoe):
                for key in Model.data["INTERNET"]["RT"].keys():
                    for element in INTERNET["RT"][key]:
                        if comboBox.get() == element:
                            self.internet += " " + INTERNET["RT"][key][element]

            self.internet += Model.data["LENTIDÃO"]["C/ LENTIDÃO" if view.swLentidao.get()
                                              else "S/ LENTIDÃO"]
    
            view.createSectionInternet()
    
    def setTv(self, view):
        self.tv = ""
        TV = Model.data["TV"]

        if "TV" in view.comboBoxProblema.get():
            for comboBox in (view.comboBoxTecnologia, view.comboBoxTV2):
                for key in Model.data["TV"].keys():
                    for element in TV[key]:
                        if comboBox.get() == element:
                            self.tv += " " + TV[key][element]
    
    @staticmethod
    def setFrames(view):
        if "INTERNET" in view.comboBoxProblema.get():
            view.createSectionInternet()
        else:
            for frame in (view.OnuFrame, view.PppoeFrame):
                frame.grid_remove()
        if "TV" in view.comboBoxProblema.get():
            view.createSectionTv()
        else:
            view.TvFrame.grid_remove()
    
    def setUser(self, view):
        self.user = view.cbUser.get()

    @staticmethod
    def ctrlc(self, target):
        pc.copy(target.get("1.0", "end-1c"))

    @staticmethod
    def atualizar(view, value):
        target = view.mainText
        tv = view.getTV()
        target.delete("1.0", "end")
        setor = Model.data["SETOR"]
        internet = view.getInternet()

        if value == "retida":
            Model.data["ANALISE"]["FINALIZACAO"] ="A Ordem de Serviço foi temporariamente retida pelo SAC N2."
        elif value == "assistencia":
            Model.data["ANALISE"]["FINALIZACAO"] = "A Ordem de Serviço foi liberada e encaminhada para a equipe de assistência."
        elif value == "cancelada":
            Model.data["ANALISE"]["FINALIZACAO"] = "Realizado contato com o titular, o mesmo confirmou normalidade e autorizou o cancelamento da Ordem de serviço. Por favor, marque-a como não executada."
        else:
            pass

        user = view.getUser()
        data = get_date_time()

        target.insert("end", f'{setor + internet + tv + Model.data["ANALISE"]["FINALIZACAO"]}\n\n{user}{data}')

        Controller.setFrames(view=view)