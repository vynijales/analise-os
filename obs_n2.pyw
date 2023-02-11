from tkinter import *
from tkinter import ttk
import customtkinter
import pyperclip as pc
import datetime

DADOS = {
  "SETOR": "N2: ",
  "USUÁRIOS": [
    "ANABARBOSA",
    "ANACLARA",
    "BRUNOBANDEIRA",
    "EDUARDOBARRETO",
    "ERICKENRIQUE",
    "IGOR",
    "JOYCEJORDANIA",
    "MATHEUSVYNICIUS",
    "MIKAEL",
    "NAELSON",
    "WALKDERLYPEREIRA",
    "PEDROWENISTON"
  ],
  "PROBLEMAS" : ["", "TV", "INTERNET", "TV e INTERNET"],
  "INTERNET" : {
            "STATUS": {
                "ONLINE": "ONU ONLINE.",
                "OFFLINE (LOS)": "ONU OFFLINE, com alarme de LOS.",
                "OFFLINE (ENERGIA)": "ONU OFFLINE, com alarme de ENERGIA."
            },
            "PORTA": {
                "PORTA NORMAL": "Checado porta, nenhum problema geral.",
                "PORTA EM VERIFICAÇÃO": "Foi identificado outras ONUs com alarme de queda no mesmo horário.",
            },
            "ALARMES": {
                "S/ ALARMES": "Sem alarmes de queda recorrentes.",
                "C/ ALARMES": "Com alarmes de LOS/Energia recorrentes."
            },
            "HISTÓRICO": {
                "HISTÓRICO NORMAL": "Sinal 1490 normal no histórico.",
                "HISTÓRICO ALTERADO": "Sinal 1490 alterado em -30.0 dBm no histórico."
            },
            "PPPOE": {
                "CONECTADO": "PPPoE conectado,",
                "DESCONECTADO": "PPPoE desconectado,"
            },
            "DESCONEXÕES": {
                "S/ DESCONEXÕES": "sem múltiplas desconexões diárias.",
                "C/ DESCONEXÕES": "com múltiplas desconexões."
            },
            "LENTIDÃO": {
                "S/ LENTIDÃO": "",
                "C/ LENTIDÃO": " Checado VLAN, GATEWAY e IP. Velocidade liberada no CMTS e ONU cadastrada com Port Rate /1000."
            }
        },
  "TV": {
            "COAXIAL": {
                "ÁREA NORMAL": "Cliente possui tecnologia COAXIAL, sem reclamações o suficiente para acionar a Equipe de Rede na Região. ",
                "ÁREA EM VERIFICAÇÃO": "Cliente possui tecnologia COAXIAL, identificado clientes com o mesmo problema na Região. Acionado a Equipe de Rede para verificar. "
            },
            "TV-FIBRA": {
                "RX NORMAL": "Cliente possui tecnologia TV-FIBRA, Sinal 1490 normal. ",
                "RX ALTERADO": "Cliente possui tecnologia TV-FIBRA, Sinal 1490 alterado (-30.0 dBm). ",
                "SINAL OFF": "Cliente possui tecnologia TV-FIBRA, está sem sinal de Internet e TV. "
            },
            "BOX-PREMIUM": {
                "LOGIN OK": "Cliente possui tecnologia TV BOX PREMIUM, testado login na Plataforma WEB, aparentemente normal. ",
                "LOGIN OFF": "Cliente possui tecnologia TV BOX PREMIUM, testado login na Plataforma WEB, sem acesso. Situação encaminhada para o CQ. "
            }
        },
    "OBSERVACAO": {
        "PRINCIPAL": "",
        "SITUACAO": "",
        "FINALIZACAO": ""
    }

}

def atualizar(variable):
    textObservacao.delete("1.0", "end")
    textObservacao.insert(END, f'{DADOS["SETOR"] + getInternet() + getTV() + DADOS["OBSERVACAO"]["FINALIZACAO"]}\n\n{cbUser.get()}{rodape()}')

def rodape():
    today = datetime.datetime.now()
    td = today.strftime("%d/%m/%Y - %H:%M")
    return f" - {td}\n"+("-"*51)

def clear():
    cbProblema.set("")
    atualizar(True)

def ctrlc():
    pc.copy(textObservacao.get("1.0","end-1c"))

def liberada():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = " OS liberada e encaminhada para a equipe de assistência."
    atualizar(True)

def retida():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = " OS temporariamente retida pelo N2."
    atualizar(True)

def cancelada():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = " Realizado contato com o titular e confirmado normalidade, autorizado cancelamento da OS. Favor baixar sem execução."
    atualizar(True)
    
def getInternet():
    situacaoNET = ""
    INTERNET = DADOS["INTERNET"]
    if "INTERNET" in cbProblema.get():
        for i, widget in enumerate([frameOnu, framePPPoE]): # Organizando os FRAMES de INTERNET
            widget.grid(column=0, row=(i + 4), padx=10, pady=5, columnspan=5, sticky="nswe")
        
        for i, widget in enumerate([cbOnu, cbPorta, cbAlarmes, cbHistorico]): # Organizando os COMBOBOX do FRAME ONU
            widget.grid(column=(i + 1), row=0, padx=5, pady=5)
        
        for i, widget in enumerate([cbPppoe, cbDesconexoes, spacer2, swLentidao]): # Organizando os COMBOBOX do FRAME PPPOE
            widget.grid(column=(i + 1), row=0, padx=5, pady=5)

        dbKeys = list(INTERNET.keys())
        for comboBox in (cbOnu, cbPorta, cbAlarmes, cbHistorico, cbPppoe, cbDesconexoes):
            for key in dbKeys:
                for element in INTERNET[key]:
                    if comboBox.get() == element:
                        situacaoNET += " " + INTERNET[key][element]

        situacaoNET += INTERNET["LENTIDÃO"]["C/ LENTIDÃO" if swLentidao.get() else "S/ LENTIDÃO"]

    else:
        for widget in (frameOnu, framePPPoE):
            widget.grid_remove()
    return situacaoNET

def getTV():
    situacaoTV = ""
    TV = DADOS["TV"]
    if "TV" in cbProblema.get():
        frameTv.grid(column=0, row=6, padx=5, pady=5, columnspan=5, sticky="nswe")
        for i, widget in enumerate([cbTV, cbTV2]):
            widget.grid(column=(i + 1), row=4, padx=5, pady=5)        
        tecnologia_selecionada = cbTV.get()
        if tecnologia_selecionada in TV:
            cbTV2["values"] = list(TV[tecnologia_selecionada].keys())
            cbTV2.configure(values=list(TV[tecnologia_selecionada].keys()))

            opcao_selecionada = cbTV2.get()
            if opcao_selecionada in TV[tecnologia_selecionada]:
                situacaoTV = TV[tecnologia_selecionada][opcao_selecionada]
            else:
                cbTV2.set(list(TV[tecnologia_selecionada].keys())[0])
                situacaoTV = TV[tecnologia_selecionada][cbTV2.get()]

    else: frameTv.grid_remove()
    return situacaoTV


# FRAME PRINICIPAL ----------------------------------------------------------------------
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
WINDOW  = customtkinter.CTk()  # create CTk WINDOW like you do with the Tk WINDOW
WINDOW.iconbitmap(r'C:\Users\Matheus\Documents\Programação\att_script\img\icon.ico')
WINDOW.title("Análise do N2")
WINDOW.resizable(False, False)

# FRAMES
frameHead = LabelFrame(WINDOW, text='INICIO DA ANÁLISE', padx=5, pady=5)
frameOnu = LabelFrame(WINDOW, text='ONU', padx=5, pady=5)
framePPPoE = LabelFrame(WINDOW, text='PPPOE', padx=5, pady=5)
frameTv = LabelFrame(WINDOW, text='TV', padx=5, pady=5)
frameFinal = LabelFrame(WINDOW, text='FIM DA ANÁLISE', padx=5, pady=5)

# frame_titles = ['INICIO DA ANÁLISE', 'ONU', 'PPPOE', 'TV', 'FIM DA ANÁLISE']
# frame_options = {'padx': 5, 'pady': 5}

# frames = [LabelFrame(WINDOW, text=title, **frame_options) for title in frame_titles]

# FRAME INICIAL ----------------------------------------------------------------------

frameHead.grid(column=0, row=0, padx=10, pady=5, columnspan=5, sticky="nswe")
spacer1 = customtkinter.CTkLabel(frameHead, text="",)
spacer1.grid(column=4,row=0, padx=200)
spacer2 = customtkinter.CTkLabel(framePPPoE, text="", width=210)

cbUser = customtkinter.CTkComboBox(frameHead, width=157, values = DADOS["USUÁRIOS"], state='readonly', command=atualizar)
cbUser.set(DADOS["USUÁRIOS"][7])
cbUser.grid(column=5,row=0, padx = 0, pady=0, sticky=E)

# FRAME OBSERVACAO -----------------------------------------------------------------

textObservacao = customtkinter.CTkTextbox(WINDOW, width=750, height=300, wrap=WORD, font=customtkinter.CTkFont(size=14,))
textObservacao.grid(column=0, row=2, columnspan=5, sticky=W,)

# FRAME INTERNET -----------------------------------------------------------------
cbProblema = customtkinter.CTkComboBox(frameHead, values = DADOS["PROBLEMAS"], state='readonly', command=atualizar)
cbProblema.grid(column=1,row=0, padx=5, pady=5,)

cbOnu = customtkinter.CTkComboBox(frameOnu, values = list(DADOS["INTERNET"]["STATUS"].keys()), state='readonly', command=atualizar)
cbOnu.set(list(DADOS["INTERNET"]["STATUS"].keys())[0])

cbPorta = customtkinter.CTkComboBox(frameOnu, values = list(DADOS["INTERNET"]["PORTA"].keys()), state='readonly', command=atualizar)
cbPorta.set(list(DADOS["INTERNET"]["PORTA"].keys())[0])

cbAlarmes = customtkinter.CTkComboBox(frameOnu, values = list(DADOS["INTERNET"]["ALARMES"].keys()), state='readonly', command=atualizar)
cbAlarmes.set(list(DADOS["INTERNET"]["ALARMES"].keys())[0])

cbPppoe = customtkinter.CTkComboBox(framePPPoE, values = list(DADOS["INTERNET"]["PPPOE"].keys()), state='readonly', command=atualizar)
cbPppoe.set(list(DADOS["INTERNET"]["PPPOE"].keys())[0])

cbDesconexoes = customtkinter.CTkComboBox(framePPPoE, values = list(DADOS["INTERNET"]["DESCONEXÕES"].keys()), state='readonly', command=atualizar)
cbDesconexoes.set(list(DADOS["INTERNET"]["DESCONEXÕES"].keys())[0])

cbHistorico = customtkinter.CTkComboBox(frameOnu, values = list(DADOS["INTERNET"]["HISTÓRICO"].keys()), state='readonly', command=atualizar)
cbHistorico.set(list(DADOS["INTERNET"]["HISTÓRICO"].keys())[0])

swLentidao = customtkinter.CTkSwitch(master=framePPPoE, command=lambda: atualizar(True), text="LENTIDÃO", state='disable')

# FRAME TV --------------------------------------------------------------------------------------------------------
cbTV = customtkinter.CTkComboBox(frameTv, values = list(DADOS["TV"].keys()), state='readonly', command=atualizar)
cbTV.set(list(DADOS["TV"].keys())[0])

cbTV2 = customtkinter.CTkComboBox(frameTv, values = list(DADOS["TV"]["COAXIAL"].keys()), state='readonly', command=atualizar)
cbTV2.set(list(DADOS["TV"]["COAXIAL"].keys())[0])

# FRAME FINAL -----------------------------------------------------------------
frameFinal.grid(column=0, row=8, padx=10, pady=5, columnspan=5, sticky="nswe")
var_end = IntVar()
rbRetida = customtkinter.CTkRadioButton(frameFinal, text = "OS retida", variable = var_end, value = 1, command=retida)
rbLiberada = customtkinter.CTkRadioButton(frameFinal, text = "OS liberada", variable = var_end, value = 2, command=liberada)
rbCancelada = customtkinter.CTkRadioButton(frameFinal, text = "OS cancelada", variable = var_end, value = 3, command=cancelada)
btClear = customtkinter.CTkButton(master=frameFinal, text="Limpar", command=clear, fg_color="red", hover_color="#d94545", width=120)
btCopy = customtkinter.CTkButton(master=frameFinal, text="Copiar", command=ctrlc, width=120)

for i, widget in enumerate([rbRetida, rbLiberada, rbCancelada, btClear, btCopy]):
    widget.grid(column=i, row=0, padx=10, pady=5)

# FRAME AUTOR -----------------------------------------------------------------
frameRodape = customtkinter.CTkFrame(master=WINDOW, height=20, fg_color="#ebebeb")
frameRodape.grid(column=0, row=10, padx=10, pady=5, columnspan=5, sticky="nswe")

lbRodape = customtkinter.CTkLabel(master = frameRodape, text="Contact for support or further information: vynijales@gmail.com.")
frameRodape.grid_rowconfigure(0, weight=1)
frameRodape.grid_columnconfigure(0, weight=1)
lbRodape.grid(row=0, column=0, sticky="nsew")

WINDOW.mainloop()

