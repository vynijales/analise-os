from customtkinter import CTkComboBox

from components.controller import Controller

class ComboBox(CTkComboBox):
    def __init__(self, master, values, view, **kwargs):
        comand = lambda value: Controller.atualizar(view, value)
        super().__init__(master, width=157, values=values, state="readonly", command=comand, **kwargs)
        master.add_widget(self)
        self.set(values[0])
