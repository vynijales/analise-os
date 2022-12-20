from tkinter import *
from tkinter import ttk
import pyperclip as pc
import datetime

from calendar import month_name
    
obs = ""
setor = "N2: "
situacao = ""
fim = ""

txt_sem_acesso = {"txt_onu": "",
"txt_port": "",
"txt_alarm": "",
"txt_pppoe": "",
"txt_desc": "",
}

list_user = ["ANAFREITAS", "EDUARDOBARRETO", "IGOR", "JOYCEJORDANIA", "MATHEUSVYNICIUS", "NAELSONGERMANO"]


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

def sem_acesso():
    global situacao, txt_sem_acesso
    
    lb_onu.grid(column=0, row=4, padx = 5, pady = 5)
    cb_onu.grid(column=1, row=4, padx = 5, pady = 5)

    cb_port.grid(column=2, row=4, padx = 5, pady = 5)

    cb_alarm.grid(column=3, row=4,)

    lb_pppoe.grid(column=0, row=5, padx = 5, pady = 5)
    cb_pppoe.grid(column=1, row=5, padx = 5, pady = 5)
    
    cb_desc.grid(column=2, row=5, padx = 5, pady = 5)


    txt_sem_acesso["txt_onu"] = f"ONU {cb_onu.get()}"

    if cb_port.get() == list_port[0]:
        txt_sem_acesso["txt_port"] = "Porta normal"
    else:
        txt_sem_acesso["txt_port"] = "Porta em verificação"
    
    if cb_alarm.get() == list_alarm[0]:
        txt_sem_acesso["txt_alarm"] = "com alarmes recorrentes de LOS/Energia"
    else:
        txt_sem_acesso["txt_alarm"] = "sem alarmes recorrentes"

    txt_sem_acesso["txt_pppoe"] = f"PPPoE {cb_pppoe.get()}"

    if cb_desc.get() == list_desc[0]:
        txt_sem_acesso["txt_desc"] = "com múltiplas desconexões"
    else:
        txt_sem_acesso["txt_desc"] = "sem múltiplas desconexões"

    situacao = f'{txt_sem_acesso["txt_onu"]}, {txt_sem_acesso["txt_port"]}, {txt_sem_acesso["txt_alarm"]}. {txt_sem_acesso["txt_pppoe"]}, {txt_sem_acesso["txt_desc"]}. '

def com_acesso():
    lb_onu.grid_remove()
    cb_onu.grid_remove()

    cb_port.grid_remove()

    cb_alarm.grid_remove()

    lb_pppoe.grid_remove()
    cb_pppoe.grid_remove()

    cb_desc.grid_remove()


window = Tk()
#window.geometry("400x400")

window.title("Análise do N2")

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

# COMBOBOX - PROBLEMA -----------------------------------------------------------------

lb_problem = Label(window, text="PROBLEMA: ")
lb_problem.grid(column=0, row=0, padx=0, pady=0)

list_problem = ["","Sem sinal total", "Sem acesso", "Lentidão"]

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