from tkinter import *
from tkinter import ttk
import pyperclip as pc
import datetime

from calendar import month_name
    
obs = ""
setor = "N2: "
situacao = ""
fim = ""

txt_sem_acesso = {"onu": "",
"port": "",
"alarm": "",
"pppoe": "",
"desc": "",
"hist": "",
}

txt_sem_sinal = {"area": "",
"port": "",
"alarm": "",
"pppoe": "",
"desc": "",
"hist": "",
}

list_user = [
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
"WALKDERLYPEREIRA"
]


def atualizar():
    global user

    checar_problema()

    user = cb_user.get()

    obs = setor + situacao + fim + "\n\n" + user + rodape()

    text_obs.delete("1.0","end")
    text_obs.insert(END, obs)

def rodape():
    today = datetime.datetime.now()
    td = today.strftime("%d/%m/%Y - %H:%M")
    
    return f" - {td}\n"+("-"*51)

def clear():
    global obs, setor, fim, rodape, situacao
    #setor = ""
    situacao = ""
    fim = ""

    cb_user.set('')

    rb_liberada.Checkbutton = False
    rb_retida.Checkbutton = False
    rb_cancelada.Checkbutton = False
    cb_problem.set("")


    atualizar()

def ctrlc():
    text = text_obs.get("1.0","end-1c")
    pc.copy(text)

def selected(event):
    value = event.widget.get()
    #print("value: '{}'".format(value))
    atualizar()

def liberada():
    global fim
    fim = "OS liberada e encaminhada para a equipe de assistência."
    atualizar()

def retida():
    global fim
    fim = "OS temporariamente retida pelo N2."
    atualizar()

def cancelada():
    global fim
    fim = "Realizado contato com o titular e confirmado normalidade, autorizado cancelamento da OS. Favor baixar sem execução."
    atualizar()
    

def checar_problema():
    if cb_problem.get() == "Sem acesso":
        sem_acesso()
    else:
        com_acesso()

    if cb_problem.get() == "Sem sinal":
        sem_sinal()
    else:
        com_sinal()

    if cb_problem.get() == "Sem sinal Total":
        sinal_total()
    else:
        pass
        #sinal_parcial()

    

def sem_acesso():
    global situacao, txt_sem_acesso
    
    lb_onu.grid(column=0, row=4, padx = 5, pady = 5)
    cb_onu.grid(column=1, row=4, padx = 5, pady = 5)

    cb_port.grid(column=2, row=4, padx = 5, pady = 5)

    cb_alarm.grid(column=3, row=4,)

    cb_hist.grid(column=4, row=4, padx = 5, pady = 5)

    lb_pppoe.grid(column=0, row=5, padx = 5, pady = 5)
    cb_pppoe.grid(column=1, row=5, padx = 5, pady = 5)
    
    cb_desc.grid(column=2, row=5, padx = 5, pady = 5)

    txt_sem_acesso["onu"] = f"ONU {cb_onu.get()}"

    if cb_port.get() == list_port[0]:
        txt_sem_acesso["port"] = "Porta normal"
    else:
        txt_sem_acesso["port"] = "Porta em verificação"
    
    if cb_alarm.get() == list_alarm[0]:
        txt_sem_acesso["alarm"] = "com alarmes recorrentes de LOS/Energia"
    else:
        txt_sem_acesso["alarm"] = "sem alarmes de quedas recorrentes"

    if cb_hist.get() == list_hist[0]:
        txt_sem_acesso["hist"] = "histórico de sinal normal"
    else:
        txt_sem_acesso["hist"] = "com histórico de sinal alterado em -30.0 dBm"
    

    txt_sem_acesso["pppoe"] = f"PPPoE {cb_pppoe.get()}"

    if cb_desc.get() == list_desc[0]:
        txt_sem_acesso["desc"] = "com múltiplas desconexões"
    else:
        txt_sem_acesso["desc"] = "sem múltiplas desconexões"

    situacao = f'{txt_sem_acesso["onu"]}, {txt_sem_acesso["port"]}, {txt_sem_acesso["alarm"]} e {txt_sem_acesso["hist"]}. {txt_sem_acesso["pppoe"]}, {txt_sem_acesso["desc"]}. '

def com_acesso():
    global txt_sem_acesso, situacao

    lb_onu.grid_remove()
    cb_onu.grid_remove()

    cb_port.grid_remove()

    cb_alarm.grid_remove()

    cb_hist.grid_remove()

    lb_pppoe.grid_remove()
    cb_pppoe.grid_remove()

    cb_desc.grid_remove()

    situacao = ""

def sem_sinal():
    global situacao, list_tv, list_tv2, selected_tv2

    lb_tv.grid(column=0, row=4, padx = 5, pady = 5)
    cb_tv.grid(column=1, row=4, padx = 5, pady = 5)

    cb_tv2.grid(column=2, row=4, padx = 5, pady = 5)

    if cb_tv.get() == list_tv[0]:
        list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
        cb_tv2['values'] = list_tv2

        if cb_tv2.get() == list_tv2[0]:
            situacao = f"Cliente possui tecnologia COAXIAL, sem reclamações o suficiente para acionar a Equipe de Rede na Região."
        elif cb_tv2.get() == list_tv2[1]:
            situacao = f"Cliente possui tecnologia COAXIAL, identificado clientes com o mesmo problema na Região. Acionado a Equipe de Rede para verificar. "
        else:
            cb_tv2.set(list_tv2[0])
            sem_sinal()

    elif cb_tv.get() == list_tv[1]:
        list_tv2 = ["RX NORMAL", "RX ALTERADO", "SINAL OFF"]
        cb_tv2['values'] = list_tv2
        
        if cb_tv2.get() == list_tv2[0]:
            situacao = f"Cliente possui tecnologia FTTH, Sinal 1490 normal. "
        elif cb_tv2.get() == list_tv2[1]:
            situacao = f"Cliente possui tecnologia FTTH, Sinal 1490 alterado (-30.0 dBm). "
        elif cb_tv2.get() == list_tv2[2]:
            situacao = f"Cliente possui tecnologia FTTH, está sem sinal de Internet e TV"
            cb_port.grid(column=3, row=4, padx = 5, pady = 5)
            if cb_port.get() == "PORTA EM VERIFICAÇÃO":
                situacao += ", porta em verificação. "
            situacao += "."
        else:
            cb_tv2.set(list_tv2[0])
            sem_sinal()
    
    elif cb_tv.get() == list_tv[2]:
        list_tv2 = ["LOGIN OK", "LOGIN OFF"]
        cb_tv2['values'] = list_tv2

        if cb_tv2.get() == list_tv2[0]:
            situacao = f"Cliente possui tecnologia TV BOX PREMIUM, testado login na Plataforma WEB, aparentemente normal. "
        elif cb_tv2.get() == list_tv2[1]:
            situacao = f"Cliente possui tecnologia TV BOX PREMIUM, testado login na Plataforma WEB, sem acesso. Situação encaminhada para o CQ. "
        else:
            cb_tv2.set(list_tv2[0])
            sem_sinal()

def com_sinal():
    lb_tv.grid_remove()
    cb_tv.grid_remove()
    cb_tv2.grid_remove()
    if cb_tv2.get() == "SINAL OFF":
        cb_port.grid_remove()

def sinal_total():
    global situacao, txt_sem_acesso
    
    lb_onu.grid(column=0, row=4, padx = 5, pady = 5)
    cb_onu.grid(column=1, row=4, padx = 5, pady = 5)

    cb_port.grid(column=2, row=4, padx = 5, pady = 5)

    cb_alarm.grid(column=3, row=4,)

    cb_hist.grid(column=4, row=4, padx = 5, pady = 5)

    lb_pppoe.grid(column=0, row=5, padx = 5, pady = 5)
    cb_pppoe.grid(column=1, row=5, padx = 5, pady = 5)
    
    cb_desc.grid(column=2, row=5, padx = 5, pady = 5)

    lb_tv.grid(column=0, row=6, padx = 5, pady = 5)
    cb_tv.grid(column=1, row=6, padx = 5, pady = 5)

    cb_tv2.grid(column=2, row=6, padx = 5, pady = 5)

    txt_sem_acesso["onu"] = f"ONU {cb_onu.get()}"

    if cb_port.get() == list_port[0]:
        txt_sem_acesso["port"] = "Porta normal"
    else:
        txt_sem_acesso["port"] = "Porta em verificação"
    
    if cb_alarm.get() == list_alarm[0]:
        txt_sem_acesso["alarm"] = "com alarmes recorrentes de LOS/Energia"
    else:
        txt_sem_acesso["alarm"] = "sem alarmes de quedas recorrentes"

    if cb_hist.get() == list_hist[0]:
        txt_sem_acesso["hist"] = "histórico de sinal normal"
    else:
        txt_sem_acesso["hist"] = "com histórico de sinal alterado em -30.0 dBm"
    

    txt_sem_acesso["pppoe"] = f"PPPoE {cb_pppoe.get()}"

    if cb_desc.get() == list_desc[0]:
        txt_sem_acesso["desc"] = "com múltiplas desconexões"
    else:
        txt_sem_acesso["desc"] = "sem múltiplas desconexões"

    situacao = f'{txt_sem_acesso["onu"]}, {txt_sem_acesso["port"]}, {txt_sem_acesso["alarm"]} e {txt_sem_acesso["hist"]}. {txt_sem_acesso["pppoe"]}, {txt_sem_acesso["desc"]}. '

    #TV

    if cb_tv.get() == list_tv[0]:
        list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
        cb_tv2['values'] = list_tv2

        if cb_tv2.get() == list_tv2[0]:
            situacao += f"Cliente possui tecnologia COAXIAL, sem reclamações o suficiente para acionar a Equipe de Rede na Região."
        elif cb_tv2.get() == list_tv2[1]:
            situacao += f"Cliente possui tecnologia COAXIAL, identificado clientes com o mesmo problema na Região. Acionado a Equipe de Rede para verificar. "
        else:
            cb_tv2.set(list_tv2[0])
            sinal_total()

    elif cb_tv.get() == list_tv[1]:
        list_tv2 = ["RX NORMAL", "RX ALTERADO", "SINAL OFF"]
        cb_tv2['values'] = list_tv2
        
        if cb_tv2.get() == list_tv2[0]:
            situacao += f"Cliente possui tecnologia FTTH, Sinal 1490 normal. "
        elif cb_tv2.get() == list_tv2[1]:
            situacao += f"Cliente possui tecnologia FTTH, Sinal 1490 alterado (-30.0 dBm). "
        elif cb_tv2.get() == list_tv2[2]:
            situacao += f"Cliente possui tecnologia FTTH, está sem sinal de Internet e TV"
            if cb_port.get() == "PORTA EM VERIFICAÇÃO":
                situacao += ", afetado em verificação. "
            situacao += "."
            
        else:
            cb_tv2.set(list_tv2[0])
            sinal_total()
    
    elif cb_tv.get() == list_tv[2]:
        list_tv2 = ["LOGIN OK", "LOGIN OFF"]
        cb_tv2['values'] = list_tv2

        if cb_tv2.get() == list_tv2[0]:
            situacao += f"Cliente possui tecnologia TV BOX PREMIUM, testado login na Plataforma WEB, aparentemente normal. "
        elif cb_tv2.get() == list_tv2[1]:
            situacao += f"Cliente possui tecnologia TV BOX PREMIUM, testado login na Plataforma WEB, sem acesso. Situação encaminhada para o CQ. "
        else:
            cb_tv2.set(list_tv2[0])
            sinal_total()


"""def sinal_parcial():
    lb_onu.grid_remove()
    cb_onu.grid_remove()

    cb_port.grid_remove()

    cb_alarm.grid_remove()

    cb_hist.grid_remove()

    lb_pppoe.grid_remove()
    cb_pppoe.grid_remove()

    cb_desc.grid_remove()

    lb_tv.grid_remove()
    cb_tv.grid_remove()
    cb_tv2.grid_remove()"""

# JANELA PRINCIPAL ==========================================================================
window = Tk()

window.title("Análise do N2")

# OPÇÕES SUPERIORES ==========================================================================
# LABEL AND COMBOBOX - USER -----------------------------------------------------------------

lb_user = Label(window, text="USUÁRIO: ")
lb_user.grid(column=2, row=0, padx=0, pady=10)

selected_user = StringVar()
cb_user = ttk.Combobox(window, textvariable=selected_user)
cb_user['values'] = list_user

cb_user['state'] = 'readonly'
cb_user.grid(column=3,row=0, padx = 0, pady=0)

cb_user.bind("<<ComboboxSelected>>", selected)


# TEXTO PRINCIPAL -----------------------------------------------------------------
text_obs = Text(window, width = 55, height=10, wrap=WORD)
text_obs.grid(column=0, row=2, columnspan=5)

# SEM ACESSO A INTERNE =================================================================
# COMBOBOX - PROBLEMA -----------------------------------------------------------------

lb_problem = Label(window, text="PROBLEMA: ")
lb_problem.grid(column=0, row=0, padx=0, pady=0)

list_problem = ["","Sem sinal", "Sem acesso", "Sem sinal Total", "Lentidão"]

selected_problem = StringVar()
cb_problem = ttk.Combobox(window, textvariable=selected_problem, width=15)
cb_problem['values'] = list_problem
cb_problem['state'] = 'readonly'
cb_problem.grid(column=1,row=0, padx=0, pady=0)
cb_problem.bind("<<ComboboxSelected>>", selected)

# LABEL/COMBOBOX - ONU -----------------------------------------------------------------
lb_onu = Label(window, text="ONU: ")
list_onu = ["ONLINE", "OFFLINE (LOS)", "OFFLINE (ENERGIA)"]

selected_onu = StringVar()
cb_onu = ttk.Combobox(window, textvariable=selected_onu,)
cb_onu.set(list_onu[0])
cb_onu['values'] = list_onu
cb_onu['state'] = 'readonly'
cb_onu.bind("<<ComboboxSelected>>", selected)

# LABEL/COMBOBOX - PORTA -----------------------------------------------------------------
list_port = ["PORTA NORMAL", "PORTA EM VERIFICAÇÃO"]
selected_port = StringVar()
cb_port = ttk.Combobox(window, textvariable=selected_port,)
cb_port.set(list_port[0])
cb_port['values'] = list_port
cb_port['state'] = 'readonly'
cb_port.bind("<<ComboboxSelected>>", selected)

# LABEL/COMBOBOX - ALARMES -----------------------------------------------------------------
list_alarm = ["C/ ALARMES", "S/ ALARMES"]
selected_alarm = StringVar()
cb_alarm = ttk.Combobox(window, textvariable=selected_alarm,)
cb_alarm.set(list_alarm[1])
cb_alarm['values'] = list_alarm
cb_alarm['state'] = 'readonly'
cb_alarm.bind("<<ComboboxSelected>>", selected)

# LABEL/COMBOBOX - PPPOE -----------------------------------------------------------------
lb_pppoe = Label(window, text="PPPOE: ")
list_pppoe = ["CONECTADO", "DESCONECTADO"]

selected_pppoe = StringVar()
cb_pppoe = ttk.Combobox(window, textvariable=selected_pppoe,)
cb_pppoe.set(list_pppoe[0])
cb_pppoe['values'] = list_pppoe
cb_pppoe['state'] = 'readonly'
cb_pppoe.bind("<<ComboboxSelected>>", selected)

# COMBOBOX - DESCONEXÕES -----------------------------------------------------------------
list_desc = ["C/ DESCONEXÕES", "S/ DESCONEXÕES"]
selected_desc = StringVar()
cb_desc = ttk.Combobox(window, textvariable=selected_desc,)
cb_desc.set(list_desc[1])
cb_desc['values'] = list_desc
cb_desc['state'] = 'readonly'
cb_desc.bind("<<ComboboxSelected>>", selected)

# COMBOBOX - HISTÓRICO DE SINAL  -----------------------------------------------------------------------------------
list_hist = ["HISTÓRICO NORMAL", "HISTÓRICO ALTERADO"]
selected_hist = StringVar()
cb_hist = ttk.Combobox(window, textvariable=selected_hist,)
cb_hist.set(list_hist[0])
cb_hist['values'] = list_hist
cb_hist['state'] = 'readonly'
cb_hist.bind("<<ComboboxSelected>>", selected)

# SEM SINAL --------------------------------------------------------------------------------------------------------
# LB/COMBOBOX - TIPO de TV
lb_tv = Label(window, text= "TECNOLOGIA: ")

list_tv = ["COAXIAL", "TV-FIBRA", "BOX-PREMIUM"]
selected_tv = StringVar()
cb_tv = ttk.Combobox(window, textvariable=selected_tv,)
cb_tv.set(list_tv[0])
cb_tv['values'] = list_tv
cb_tv['state'] = 'readonly'
cb_tv.bind("<<ComboboxSelected>>", selected)

list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
selected_tv2 = StringVar()
cb_tv2 = ttk.Combobox(window, textvariable=selected_tv2,)
cb_tv2.set(list_tv2[0])
cb_tv2['values'] = list_tv2
cb_tv2['state'] = 'readonly'
cb_tv2.bind("<<ComboboxSelected>>", selected)


# LENTIDÃO ================================================================================================
# RADIO BUTTONS - OS LIBERADA / RETIDA / CANCELADA -----------------------------------------------------------------

lb_lent = Label(window, text= ": ")

list_tv = ["COAXIAL", "TV-FIBRA", "BOX-PREMIUM"]
selected_tv = StringVar()
cb_tv = ttk.Combobox(window, textvariable=selected_tv,)
cb_tv.set(list_tv[0])
cb_tv['values'] = list_tv
cb_tv['state'] = 'readonly'
cb_tv.bind("<<ComboboxSelected>>", selected)

list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
selected_tv2 = StringVar()
cb_tv2 = ttk.Combobox(window, textvariable=selected_tv2,)
cb_tv2.set(list_tv2[0])
cb_tv2['values'] = list_tv2
cb_tv2['state'] = 'readonly'
cb_tv2.bind("<<ComboboxSelected>>", selected)


# FIM DA OBSERVAÇÃO ================================================================================================
# RADIO BUTTONS - OS LIBERADA / RETIDA / CANCELADA -----------------------------------------------------------------
var_end = IntVar()

rb_retida = Radiobutton(window, text = "OS retida", variable = var_end, value = 1, command=retida)
rb_retida.grid(column=0, row=8, padx = 5, pady = 5)
 
rb_liberada = Radiobutton(window, text = "OS liberada", variable = var_end, value = 2, command=liberada)
rb_liberada.grid(column=1, row=8, padx = 5, pady = 5)

rb_cancelada = Radiobutton(window, text = "OS cancelada", variable = var_end, value = 3, command=cancelada)
rb_cancelada.grid(column=2, row=8, padx = 5, pady = 5)

# BUTTON CLEAR -----------------------------------------------------------------
bt_clear = Button(window, text="Limpar", command=clear)
bt_clear.grid(column=3, row=8, padx=10, pady=10)

# BUTTON COPY -----------------------------------------------------------------
bt_copy = Button(window, text="Copiar", command=ctrlc)
bt_copy.grid(column=4, row=8, padx=10, pady=10)

window.mainloop()