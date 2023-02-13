from tkinter import *
from tkinter import ttk
import customtkinter
import pyperclip as pc
import datetime
import sys, os

def resource_path(relative_path): # Função usada ao exportar para executável
    """Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

TOTALCOLUNAS = 6

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
            "MODELO ONU": {
                "FIBERHOME": "ONU FIBERHOME",
                "ZTE": "ONU ZTE",
                "HUAWEI": "ONU HUAWEI"
            },
            "STATUS": {
                "ONLINE": "online.",
                "OFFLINE (LOS)": "offline, com alarme de LOS.",
                "OFFLINE (ENERGIA)": "offline, com alarme de ENERGIA."
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
            "MODELO RT": {
                "RT TP-LINK": "Rt TP-LINK com",
                "RT INTELBRAS": "Rt INTELBRAS com",
                "RT ZTE": "Rt ZTE com",
                "RT HUAWEI": "Rt HUAWEI com",
                "RT PARTICULAR": "Rt particular com",
                "RB MIKROTIK": "Rb MikroTik com",
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
                "LOGIN OFF": "Cliente possui TV BOX-PREMIUM, testado login na Plataforma WEB e não foi possível acessar. A situação foi encaminhada para o setor de Controle de Qualidade. "
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

def assistencia():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "A Ordem de Serviço foi liberada e encaminhada para a equipe de assistência."
    atualizar(True)

def retida():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "A Ordem de Serviço foi temporariamente retida pelo SAC N2."
    atualizar(True)

def cancelada():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "Realizado contato com o titular, o mesmo confirmou normalidade e autorizou o cancelamento da Ordem de serviço. Por favor, marque-a como não executada."
    atualizar(True)
    
def getInternet():
    situacaoNET = ""
    INTERNET = DADOS["INTERNET"] # Recebendo valores do banco de informação
    if "INTERNET" in cbProblema.get():
        for i, frame in enumerate([frames[1], frames[2]]): # Organizando os FRAMES de INTERNET
            frame.grid(column=0, row=(i + 4), padx=5, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe")
        
        for i, widget in enumerate([comboBoxOnu[0], comboBoxOnu[1], comboBoxOnu[2], comboBoxOnu[3], comboBoxOnu[4], comboBoxPppoe[0], comboBoxPppoe[1], comboBoxPppoe[2], spacer2, swLentidao]): # Organizando os COMBOBOX dos FRAMES ONU e PPPoE 
            widget.grid(column=(i + 1), row=0, padx=5, pady=5, sticky="nswe")

        dbKeys = list(INTERNET.keys())
        for comboBox in (comboBoxOnu[0], comboBoxOnu[1], comboBoxOnu[2], comboBoxOnu[3], comboBoxOnu[4], comboBoxPppoe[0], comboBoxPppoe[1], comboBoxPppoe[2]): # Checando as entradas de todos os COMBOBOX do Frame ONU e gerando o texto da internet
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
        frames[3].grid(column=0, row=6, padx=5, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe") # Organiizando o FRAME de TV
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
# WINDOW.iconphoto(False, PhotoImage(file=resource_path('img/icon.png'))) # Converter para executável
WINDOW.iconbitmap('img/icon.ico') # Enquanto programa local
WINDOW.title("ANÁLISE DE OS - SISTEMA OESTE DE COMUNICAÇÃO LTDA")
WINDOW.resizable(False, False)

# CRIANDO OS FRAMES
frame_titles = ['INICIO DA ANÁLISE', 'ONU', 'PPPOE', 'TV', 'FIM DA ANÁLISE']
frame_options = {'padx': 5, 'pady': 5}
frames = [LabelFrame(WINDOW, text=title, **frame_options) for title in frame_titles]

# FRAME CABECALHO 
frames[0].grid(column=0, row=0, padx=10, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe")

cbProblema = customtkinter.CTkComboBox(frames[0], values = DADOS["PROBLEMAS"], state='readonly', command=atualizar)
cbProblema.grid(column=1,row=0, padx=5, pady=5,)
spacer1 = customtkinter.CTkLabel(frames[0], text="",)
spacer1.grid(column=4,row=0, padx=215)
cbUser = customtkinter.CTkComboBox(frames[0], width=157, values = DADOS["USUÁRIOS"], state='readonly', command=atualizar)
cbUser.set(DADOS["USUÁRIOS"][7])
cbUser.grid(column=(TOTALCOLUNAS - 1), row=0, padx = 5, pady=5, sticky="e")

# FRAME OBSERVACAO
textObservacao = customtkinter.CTkTextbox(WINDOW, width=610, height=300, wrap=WORD, font=customtkinter.CTkFont(size=14,))
textObservacao.grid(column=0, row=2, columnspan=TOTALCOLUNAS, sticky="nswe")

# FRAME INTERNET
listaOnu = ["MODELO ONU", "STATUS", "PORTA", "ALARMES", "HISTÓRICO"]
comboBoxOnu = [customtkinter.CTkComboBox(frames[1], values = list(DADOS["INTERNET"][cb].keys()), state='readonly', command=atualizar) for cb in listaOnu] # Criando COMBOBOXes do FRAME ONU

listaPppoe = ["MODELO RT", "PPPOE", "DESCONEXÕES"]
comboBoxPppoe = [customtkinter.CTkComboBox(frames[2], values = list(DADOS["INTERNET"][cb].keys()), state='readonly', command=atualizar) for cb in listaPppoe] # Criando COMBOBOXes do FRAME PPPoE

for i, cb in enumerate(comboBoxOnu):
    cb.set(list(DADOS["INTERNET"][listaOnu[i]].keys())[0])

for i, cb in enumerate(comboBoxPppoe):
    cb.set(list(DADOS["INTERNET"][listaPppoe[i]].keys())[0])

spacer2 = customtkinter.CTkLabel(frames[2], text="", width=168)
swLentidao = customtkinter.CTkSwitch(master=frames[2], command=lambda: atualizar(True), text="LENTIDÃO", state='disable')

# FRAME TV
cbTV = customtkinter.CTkComboBox(frames[3], values = list(DADOS["TV"].keys()), state='readonly', command=atualizar)
cbTV.set(list(DADOS["TV"].keys())[0])
cbTV2 = customtkinter.CTkComboBox(frames[3], values = list(DADOS["TV"]["COAXIAL"].keys()), state='readonly', command=atualizar)
cbTV2.set(list(DADOS["TV"]["COAXIAL"].keys())[0])
# FRAME FINAL
frames[4].grid(column=0, row=8, padx=10, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe")
var_end = IntVar()
rbRetida = customtkinter.CTkRadioButton(frames[4], text = "SAC N2", variable = var_end, value = 1, command=retida)
rbAssistencia = customtkinter.CTkRadioButton(frames[4], text = "ASSISTÊNCIA", variable = var_end, value = 2, command=assistencia)
rbCancelada = customtkinter.CTkRadioButton(frames[4], text = "CANCELADA", variable = var_end, value = 3, command=cancelada)
spacer3 = customtkinter.CTkLabel(frames[4], text="", width=120)
btClear = customtkinter.CTkButton(master=frames[4], text="LIMPAR", command=clear, fg_color="red", hover_color="#d94545", width=95)
btCopy = customtkinter.CTkButton(master=frames[4], text="COPIAR", command=ctrlc, width=95)
for i, widget in enumerate([rbRetida, rbAssistencia, rbCancelada, spacer3, btClear, btCopy]): # Organizando os elementos do FRAME FINAL
    widget.grid(column=i, row=0, padx=10, pady=5)

# FRAME AUTOR
frameRodape = customtkinter.CTkFrame(master=WINDOW, height=20, fg_color="#ebebeb")
frameRodape.grid(column=0, row=10, padx=10, pady=5, columnspan=TOTALCOLUNAS, sticky="nswe")
lbRodape = customtkinter.CTkLabel(master = frameRodape, text="Contact for support or further information: vynijales@gmail.com.")
frameRodape.grid_rowconfigure(0, weight=1)
frameRodape.grid_columnconfigure(0, weight=1)
lbRodape.grid(row=0, column=0, sticky="nsew")

# MAIN LOOP
WINDOW.mainloop()