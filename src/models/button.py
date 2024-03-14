from customtkinter import CTkButton, CTkRadioButton


class Button(CTkButton):
    def __init__(self, window, text, command, **kwargs):
        super().__init__(window, text=text, command=command, width=95, **kwargs)
        window.add_widget(self)


class ButtonClear(Button):
    def __init__(self, window, command):
        super().__init__(window, text="LIMPAR", command=command,
                         fg_color="red", hover_color="#d94545")


class ButtonCopy(Button):
    def __init__(self, window, command):
        super().__init__(window, text="COPIAR", command=command,)


class RadioButton(CTkRadioButton):
    def __init__(self, window, text, variable, value, command, **kwargs):
        super().__init__(window, text=text, variable=variable,
                         value=value, command=command, **kwargs)
        window.add_widget(self)


class RadioButtonRetida(RadioButton):
    def __init__(self, window, variable, command, **kwargs):
        super().__init__(window, text="SAC N2", variable=variable, value=1, command=command, **kwargs)


class RadioButtonAssistencia(RadioButton):
    def __init__(self, window, variable, command, **kwargs):
        super().__init__(window, text="ASSISTÊNCIA",
                         variable=variable, value=2, command=command, **kwargs)


class RadioButtonCancelada(RadioButton):
    def __init__(self, window, variable, command, **kwargs):
        super().__init__(window, text="CANCELADA",
                         variable=variable, value=3, command=command, **kwargs)
