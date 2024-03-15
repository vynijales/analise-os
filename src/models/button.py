from customtkinter import CTkButton, CTkRadioButton

from components.controller import Controller


class Button(CTkButton):
    def __init__(self, master, text, command, **kwargs):
        super().__init__(master, text=text, command=command, width=95, **kwargs)
        master.add_widget(self)


class RadioButton(CTkRadioButton):
    def __init__(self, master, text, view, **kwargs):
        super().__init__(master, text=text, value=text, variable=view.variable, command=lambda: Controller.atualizar(view, text), **kwargs)
        master.add_widget(self)
