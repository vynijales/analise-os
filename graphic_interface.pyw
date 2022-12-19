from tkinter import *
from tkinter import ttk
import pyperclip as pc
import datetime

from calendar import month_name
    
obs = ""
setor = "N2: "
list_user = ["ANAFREITAS", "EDUARDOBARRETO", "IGOR", "JOYCEJORDANIA", "MATHEUSVYNICIUS", "NAELSONGERMANO"
        ]

fim = ""

def atualizar():
    global user


    user = cb_user.get()

    obs = setor + fim + "\n\n" + user + rodape()

    text_obs.delete("1.0","end")
    text_obs.insert(END, obs)

def rodape():
    today = datetime.datetime.now()
    td = today.strftime("%d/%m/%Y - %H:%M")
    
    return f" - {td}\n"+("-"*51)

def clear():
    global obs, setor, fim, rodape
    #setor = ""
    fim = ""

    cb_user.set('')

    rb_liberada.Checkbutton = False
    rb_retida.Checkbutton = False
    rb_cancelada.Checkbutton = False

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


window = Tk()
#window.geometry("400x400")

window.title("Análise do N2")

# LABEL AND COMBOBOX - USER

lb_user = Label(window, text="USUÁRIO: ")
lb_user.grid(column=0, row=0, padx=10, pady=10)

selected_user = StringVar()
cb_user = ttk.Combobox(window, textvariable=selected_user)
cb_user['values'] = list_user
# prevent typing a value
cb_user['state'] = 'readonly'
cb_user.bind(atualizar)
cb_user.grid(column=1,row=0)

cb_user.bind("<<ComboboxSelected>>", selected)


# TEXTO PRINCIPAL
text_obs = Text(window, width = 55, height=10)
text_obs.grid(column=0, row=1, columnspan=5)

# RADIO BUTTONS - OS LIBERADA / RETIDA
var = IntVar()

rb_retida = Radiobutton(window, text = "OS retida", variable = var, value = 1, command=retida)
rb_retida.grid(column=0, row=4, padx = 5, pady = 5)
 
rb_liberada = Radiobutton(window, text = "OS liberada", variable = var, value = 2, command=liberada)
rb_liberada.grid(column=1, row=4, padx = 5, pady = 5)

rb_cancelada = Radiobutton(window, text = "OS cancelada", variable = var, value = 3, command=cancelada)
rb_cancelada.grid(column=2, row=4, padx = 5, pady = 5)

# BUTTON CLEAR
bt_clear = Button(window, text = "Limpar", command=clear)
bt_clear.grid(column=3, row=4, padx=10, pady=10)

# BUTTON COPY
bt_copy = Button(window, text = "Copiar", command=ctrlc)
bt_copy.grid(column=4, row=4, padx=10, pady=10)

window.mainloop()