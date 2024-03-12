import pyperclip as pc

from utils.base import Model, get_date_time

class Controller:
    def __init__(self):
        self.setor = ""
        self.internet = ""
        self.tv = ""
        self.finalizacao = ""
        self.user = ""

    def getInternet(self, source, target):
        self.internet = ""
        INTERNET = Model.data["INTERNET"]

        # Deixarei esse método apenas para retornar o texto referente à internet, os objetos de tela serão criados em outra função
        if "INTERNET" in source.get():
            dbKeys = list(INTERNET.keys())
            for comboBox in target:
                for key in dbKeys:
                    for element in INTERNET[key]:
                        if comboBox.get() == element:
                            self.internet += " " + INTERNET[key][element]
    
    @staticmethod
    def ctrlc(self, target):
        pc.copy(target.get("1.0", "end-1c"))

    @staticmethod
    def clear(self, target):
        target.delete("1.0", "end-1c")

    def atualizar(self, target):
        target.delete("1.0", "end")
        setor = Model.data["SETOR"]
        internet = getInternet()
        tv = getTV()
        finalizacao = Model.data["OBSERVACAO"]["FINALIZACAO"]
        user = cbUser.get()
        data = get_date_time()

        target.insert(
            "end", f'{setor + internet + tv + finalizacao}\n\n{user}{data}')
