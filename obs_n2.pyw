from tkinter import *
from tkinter import ttk
import customtkinter
import pyperclip as pc
import datetime

dados = {
  "SECTOR": "N2: ",
  "USERS": [
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
  "PROBLEM": [
    "",
    "TV",
    "INTERNET",
    "TV e INTERNET"
  ],
  "ONU_STATUS": [
    "ONLINE",
    "OFFLINE (LOS)",
    "OFFLINE (ENERGIA)",
    "ONU CADASTRADA"
  ],
  "PORT": [
    "PORTA NORMAL",
    "PORTA EM VERIFICAÇÃO"
  ],
  "ONU_ALARM": [
    "C/ ALARMES",
    "S/ ALARMES"
  ],
  "PPPOE_STATUS": [
    "CONECTADO",
    "DESCONECTADO"
  ],
  "PPPOE_HIST": [
    "C/ DESCONEXÕES",
    "S/ DESCONEXÕES"
  ],
  "COAXIAL": [
    "COAXIAL",
    "TV-FIBRA",
    "BOX-PREMIUM"
  ],
  "LENT": [
    "",
    "Checado VLAN, GATEWAY e IP. Velocidade contratada liberada no CMTS e ONU cadastrada com Port Rate /1000"
  ]
}

obs = ""
setor = "N2: "
situacao = ""
end = ""

db = {"onu": "",
"port": "",
"alarm": "",
"pppoe": "",
"desc": "",
"hist": "",
"lent": "",
}

def atualizar(variable):
    global user
    checar_problema()
    user = cb_user.get()
    text_obs.delete("1.0", "end")
    text_obs.insert(END, f"{setor + situacao + end}\n\n{user}{rodape()}")


def rodape():
    today = datetime.datetime.now()
    td = today.strftime("%d/%m/%Y - %H:%M")
    
    return f" - {td}\n"+("-"*51)

def clear():
    global obs, setor, end, situacao
    situacao = ""
    cb_problem.set("")

    atualizar(True)

def ctrlc():
    text = text_obs.get("1.0","end-1c")
    pc.copy(text)

def liberada():
    global end
    end = "OS liberada e encaminhada para a equipe de assistência."
    atualizar(True)

def retida():
    global end
    end = "OS temporariamente retida pelo N2."
    atualizar(True)

def cancelada():
    global end
    end = "Realizado contato com o titular e confirmado normalidade, autorizado cancelamento da OS. Favor baixar sem execução."
    atualizar(True)
    

def checar_problema():
    if cb_problem.get() == "INTERNET":
        sem_acesso()
    else:
        com_acesso()

    if cb_problem.get() == "TV":
        sem_sinal()
    else:
        com_sinal()

    if cb_problem.get() == "TV e INTERNET":
        sinal_total()
    else:
        pass
    

def sem_acesso():
    global situacao
    for i, widget in enumerate([frame_onu, frame_pppoe]):
        widget.grid(column=0, row=(i + 4), padx=10, pady=5, columnspan=5, sticky="nswe")
    
    for i, widget in enumerate([cb_onu, cb_port, cb_alarm, cb_hist]):
        widget.grid(column=(i + 1), row=0, padx=5, pady=5)
    
    for i, widget in enumerate([cb_pppoe, cb_desc, spacer2, sw_lentidao]):
        widget.grid(column=(i + 1), row=0, padx=5, pady=5)

    db = {
        "ONU": f"ONU {cb_onu.get()}",
        "PORT": "porta normal" if cb_port.get() == list_port[0] else "porta em verificação",
        "ALARM": "com alarmes recorrentes de LOS/Energia" if cb_alarm.get() == list_alarm[0] else "sem alarmes de quedas recorrentes",
        "HIST": "histórico de sinal normal" if cb_hist.get() == list_hist[0] else "com histórico de sinal alterado em -30.0 dBm",
        "PPPOE": f"PPPoE {cb_pppoe.get()}",
        "DESC": "com múltiplas desconexões" if cb_desc.get() == list_desc[0] else "sem múltiplas desconexões",
        "LENT": "Checado VLAN, GATEWAY e IP. Velocidade liberada no CMTS e ONU cadastrada com Port Rate /1000." if sw_lentidao.get() else ""
    }

    situacao = f'{db["ONU"]}, {db["PORT"]}, {db["ALARM"]} e {db["HIST"]}. {db["PPPOE"]}, {db["DESC"]}. {db["LENT"]}'

def com_acesso():
    global situacao
    for widget in (frame_onu, frame_pppoe):
        widget.grid_remove()
    situacao = ""


def sem_sinal():
    global situacao
    frame_tv.grid(column=0, row=6, padx=5, pady=5, columnspan=5, sticky="nswe")
    for i, widget in enumerate([cb_tv, cb_tv2]):
        widget.grid(column=(i + 1), row=4, padx=5, pady=5)

    db = {
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
    }

    tecnologia_selecionada = cb_tv.get()
    if tecnologia_selecionada in db:
        cb_tv2["values"] = list(db[tecnologia_selecionada].keys())
        cb_tv2.configure(values=list(db[tecnologia_selecionada].keys()))

        opcao_selecionada = cb_tv2.get()
        if opcao_selecionada in db[tecnologia_selecionada]:
            situacao = db[tecnologia_selecionada][opcao_selecionada]
        else:
            cb_tv2.set(list(db[tecnologia_selecionada].keys())[0])
            situacao = db[tecnologia_selecionada][cb_tv2.get()]


def com_sinal():
    frame_tv.grid_remove()

    if cb_tv2.get() == "SINAL OFF":
        cb_port.grid_remove()

def sinal_total():
    global situacao, db
    sem_acesso()
    sem_sinal()


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

cb_user = customtkinter.CTkComboBox(frame_head, width=157, values = dados["USERS"], state='readonly', command=atualizar)
cb_user.set(dados["USERS"][7])
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

