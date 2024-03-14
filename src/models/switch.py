from customtkinter import CTkSwitch


class Switch(CTkSwitch):
    def __init__(self, window, command):
        super().__init__(window, command=command, text="LENTIDÃO", state="disable")
        window.add_widget(self)
