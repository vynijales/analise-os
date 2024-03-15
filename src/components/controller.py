import pyperclip as pc
from models.models import Model
from utils.base import get_date_time


class Controller:
    @staticmethod
    def internet_text(view):
        if "INTERNET" in view.cbProblema.get():
            view.create_section_internet()
            view.Rt.widgets[-1].pack(side="right")
            return view.get_internet()
        view.Onu.pack_forget()
        view.Rt.pack_forget()
        return ""

    @staticmethod
    def tv_text(view):
        if "TV" in view.cbProblema.get():
            view.create_section_tv()
            return view.get_tv()
        view.Tv.pack_forget()
        return ""

    @staticmethod
    def finalizacao_text(value):
        if value == "SAC N2":
            Model.data["ANALISE"]["FINALIZACAO"] = "A Ordem de Serviço foi temporariamente retida pelo SAC N2."
        elif value == "ASSISTÊNCIA":
            Model.data["ANALISE"]["FINALIZACAO"] = "A Ordem de Serviço foi liberada e encaminhada para a equipe de assistência."
        elif value == "CANCELADA":
            Model.data["ANALISE"]["FINALIZACAO"] = "Realizado contato com o titular, o mesmo confirmou normalidade e autorizou o cancelamento da Ordem de serviço. Por favor, marque-a como não executada."
        else:
            pass
        return Model.data["ANALISE"]["FINALIZACAO"]

    @staticmethod
    def ctrl_c(view):
        pc.copy(view.Payload.get("1.0", "end-1c"))

    @staticmethod
    def atualizar(view, value):
        view.Payload.delete("1.0", "end")

        internet = Controller.internet_text(view)
        tv = Controller.tv_text(view)
        setor = Model.data["SETOR"]
        finalizacao = Controller.finalizacao_text(value)

        user = view.cbUser.get()
        data = get_date_time()

        view.Payload.insert("end", f'{setor + internet + tv + finalizacao}\n\n{user}{data}')

        view.adjust_window_height()