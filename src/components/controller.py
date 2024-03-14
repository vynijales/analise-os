import pyperclip as pc

from components.models import Model
from utils.base import get_date_time


class Controller:

    @staticmethod
    def InternetText(view):
        if "INTERNET" in view.comboBoxProblema.get():
            view.createSectionInternet()
            view.RtFrame.widgets[-1].pack(side="right")
            return view.getInternet()
        view.OnuFrame.pack_forget()
        view.RtFrame.pack_forget()
        return ""

    @staticmethod
    def TvText(view):
        if "TV" in view.comboBoxProblema.get():
            view.createSectionTv()
            return view.getTv()
        view.TvFrame.pack_forget()
        return ""

    @staticmethod
    def finalizacaoText(value):
        if value == "retida":
            Model.data["ANALISE"]["FINALIZACAO"] = "A Ordem de Serviço foi temporariamente retida pelo SAC N2."
        elif value == "assistencia":
            Model.data["ANALISE"]["FINALIZACAO"] = "A Ordem de Serviço foi liberada e encaminhada para a equipe de assistência."
        elif value == "cancelada":
            Model.data["ANALISE"]["FINALIZACAO"] = "Realizado contato com o titular, o mesmo confirmou normalidade e autorizou o cancelamento da Ordem de serviço. Por favor, marque-a como não executada."
        else:
            pass
        return Model.data["ANALISE"]["FINALIZACAO"]

    @staticmethod
    def ctrlc(view):
        pc.copy(view.Payload.get("1.0", "end-1c"))

    @staticmethod
    def atualizar(view, value):
        view.Payload.delete("1.0", "end")

        internet = Controller.InternetText(view)
        tv = Controller.TvText(view)
        setor = Model.data["SETOR"]
        finalizacao = Controller.finalizacaoText(value)

        user = view.comboBoxUser.get()
        data = get_date_time()

        view.Payload.insert(
            "end", f'{setor + internet + tv + finalizacao}\n\n{user}{data}')

        view.adjust_window_height()