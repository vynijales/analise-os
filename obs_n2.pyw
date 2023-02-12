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
                "PORTA NORMAL": "A porta foi verificada e não foi encontrado nenhum problema geral.",
                "PORTA EM VERIFICAÇÃO": "Foram identificadas outras ONUs com alarme de queda no mesmo horário na porta.",
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
                "S/ DESCONEXÕES": "sem múltiplas desconexões diárias. ",
                "C/ DESCONEXÕES": "com múltiplas desconexões. "
            },
            "LENTIDÃO": {
                "S/ LENTIDÃO": "",
                "C/ LENTIDÃO": " Foram verificadas as configurações de VLAN, GATEWAY e IP. A velocidade foi liberada no CMTS e a ONU está registrada com Port Rate de 1000 Mbps."




            }
        },
  "TV": {
            "COAXIAL": {
                "ÁREA NORMAL": "Cliente possui TV COAXIAL, sem reclamações o suficiente na região para acionar a Equipe de Rede. ",
                "ÁREA EM VERIFICAÇÃO": "Cliente possui TV COAXIAL, outros clientes na região apresentam o mesmo problema. A equipe de rede foi acionada para investigar. "
            },
            "TV-FIBRA": {
                "RX NORMAL": "Cliente possui TV-FIBRA, está com sinal 1490 normal. ",
                "RX ALTERADO": "Cliente possui TV-FIBRA, está com sinal 1490 alterado (-30.0 dBm). ",
                "SINAL OFF": "Cliente possui TV-FIBRA, está sem sinal de Internet e TV. "
            },
            "BOX-PREMIUM": {
                "LOGIN OK": "Cliente possui TV BOX-PREMIUM, testado login na Plataforma WEB e aparentemente está funcionando corretamente. ",
                "LOGIN OFF": "Cliente possui TV BOX-PREMIUM, testado login na Plataforma WEB e não foi possível acessar. A situação foi encaminhada para o de Controle de Qualidade para resolução. "
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
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "A Ordem de Serviço foi liberada e encaminhada para a equipe de assistência."
    atualizar(True)

def retida():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = " A Ordem de Serviço foi temporariamente retida pelo Nível 2."
    atualizar(True)

def cancelada():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = " Realizado contato com o titular e o mesmo confirmou normalidade. Foi autorizado o cancelamentto da Ordem de serviço. Por favor, marque-a como não executada."
    atualizar(True)
    
def getInternet():
    situacaoNET = ""
    INTERNET = DADOS["INTERNET"] # Recebendo valores do banco de informação
    if "INTERNET" in cbProblema.get():
        for i, frame in enumerate([frames[1], frames[2]]): # Organizando os FRAMES de INTERNET
            frame.grid(column=0, row=(i + 4), padx=5, pady=5, columnspan=4, sticky="nswe")
        
        for i, widget in enumerate([cbOnu, cbPorta, cbAlarmes, cbHistorico, cbPppoe, cbDesconexoes, spacer2, swLentidao]): # Organizando os COMBOBOX dos FRAMES ONU e PPPoE 
            widget.grid(column=(i + 1), row=0, padx=5, pady=5, sticky="nswe")

        dbKeys = list(INTERNET.keys())
        for comboBox in (cbOnu, cbPorta, cbAlarmes, cbHistorico, cbPppoe, cbDesconexoes): # Checando as entradas de todos os COMBOBOX do Frame ONU e gerando o texto da internet
            for key in dbKeys:
                for element in INTERNET[key]:
                    if comboBox.get() == element:
                        situacaoNET += " " + INTERNET[key][element]

        situacaoNET += INTERNET["LENTIDÃO"]["C/ LENTIDÃO" if swLentidao.get() else "S/ LENTIDÃO"] # Gerando texto referente à lentdão

    else:
        for frame in (frames[1], frames[2]): # Removendo os FRAMES de ONU e PPPoE, dessa forma a função está retornando ""
            frame.grid_remove()
    return situacaoNET

def getTV():
    situacaoTV = ""
    TV = DADOS["TV"] # Recebendo valores do banco de informação
    if "TV" in cbProblema.get():
        frames[3].grid(column=0, row=6, padx=5, pady=5, columnspan=4, sticky="nswe") # Organiizando o FRAME de TV
        for i, comboBox in enumerate([cbTV, cbTV2]): # Organizando os COMBOBOX do Frame TV
            comboBox.grid(column=i, row=4, padx=5, pady=5)        
        tecnologia_selecionada = cbTV.get() # Recebe o valor do COMBOBOX TV 1
        if tecnologia_selecionada in TV:
            cbTV2["values"] = list(TV[tecnologia_selecionada].keys())
            cbTV2.configure(values=list(TV[tecnologia_selecionada].keys()))
            opcao_selecionada = cbTV2.get() # Recebendo o valor do COMBOBOX TV 2
            if opcao_selecionada in TV[tecnologia_selecionada]:
                situacaoTV = TV[tecnologia_selecionada][opcao_selecionada] # Gerando o texto referente à TV
            else:
                cbTV2.set(list(TV[tecnologia_selecionada].keys())[0]) # Caso altere o COMBOBOX TV 1, irá setar o COMBOBOX TV 2 para o elemento de índice 0
                situacaoTV = TV[tecnologia_selecionada][cbTV2.get()] # Gerando o texto referente à TV

    else: frames[3].grid_remove() # Removendo o FRAME de TV, dessa forma a função está retornando 
    return situacaoTV


# JANELA PRINCIPAL
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")
WINDOW = customtkinter.CTk()
WINDOW.iconbitmap(r'C:\Users\Matheus\Documents\Programação\att_script\img\icon.ico')
WINDOW.title("ANÁLISE DE OS N2 - SISTEMA OESTE DE COMUNICAÇÃO LTDA")
WINDOW.resizable(False, False)

# CRIANDO OS FRAMES
frame_titles = ['INICIO DA ANÁLISE', 'ONU', 'PPPOE', 'TV', 'FIM DA ANÁLISE']
frame_options = {'padx': 5, 'pady': 5}
frames = [LabelFrame(WINDOW, text=title, **frame_options) for title in frame_titles]

# FRAME CABECALHO 
frames[0].grid(column=0, row=0, padx=10, pady=5, columnspan=4, sticky="nswe")
spacer1 = customtkinter.CTkLabel(frames[0], text="",)
spacer1.grid(column=4,row=0, padx=140)
cbUser = customtkinter.CTkComboBox(frames[0], width=157, values = DADOS["USUÁRIOS"], state='readonly', command=atualizar)
cbUser.set(DADOS["USUÁRIOS"][7])
cbUser.grid(column=5,row=0, padx = 0, pady=0, sticky=E)

# FRAME OBSERVACAO
textObservacao = customtkinter.CTkTextbox(WINDOW, width=620, height=300, wrap=WORD, font=customtkinter.CTkFont(size=14,))
textObservacao.grid(column=0, row=2, columnspan=4, sticky="nswe")

# FRAME INTERNET
cbProblema = customtkinter.CTkComboBox(frames[0], values = DADOS["PROBLEMAS"], state='readonly', command=atualizar)
cbProblema.grid(column=1,row=0, padx=5, pady=5,)
cbOnu = customtkinter.CTkComboBox(frames[1], values = list(DADOS["INTERNET"]["STATUS"].keys()), state='readonly', command=atualizar)
cbOnu.set(list(DADOS["INTERNET"]["STATUS"].keys())[0])
cbPorta = customtkinter.CTkComboBox(frames[1], values = list(DADOS["INTERNET"]["PORTA"].keys()), state='readonly', command=atualizar)
cbPorta.set(list(DADOS["INTERNET"]["PORTA"].keys())[0])
cbAlarmes = customtkinter.CTkComboBox(frames[1], values = list(DADOS["INTERNET"]["ALARMES"].keys()), state='readonly', command=atualizar)
cbAlarmes.set(list(DADOS["INTERNET"]["ALARMES"].keys())[0])
cbHistorico = customtkinter.CTkComboBox(frames[1], values = list(DADOS["INTERNET"]["HISTÓRICO"].keys()), state='readonly', command=atualizar)
cbHistorico.set(list(DADOS["INTERNET"]["HISTÓRICO"].keys())[0])
cbPppoe = customtkinter.CTkComboBox(frames[2], values = list(DADOS["INTERNET"]["PPPOE"].keys()), state='readonly', command=atualizar)
cbPppoe.set(list(DADOS["INTERNET"]["PPPOE"].keys())[0])
cbDesconexoes = customtkinter.CTkComboBox(frames[2], values = list(DADOS["INTERNET"]["DESCONEXÕES"].keys()), state='readonly', command=atualizar)
cbDesconexoes.set(list(DADOS["INTERNET"]["DESCONEXÕES"].keys())[0])
spacer2 = customtkinter.CTkLabel(frames[2], text="", width=170)
swLentidao = customtkinter.CTkSwitch(master=frames[2], command=lambda: atualizar(True), text="LENTIDÃO", state='disable')

# FRAME TV
cbTV = customtkinter.CTkComboBox(frames[3], values = list(DADOS["TV"].keys()), state='readonly', command=atualizar)
cbTV.set(list(DADOS["TV"].keys())[0])
cbTV2 = customtkinter.CTkComboBox(frames[3], values = list(DADOS["TV"]["COAXIAL"].keys()), state='readonly', command=atualizar)
cbTV2.set(list(DADOS["TV"]["COAXIAL"].keys())[0])
# FRAME FINAL
frames[4].grid(column=0, row=8, padx=10, pady=5, columnspan=4, sticky="nswe")
var_end = IntVar()
rbRetida = customtkinter.CTkRadioButton(frames[4], text = "OS retida", variable = var_end, value = 1, command=retida)
rbLiberada = customtkinter.CTkRadioButton(frames[4], text = "OS liberada", variable = var_end, value = 2, command=liberada)
rbCancelada = customtkinter.CTkRadioButton(frames[4], text = "OS cancelada", variable = var_end, value = 3, command=cancelada)
btClear = customtkinter.CTkButton(master=frames[4], text="Limpar", command=clear, fg_color="red", hover_color="#d94545", width=95)
btCopy = customtkinter.CTkButton(master=frames[4], text="Copiar", command=ctrlc, width=95)
for i, widget in enumerate([rbRetida, rbLiberada, rbCancelada, btClear, btCopy]): # Organizando os elementos do FRAME FINAL
    widget.grid(column=i, row=0, padx=10, pady=5)

# FRAME AUTOR
frameRodape = customtkinter.CTkFrame(master=WINDOW, height=20, fg_color="#ebebeb")
frameRodape.grid(column=0, row=10, padx=10, pady=5, columnspan=4, sticky="nswe")
lbRodape = customtkinter.CTkLabel(master = frameRodape, text="Contact for support or further information: vynijales@gmail.com.")
frameRodape.grid_rowconfigure(0, weight=1)
frameRodape.grid_columnconfigure(0, weight=1)
lbRodape.grid(row=0, column=0, sticky="nsew")

# MAIN LOOP
WINDOW.mainloop()