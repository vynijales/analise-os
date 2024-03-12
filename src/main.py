from tkinter import *
import customtkinter
import pyperclip as pc

from utils.constants import TOTALCOLUNAS
from utils.base import Model, resource_path, get_date_time
from components.view import *

DADOS = Model.data


class Controller:
    def __init__(self):
        self.setor = ""
        self.internet = ""
        self.tv = ""
        self.finalizacao = ""
        self.user = ""

    def getInternet(self, source, target):
        self.internet = ""
        INTERNET = DADOS["INTERNET"]

        # Deixarei esse método apenas para retornar o texto referente à internet, os objetos de tela serão criados em outra função
        if "INTERNET" in source.get():
            dbKeys = list(INTERNET.keys())
            for comboBox in target:
                for key in dbKeys:
                    for element in INTERNET[key]:
                        if comboBox.get() == element:
                            self.internet += " " + INTERNET[key][element]


controller = Controller()
view = View()


def atualizar(arg):
    textObservacao.delete("1.0", "end")
    setor = DADOS["SETOR"]
    internet = getInternet()
    tv = getTV()
    finalizacao = DADOS["OBSERVACAO"]["FINALIZACAO"]
    user = cbUser.get()
    data = get_date_time()
    textObservacao.insert(
        END, f'{setor + internet + tv + finalizacao}\n\n{user}{data}')


def clear():
    cbProblema.set("")
    atualizar(True)


def ctrlc():
    pc.copy(textObservacao.get("1.0", "end-1c"))


def assistencia():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "A Ordem de Serviço foi liberada e encaminhada para a equipe de assistência."
    atualizar(True)


def retida():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "A Ordem de Serviço foi temporariamente retida pelo SAC N2."
    atualizar(True)


def cancelada():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "Realizado contato com o titular, o mesmo confirmou normalidade e autorizou o cancelamento da Ordem de serviço. Por favor, marque-a como não executada."
    atualizar(True)


def createSectionInternet():
    for i, frame in enumerate([view.OnuFrame, view.PppoeFrame]):
        frame.grid(column=0, row=(i + 4), padx=5, pady=5,
                   columnspan=TOTALCOLUNAS, sticky="nswe")
    for i, widget in enumerate(comboBoxOnu + comboBoxPppoe + [spacer2, swLentidao]):
        widget.grid(column=(i + 1), row=0, padx=5, pady=5, sticky="nswe")


def getInternet():
    situacaoNET = ""
    # Recebendo valores do banco de informação
    INTERNET = Model.data["INTERNET"]

    if "INTERNET" in cbProblema.get():
        createSectionInternet()  # Organizando os FRAMES de ONU e PPPoE

        # Checando as entradas de todos os COMBOBOX do Frame ONU e gerando o texto da internet
        for comboBox in (comboBoxOnu):
            for key in Model.data["INTERNET"]["ONU"].keys():
                for element in INTERNET["ONU"][key]:
                    if comboBox.get() == element:
                        situacaoNET += " " + INTERNET["ONU"][key][element]

        # Checando as entradas de todos os COMBOBOX do Frame PPPoE e gerando o texto da internet
        for comboBox in (comboBoxPppoe):
            for key in Model.data["INTERNET"]["RT"].keys():
                for element in INTERNET["RT"][key]:
                    if comboBox.get() == element:
                        situacaoNET += " " + INTERNET["RT"][key][element]

        # Gerando texto referente à lentdão
        situacaoNET += Model.data["LENTIDÃO"]["C/ LENTIDÃO" if swLentidao.get()
                                              else "S/ LENTIDÃO"]

    else:
        # Removendo os FRAMES de ONU e PPPoE, dessa forma a função está retornando ""
        for frame in (view.OnuFrame, view.PppoeFrame):
            frame.grid_remove()
    return situacaoNET


def getTV():
    situacaoTV = ""
    TV = DADOS["TV"]  # Recebendo valores do banco de informação
    if "TV" in cbProblema.get():
        # Organiizando o FRAME de TV
        view.TvFrame.grid(column=0, row=6, padx=5, pady=5,
                          columnspan=TOTALCOLUNAS, sticky="nswe")
        # Organizando os COMBOBOX do Frame TV
        for i, comboBox in enumerate([cbTecnologia, cbTV2]):
            comboBox.grid(column=i, row=4, padx=5, pady=5)
        tecnologia_selecionada = cbTecnologia.get()  # Recebe o valor do COMBOBOX TV 1
        if tecnologia_selecionada in TV:
            cbTV2["values"] = list(TV[tecnologia_selecionada].keys())
            cbTV2.configure(values=list(TV[tecnologia_selecionada].keys()))
            opcao_selecionada = cbTV2.get()  # Recebendo o valor do COMBOBOX TV 2
            if opcao_selecionada in TV[tecnologia_selecionada]:
                # Gerando o texto referente à TV
                situacaoTV = TV[tecnologia_selecionada][opcao_selecionada]
            else:
                # Caso altere o COMBOBOX TV 1, irá setar o COMBOBOX TV 2 para o elemento de índice 0
                cbTV2.set(list(TV[tecnologia_selecionada].keys())[0])
                # Gerando o texto referente à TV
                situacaoTV = TV[tecnologia_selecionada][cbTV2.get()]

    else:
        # Removendo o FRAME de TV, dessa forma a função está retornando
        view.TvFrame.grid_remove()
    return situacaoTV


# WINDOW.iconbitmap(False, PhotoImage(file=path)) # Converter para executável
# Enquanto programa local
view.window.iconbitmap(resource_path('assets/img/icon.ico'))
view.window.title("ANÁLISE DE OS - SISTEMA OESTE DE COMUNICAÇÃO LTDA")
view.window.resizable(False, False)

# CRIANDO OS FRAMES

# FRAME CABECALHO
# view.CabecalhoFrame.grid(column=0, row=0, padx=10, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe")

# cbProblema = customtkinter.CTkComboBox(view.CabecalhoFrame, width=157, values = DADOS["PROBLEMAS"], state='readonly', command=atualizar)
# cbProblema.grid(column=0,row=0, padx=5, pady=5,)

cbProblema = ComboBoxProblema(view.CabecalhoFrame, atualizar)

spacer1 = GapCabecalho(view.CabecalhoFrame)

cbUser = ComboBoxUser(view.CabecalhoFrame, atualizar)

# FRAME OBSERVACAO
# textObservacao = customtkinter.CTkTextbox(
#     view.window, height=300, wrap=WORD, font=customtkinter.CTkFont(size=14,))
# textObservacao.grid(column=0, row=2, columnspan=TOTALCOLUNAS, sticky="nswe")

textObservacao = MainText(view.window)

# FRAME INTERNET

# listaOnu = ["MODELO ONU", "STATUS", "PORTA", "ALARMES", "HISTÓRICO"]
listaOnu = list(Model.data["INTERNET"]["ONU"].keys())
comboBoxOnu = [customtkinter.CTkComboBox(view.OnuFrame, values=list(DADOS["INTERNET"]["ONU"][cb].keys(
    # Criando COMBOBOXes do FRAME ONU
)), state='readonly', command=atualizar) for cb in listaOnu]

listaPppoe = list(Model.data["INTERNET"]["RT"].keys())
comboBoxPppoe = [customtkinter.CTkComboBox(view.PppoeFrame, values=list(DADOS["INTERNET"]["RT"][cb].keys(
    # Criando COMBOBOXes do FRAME PPPoE
)), state='readonly', command=atualizar) for cb in listaPppoe]

for i, cb in enumerate(comboBoxOnu):
    cb.set(list(DADOS["INTERNET"]["ONU"][listaOnu[i]].keys())[0])

for i, cb in enumerate(comboBoxPppoe):
    cb.set(list(DADOS["INTERNET"]["RT"][listaPppoe[i]].keys())[0])

spacer2 = GapInternet(view.PppoeFrame)
swLentidao = customtkinter.CTkSwitch(master=view.PppoeFrame, command=lambda: atualizar(
    True), text="LENTIDÃO", state='disable')

# FRAME TV
# cbTecnologia = customtkinter.CTkComboBox(view.TvFrame, values = list(DADOS["TV"].keys()), state='readonly', command=atualizar)
# cbTecnologia.set(list(DADOS["TV"].keys())[0])
cbTecnologia = ComboBoxTecnologia(view.TvFrame, atualizar)

cbTV2 = ComboBoxTV2(view.TvFrame, atualizar)
# FRAME FINAL
var_end = IntVar()
# rbRetida = customtkinter.CTkRadioButton(view.FinalFrame, text = "SAC N2", variable = var_end, value = 1, command=retida)
# rbAssistencia = customtkinter.CTkRadioButton(view.FinalFrame, text = "ASSISTÊNCIA", variable = var_end, value = 2, command=assistencia)
# rbCancelada = customtkinter.CTkRadioButton(view.FinalFrame, text = "CANCELADA", variable = var_end, value = 3, command=cancelada)

rbRetida = RadioButtonRetida(view.FinalFrame, var_end, retida)
rbAssistencia = RadioButtonAssistencia(view.FinalFrame, var_end, assistencia)
rbCancelada = RadioButtonCancelada(view.FinalFrame, var_end, cancelada)

# spacer3 = customtkinter.CTkLabel(view.FinalFrame, text="", width=120)
spacer3 = GapFinal(view.FinalFrame)
btClear = ButtonClear(view.FinalFrame, command=clear)
btCopy = ButtonCopy(view.FinalFrame, command=ctrlc)
# Organizando os elementos do FRAME FINAL
for i, widget in enumerate([rbRetida, rbAssistencia, rbCancelada, spacer3, btClear, btCopy]):
    widget.grid(column=i, row=0, padx=10, pady=5)

# FRAME AUTOR

lbRodape = customtkinter.CTkLabel(
    master=view.window, text="Contact for support or further information: vynijales@gmail.com.")
lbRodape.grid(row=11, column=0, columnspan=TOTALCOLUNAS, sticky="nsew")

# MAIN LOOP
view.window.mainloop()
