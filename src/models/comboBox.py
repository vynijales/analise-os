from customtkinter import CTkComboBox

from components.models import Model


class ComboBox(CTkComboBox):
    def __init__(self, window, values, command, **kwargs):
        super().__init__(window, width=157, values=values,
                         state="readonly", command=command, **kwargs)
        window.add_widget(self)


class ComboBoxProblema(ComboBox):
    def __init__(self, window, command, **kwargs):
        super().__init__(
            window, values=Model.data["PROBLEMAS"], command=command, **kwargs)


class ComboBoxUser(ComboBox):
    def __init__(self, window, command, **kwargs):
        super().__init__(
            window, values=Model.data["USUÁRIOS"], command=command, **kwargs)
        self.set(Model.data["USUÁRIOS"][7])


class ComboBoxOnu(ComboBox):
    def __init__(self, window, combo, command, **kwargs):
        super().__init__(window, values=list(
            Model.data["INTERNET"]["ONU"][combo].keys()), command=command, **kwargs)
        self.set(list(Model.data["INTERNET"]["ONU"][combo].keys())[0])


class ComboBoxRT(ComboBox):
    def __init__(self, window, combo, command, **kwargs):
        super().__init__(window, values=list(
            Model.data["INTERNET"]["RT"][combo].keys()), command=command, **kwargs)
        self.set(list(Model.data["INTERNET"]["RT"][combo].keys())[0])


class ComboBoxTecnologia(ComboBox):
    def __init__(self, window, command, **kwargs):
        super().__init__(window, values=list(
            Model.data["TV"].keys()), command=command, **kwargs)
        self.set(list(Model.data["TV"].keys())[0])


class ComboBoxTV2(ComboBox):
    def __init__(self, window, command, tec="COAXIAL", **kwargs):
        super().__init__(window, values=list(
            Model.data["TV"][tec].keys()), command=command, **kwargs)
        self.set(list(Model.data["TV"]["COAXIAL"].keys())[0])
