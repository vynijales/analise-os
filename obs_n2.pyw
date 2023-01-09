from tkinter import *
from tkinter import ttk
import customtkinter
import pyperclip as pc
import datetime
import json
from calendar import month_name

with open("db.json",'r') as json_file:
    dados = json.load(json_file)

print(dados) 

class OBS_N2():
    def __init__(self) -> None:
        super().__init__()
        self.setor = 'N2'
        self.obs = ''
        self.situacao = ''
        self.fim = ''
    
    

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
"lent": "",
}

txt_sem_sinal = {"area": "",
"port": "",
"alarm": "",
"pppoe": "",
"desc": "",
"hist": "",
}

list_user = dados['USERS']


def atualizar(variable):
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

    # cb_user.set('')

    rb_liberada.Checkbutton = False
    rb_retida.Checkbutton = False
    rb_cancelada.Checkbutton = False
    cb_problem.set("")

    atualizar(True)

def ctrlc():
    text = text_obs.get("1.0","end-1c")
    pc.copy(text)

def liberada():
    global fim
    fim = "OS liberada e encaminhada para a equipe de assistência."
    atualizar(True)

def retida():
    global fim
    fim = "OS temporariamente retida pelo N2."
    atualizar(True)

def cancelada():
    global fim
    fim = "Realizado contato com o titular e confirmado normalidade, autorizado cancelamento da OS. Favor baixar sem execução."
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
    global situacao, txt_sem_acesso
    
    frame_onu.grid(column=0, row=4, padx=10, pady=5, columnspan=4, sticky="nswe")
    frame_pppoe.grid(column=0, row=5, padx=10, pady=5, columnspan=2, sticky="nswe")

    lb_onu.grid(column=0, row=4, padx = 5, pady = 5)
    cb_onu.grid(column=1, row=4, padx = 5, pady = 5)

    cb_port.grid(column=2, row=4, padx = 5, pady = 5)

    cb_alarm.grid(column=3, row=4,  padx = 5, pady = 5)

    cb_hist.grid(column=4, row=4, padx = 5, pady = 5)

    lb_pppoe.grid(column=0, row=5, padx = 5, pady = 5)
    cb_pppoe.grid(column=1, row=5, padx = 5, pady = 5)
    
    cb_desc.grid(column=2, row=5, padx = 5, pady = 5)

    sw_lentidao.grid(column=4, row=5, padx = 5, pady = 5)

    txt_sem_acesso["ONU"] = f"ONU {cb_onu.get()}"

    if cb_port.get() == list_port[0]:
        txt_sem_acesso["PORT"] = "Porta normal"
    else:
        txt_sem_acesso["PORT"] = "Porta em verificação"
    
    if cb_alarm.get() == list_alarm[0]:
        txt_sem_acesso["ALARM"] = "com alarmes recorrentes de LOS/Energia"
    else:
        txt_sem_acesso["ALARM"] = "sem alarmes de quedas recorrentes"

    if cb_hist.get() == list_hist[0]:
        txt_sem_acesso["HIST"] = "histórico de sinal normal"
    else:
        txt_sem_acesso["HIST"] = "com histórico de sinal alterado em -30.0 dBm"
    

    txt_sem_acesso["PPPOE"] = f"PPPoE {cb_pppoe.get()}"

    if cb_desc.get() == list_desc[0]:
        txt_sem_acesso["DESC"] = "com múltiplas desconexões"
    else:
        txt_sem_acesso["DESC"] = "sem múltiplas desconexões"

    if sw_lentidao.get():
        txt_sem_acesso['LENT'] = f"Checado VLAN, GATEWAY e IP. Velocidade liberada no CMTS e ONU cadastrada com Port Rate /1000. "
        
    else:
        txt_sem_acesso['LENT'] = ""
        # sw_lentidao.configure(state="disabled")

    situacao = f'{txt_sem_acesso["ONU"]}, {txt_sem_acesso["PORT"]}, {txt_sem_acesso["ALARM"]} e {txt_sem_acesso["HIST"]}. {txt_sem_acesso["PPPOE"]}, {txt_sem_acesso["DESC"]}. {txt_sem_acesso["LENT"]}'

def com_acesso():
    global txt_sem_acesso, situacao

    frame_onu.grid_remove()
    frame_pppoe.grid_remove()

    lb_onu.grid_remove()
    cb_onu.grid_remove()

    cb_port.grid_remove()

    cb_alarm.grid_remove()

    cb_hist.grid_remove()

    lb_pppoe.grid_remove()
    cb_pppoe.grid_remove()

    cb_desc.grid_remove()
    
    sw_lentidao.grid_remove()

    situacao = ""

def sem_sinal():
    global situacao, list_tv, list_tv2, selected_tv2

    frame_tv.grid(column=0, row=6, padx = 5, pady = 5, columnspan=5)

    lb_tv.grid(column=0, row=4, padx = 5, pady = 5)
    cb_tv.grid(column=1, row=4, padx = 5, pady = 5)

    cb_tv2.grid(column=2, row=4, padx = 5, pady = 5)

    if cb_tv.get() == list_tv[0]:
        list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
        cb_tv2['values'] = list_tv2
        cb_tv2.configure(values=list_tv2)

        if cb_tv2.get() == list_tv2[0]:
            situacao = f"Cliente possui tecnologia COAXIAL, sem reclamações o suficiente para acionar a Equipe de Rede na Região. "
        elif cb_tv2.get() == list_tv2[1]:
            situacao = f"Cliente possui tecnologia COAXIAL, identificado clientes com o mesmo problema na Região. Acionado a Equipe de Rede para verificar. "
        else:
            cb_tv2.set(list_tv2[0])
            sem_sinal()

    elif cb_tv.get() == list_tv[1]:
        list_tv2 = ["RX NORMAL", "RX ALTERADO", "SINAL OFF"]
        cb_tv2['values'] = list_tv2
        cb_tv2.configure(values=list_tv2)

        if cb_tv2.get() == list_tv2[0]:
            situacao = f"Cliente possui tecnologia TV-FIBRA, Sinal 1490 normal. "
        elif cb_tv2.get() == list_tv2[1]:
            situacao = f"Cliente possui tecnologia TV-FIBRA, Sinal 1490 alterado (-30.0 dBm). "
        elif cb_tv2.get() == list_tv2[2]:
            situacao = f"Cliente possui tecnologia TV-FIBRA, está sem sinal de Internet e TV"
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
        cb_tv2.configure(values=list_tv2)

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

    sw_lentidao.grid(column=4, row=5, padx = 5, pady = 5)

    txt_sem_acesso["ONU"] = f"ONU {cb_onu.get()}"

    if cb_port.get() == list_port[0]:
        txt_sem_acesso["PORT"] = "Porta normal"
    else:
        txt_sem_acesso["PORT"] = "Porta em verificação"
    
    if cb_alarm.get() == list_alarm[0]:
        txt_sem_acesso["ALARM"] = "com alarmes recorrentes de LOS/Energia"
    else:
        txt_sem_acesso["ALARM"] = "sem alarmes de quedas recorrentes"

    if cb_hist.get() == list_hist[0]:
        txt_sem_acesso["HIST"] = "histórico de sinal normal"
    else:
        txt_sem_acesso["HIST"] = "com histórico de sinal alterado em -30.0 dBm"
    

    txt_sem_acesso["PPPOE"] = f"PPPoE {cb_pppoe.get()}"

    if cb_desc.get() == list_desc[0]:
        txt_sem_acesso["DESC"] = "com múltiplas desconexões"
    else:
        txt_sem_acesso["DESC"] = "sem múltiplas desconexões"

    if sw_lentidao.get():
        txt_sem_acesso['LENT'] = f"Checado VLAN, GATEWAY e IP. Velocidade liberada no CMTS e ONU cadastrada com Port Rate /1000. "
    else:
        txt_sem_acesso['LENT'] = ''

    situacao = f'{txt_sem_acesso["ONU"]}, {txt_sem_acesso["PORT"]}, {txt_sem_acesso["ALARM"]} e {txt_sem_acesso["HIST"]}. {txt_sem_acesso["PPPOE"]}, {txt_sem_acesso["DESC"]}. {txt_sem_acesso["LENT"]} '

    #TV

    if cb_tv.get() == list_tv[0]:
        list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
        cb_tv2['values'] = list_tv2
        cb_tv2.configure(values=list_tv2)

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
        cb_tv2.configure(values=list_tv2)
        
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
            cb_tv2.configure(values=list_tv2)
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



# JANELA PRINCIPAL ==========================================================================

# style= ttk.Style()
#style.theme_use('light')
# style.configure("customtkinter.CTkComboBox", fieldbackground= "orange", background= "white")

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

window  = customtkinter.CTk()  # create CTk window like you do with the Tk window


window.title("Análise do N2")

# widget.columnconfigure(0, 200)

window.resizable(False, False)

# FRAMES
frame_head = LabelFrame(window, text='INICIO DA ANÁLISE', padx=5, pady=5)
frame_onu = LabelFrame(window, text='ONU', padx=5, pady=5)
frame_pppoe = LabelFrame(window, text='PPPOE', padx=5, pady=5)
frame_tv = LabelFrame(window, text='PPPOE', padx=5, pady=5)
frame_end = LabelFrame(window, text='FIM DA ANÁLISE', padx=5, pady=5)


# OPÇÕES SUPERIORES ==========================================================================cb_user
# LABEL AND COMBOBOX - USER -----------------------------------------------------------------
frame_head.grid(column=0, row=0, padx=10, pady=5, columnspan=5, sticky="nswe")
lb_user = customtkinter.CTkLabel(frame_head, text="USUÁRIO: ",)
lb_user.grid(column=3, row=0, padx=0, pady=10, sticky=E)


cb_user = customtkinter.CTkComboBox(frame_head, width=157, values = list_user, state='readonly', command=atualizar)
cb_user.set(list_user[7])
cb_user.grid(column=4,row=0, padx = 0, pady=0, sticky=W)

# cb_user.bind("<<ComboboxSelected>>", selected)


# TEXTO PRINCIPAL -----------------------------------------------------------------
# text_obs = Text(window, width = 55, height=10, wrap=WORD)
text_obs = customtkinter.CTkTextbox(window, width=750, height=300, wrap=WORD, font=customtkinter.CTkFont(size=14,))
text_obs.grid(column=0, row=2, columnspan=5, sticky=W,)

# SEM ACESSO A INTERNE =================================================================
# COMBOBOX - PROBLEMA -----------------------------------------------------------------

lb_problem = customtkinter.CTkLabel(frame_head, text="PROBLEMA: ", )
lb_problem.grid(column=0, row=0, padx=0, pady=0, sticky=W)

list_problem = ["", "TV", "INTERNET", "TV e INTERNET",]

cb_problem = customtkinter.CTkComboBox(frame_head, values = list_problem, state='readonly', command=atualizar)
cb_problem.grid(column=1,row=0, padx=0, pady=0,)

# LABEL/COMBOBOX - ONU -----------------------------------------------------------------
lb_onu = customtkinter.CTkLabel(frame_onu, text="ONU: ")
list_onu = ["ONLINE", "OFFLINE (LOS)", "OFFLINE (ENERGIA)"]

# selected_onu = StringVar()
cb_onu = customtkinter.CTkComboBox(frame_onu, values = list_onu, state='readonly', command=atualizar)
cb_onu.set(list_onu[0])

# LABEL/COMBOBOX - PORTA -----------------------------------------------------------------
list_port = ["PORTA NORMAL", "PORTA EM VERIFICAÇÃO"]
cb_port = customtkinter.CTkComboBox(frame_onu, values = list_port, state='readonly', command=atualizar)
cb_port.set(list_port[0])

# customtkinter.CTkLabel/COMBOBOX - ALARMES -----------------------------------------------------------------
list_alarm = ["C/ ALARMES", "S/ ALARMES"]
cb_alarm = customtkinter.CTkComboBox(frame_onu, values = list_alarm, state='readonly', command=atualizar)
cb_alarm.set(list_alarm[1])

# LABEL/COMBOBOX - PPPOE -----------------------------------------------------------------
lb_pppoe = customtkinter.CTkLabel(frame_pppoe, text="PPPOE: ")
list_pppoe = ["CONECTADO", "DESCONECTADO"]

cb_pppoe = customtkinter.CTkComboBox(frame_pppoe, values = list_pppoe, state='readonly', command=atualizar)
cb_pppoe.set(list_pppoe[0])

# COMBOBOX - DESCONEXÕES -----------------------------------------------------------------
list_desc = ["C/ DESCONEXÕES", "S/ DESCONEXÕES"]
cb_desc = customtkinter.CTkComboBox(frame_pppoe, values = list_desc, state='readonly', command=atualizar)
cb_desc.set(list_desc[1])

# COMBOBOX - HISTÓRICO DE SINAL  -----------------------------------------------------------------------------------
list_hist = ["HISTÓRICO NORMAL", "HISTÓRICO ALTERADO"]
cb_hist = customtkinter.CTkComboBox(frame_onu, values = list_hist, state='readonly', command=atualizar)
cb_hist.set(list_hist[0])

# SEM SINAL --------------------------------------------------------------------------------------------------------
# LB/COMBOBOX - TIPO de TV
lb_tv = customtkinter.CTkLabel(window, text= "TECNOLOGIA: ")

list_tv = ["COAXIAL", "TV-FIBRA", "BOX-PREMIUM"]
cb_tv = customtkinter.CTkComboBox(window, values = list_tv, state='readonly', command=atualizar)
cb_tv.set(list_tv[0])

list_tv2 = ["ÁREA NORMAL", "ÁREA EM VERIFICAÇÃO"]
cb_tv2 = customtkinter.CTkComboBox(window, values = list_tv2, state='readonly', command=atualizar)
cb_tv2.set(list_tv2[0])

# LENTIDÃO ================================================================================================
# LB/COMBOBOX - OS LIBERADA / RETIDA / CANCELADA -----------------------------------------------------------------

sw_lentidao = customtkinter.CTkSwitch(master=window, command=lambda: atualizar(True), text="LENTIDÃO", state='disable')

# FIM DA OBSERVAÇÃO ================================================================================================
# RADIO BUTTONS - OS LIBERADA / RETIDA / CANCELADA -----------------------------------------------------------------

frame_end.grid(column=0, row=8, padx=10, pady=5, columnspan=5, sticky="nswe")

var_end = IntVar()

rb_retida = customtkinter.CTkRadioButton(frame_end, text = "OS retida", variable = var_end, value = 1, command=retida)
rb_retida.grid(column=0, row=8, padx = 5, pady = 5)
 
rb_liberada = customtkinter.CTkRadioButton(frame_end, text = "OS liberada", variable = var_end, value = 2, command=liberada)
rb_liberada.grid(column=1, row=8, padx = 5, pady = 5)

rb_cancelada = customtkinter.CTkRadioButton(frame_end, text = "OS cancelada", variable = var_end, value = 3, command=cancelada)
rb_cancelada.grid(column=2, row=8, padx = 5, pady = 5)

# BUTTON CLEAR -----------------------------------------------------------------
bt_clear = customtkinter.CTkButton(master=frame_end, text="Limpar", command=clear, fg_color="red", hover_color="#d94545")
bt_clear.grid(column=3, row=8, padx=10, pady=10)

#bt_clear = Button(window, text="Limpar", command=clear)
#bt_clear.grid(column=3, row=8, padx=10, pady=10)

# BUTTON COPY -----------------------------------------------------------------

bt_copy = customtkinter.CTkButton(master=frame_end, text="Copiar", command=ctrlc)
bt_copy.grid(column=4, row=8, padx=10, pady=10)

# bt_copy = Button(window, text="Copiar", command=ctrlc)
# bt_copy.grid(column=4, row=8, padx=10, pady=10)

window.mainloop()