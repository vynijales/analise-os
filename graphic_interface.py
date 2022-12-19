from tkinter import *

obs = ""
comeco = ""
fim = ""

def atualizar():
    obs = comeco + fim
    text_obs.delete("1.0","end")
    text_obs.insert(END, obs)
    
    
def clear():
    global obs, comeco, fim
    obs = ""
    comeco = ""
    fim = ""
    atualizar()

def liberada():
    global fim
    fim = "OS liberada e encaminhada para a equipe de assistência."
    atualizar()

def retida():
    global fim
    fim = "OS temporariamente retida pelo N2."
    atualizar()


window = Tk()
#window.geometry("400x400")

window.title("Análise do N2")

#texto_orientacao = Label(window, text="Clique no botão para ver as cotações das moedas. ")
#texto_orientacao.grid(column=0, row=0, padx=10, pady=10)
#
var = IntVar()
 
rb_retida = Radiobutton(window, text = "OS retida", variable = var, value = 1, command=retida)
rb_retida.grid(column=0, row=2, padx = 5, pady = 5)
 
rb_liberada = Radiobutton(window, text = "OS liberada", variable = var, value = 2, command=liberada)
rb_liberada.Checkbutton = False
rb_liberada.grid(column=1, row=2, padx = 5, pady = 5)
#

#botao = Button(window, text="Ok", command=atualizar)
#botao.grid(column=0, row=1, padx=10, pady=10)

bt_clear = Button(window, text = "Limpar", command=clear)
bt_clear.grid(column=2, row=2, padx=10, pady=10)

text_obs = Text(window, width = 50, height=10)
text_obs.grid(column=0, row=0, columnspan=3)

print(obs)
print(fim)



window.mainloop()