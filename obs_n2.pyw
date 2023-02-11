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
            "PPPoE": {
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
    text_obs.delete("1.0", "end")
    text_obs.insert(END, f'{DADOS["SETOR"] + getInternet() + getTV() + DADOS["OBSERVACAO"]["FINALIZACAO"]}\n\n{cb_user.get()}{rodape()}')

def rodape():
    today = datetime.datetime.now()
    td = today.strftime("%d/%m/%Y - %H:%M")
    return f" - {td}\n"+("-"*51)

def clear():
    cb_problem.set("")
    atualizar(True)

def ctrlc():
    pc.copy(text_obs.get("1.0","end-1c"))

def liberada():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "OS liberada e encaminhada para a equipe de assistência."
    atualizar(True)

def retida():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "OS temporariamente retida pelo N2."
    atualizar(True)

def cancelada():
    DADOS["OBSERVACAO"]["FINALIZACAO"] = "Realizado contato com o titular e confirmado normalidade, autorizado cancelamento da OS. Favor baixar sem execução."
    atualizar(True)
    
def getInternet():
    situacaoNET = ""
    INTERNET = DADOS["INTERNET"]
    if "INTERNET" in cb_problem.get():
        for i, widget in enumerate([frame_onu, frame_pppoe]): # Organizando os FRAMES de INTERNET
            widget.grid(column=0, row=(i + 4), padx=10, pady=5, columnspan=5, sticky="nswe")
        
        for i, widget in enumerate([cb_onu, cb_port, cb_alarm, cb_hist]): # Organizando os COMBOBOX do FRAME ONU
            widget.grid(column=(i + 1), row=0, padx=5, pady=5)
        
        for i, widget in enumerate([cb_pppoe, cb_desc, spacer2, sw_lentidao]): # Organizando os COMBOBOX do FRAME PPPOE
            widget.grid(column=(i + 1), row=0, padx=5, pady=5)

        dbKeys = list(INTERNET.keys())
        for comboBox in (cb_onu, cb_port, cb_alarm, cb_hist, cb_pppoe, cb_desc):
            for key in dbKeys:
                for element in INTERNET[key]:
                    if comboBox.get() == element:
                        situacaoNET += " " + INTERNET[key][element]

        situacaoNET += INTERNET["LENTIDÃO"]["C/ LENTIDÃO" if sw_lentidao.get() else "S/ LENTIDÃO"]

    else:
        for widget in (frame_onu, frame_pppoe):
            widget.grid_remove()
    return situacaoNET

def getTV():
    situacaoTV = ""
    TV = DADOS["TV"]
    if "TV" in cb_problem.get():
        frame_tv.grid(column=0, row=6, padx=5, pady=5, columnspan=5, sticky="nswe")
        for i, widget in enumerate([cb_tv, cb_tv2]):
            widget.grid(column=(i + 1), row=4, padx=5, pady=5)        
        tecnologia_selecionada = cb_tv.get()
        if tecnologia_selecionada in TV:
            cb_tv2["values"] = list(TV[tecnologia_selecionada].keys())
            cb_tv2.configure(values=list(TV[tecnologia_selecionada].keys()))

            opcao_selecionada = cb_tv2.get()
            if opcao_selecionada in TV[tecnologia_selecionada]:
                situacaoTV = TV[tecnologia_selecionada][opcao_selecionada]
            else:
                cb_tv2.set(list(TV[tecnologia_selecionada].keys())[0])
                situacaoTV = TV[tecnologia_selecionada][cb_tv2.get()]

    else: frame_tv.grid_remove()
    return situacaoTV


# FRAME PRINICIPAL ----------------------------------------------------------------------
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
window  = customtkinter.CTk()  # create CTk window like you do with the Tk window
window.iconbitmap(r'C:\Users\Matheus\Documents\Programação\att_script\img\icon.ico')
window.title("Análise do N2")
window.resizable(False, False)

# FRAMES
frame_head = LabelFrame(window, text='INICIO DA ANÁLISE', padx=5, pady=5)
frame_onu = LabelFrame(window, text='ONU', padx=5, pady=5)
frame_pppoe = LabelFrame(window, text='PPPOE', padx=5, pady=5)
frame_tv = LabelFrame(window, text='TV', padx=5, pady=5)
frame_end = LabelFrame(window, text='FIM DA ANÁLISE', padx=5, pady=5)

# FRAME INICIAL ----------------------------------------------------------------------

frame_head.grid(column=0, row=0, padx=10, pady=5, columnspan=5, sticky="nswe")
spacer1 = customtkinter.CTkLabel(frame_head, text="",)
spacer1.grid(column=4,row=0, padx=200)
spacer2 = customtkinter.CTkLabel(frame_pppoe, text="", width=210)

cb_user = customtkinter.CTkComboBox(frame_head, width=157, values = DADOS["USUÁRIOS"], state='readonly', command=atualizar)
cb_user.set(DADOS["USUÁRIOS"][7])
cb_user.grid(column=5,row=0, padx = 0, pady=0, sticky=E)

# FRAME OBSERVACAO -----------------------------------------------------------------

text_obs = customtkinter.CTkTextbox(window, width=750, height=300, wrap=WORD, font=customtkinter.CTkFont(size=14,))
text_obs.grid(column=0, row=2, columnspan=5, sticky=W,)

# FRAME INTERNET -----------------------------------------------------------------
list_problem = ["", "TV", "INTERNET", "TV e INTERNET",]
cb_problem = customtkinter.CTkComboBox(frame_head, values = list_problem, state='readonly', command=atualizar)
cb_problem.grid(column=1,row=0, padx=5, pady=5,)
list_onu = ["ONLINE", "OFFLINE (LOS)", "OFFLINE (ENERGIA)"]
cb_onu = customtkinter.CTkComboBox(frame_onu, values = list_onu, state='readonly', command=atualizar)
cb_onu.set(list_onu[0])
list_port = ["PORTA NORMAL", "PORTA EM VERIFICAÇÃO"]
cb_port = customtkinter.CTkComboBox(frame_onu, values = list_port, state='readonly', command=atualizar)
cb_port.set(list_port[0])
list_alarm = ["C/ ALARMES", "S/ ALARMES"]
cb_alarm = customtkinter.CTkComboBox(frame_onu, values = list_alarm, state='readonly', command=atualizar)
cb_alarm.set(list_alarm[1])
list_pppoe = ["CONECTADO", "DESCONECTADO"]
cb_pppoe = customtkinter.CTkComboBox(frame_pppoe, values = list_pppoe, state='readonly', command=atualizar)
cb_pppoe.set(list_pppoe[0])
list_desc = ["C/ DESCONEXÕES", "S/ DESCONEXÕES"]
cb_desc = customtkinter.CTkComboBox(frame_pppoe, values = list_desc, state='readonly', command=atualizar)
cb_desc.set(list_desc[1])
list_hist = ["HISTÓRICO NORMAL", "HISTÓRICO ALTERADO"]
cb_hist = customtkinter.CTkComboBox(frame_onu, values = list_hist, state='readonly', command=atualizar)
cb_hist.set(list_hist[0])
sw_lentidao = customtkinter.CTkSwitch(master=frame_pppoe, command=lambda: atualizar(True), text="LENTIDÃO", state='disable')

# FRAME TV --------------------------------------------------------------------------------------------------------
list_tv = ["COAXIAL", "TV-FIBRA", "BOX-PREMIUM"]
cb_tv = customtkinter.CTkComboBox(frame_tv, values = list_tv, state='readonly', command=atualizar)
cb_tv.set(list_tv[0])

list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
cb_tv2 = customtkinter.CTkComboBox(frame_tv, values = list_tv2, state='readonly', command=atualizar)
cb_tv2.set(list_tv2[0])

# FRAME FINAL -----------------------------------------------------------------
frame_end.grid(column=0, row=8, padx=10, pady=5, columnspan=5, sticky="nswe")
var_end = IntVar()
rb_retida = customtkinter.CTkRadioButton(frame_end, text = "OS retida", variable = var_end, value = 1, command=retida)
rb_liberada = customtkinter.CTkRadioButton(frame_end, text = "OS liberada", variable = var_end, value = 2, command=liberada)
rb_cancelada = customtkinter.CTkRadioButton(frame_end, text = "OS cancelada", variable = var_end, value = 3, command=cancelada)
bt_clear = customtkinter.CTkButton(master=frame_end, text="Limpar", command=clear, fg_color="red", hover_color="#d94545", width=120)
bt_copy = customtkinter.CTkButton(master=frame_end, text="Copiar", command=ctrlc, width=120)

for i, widget in enumerate([rb_retida, rb_liberada, rb_cancelada, bt_clear, bt_copy]):
    widget.grid(column=i, row=0, padx=10, pady=5)

# FRAME AUTOR -----------------------------------------------------------------
frame_autor = customtkinter.CTkFrame(master=window, height=20, fg_color="#ebebeb")
frame_autor.grid(column=0, row=10, padx=10, pady=5, columnspan=5, sticky="nswe")

lb_autor = customtkinter.CTkLabel(master = frame_autor, text="Contact for support or further information: vynijales@gmail.com.")
frame_autor.grid_rowconfigure(0, weight=1)
frame_autor.grid_columnconfigure(0, weight=1)
lb_autor.grid(row=0, column=0, sticky="nsew")

window.mainloop()

