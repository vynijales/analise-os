from tkinter import LabelFrame

from utils.constants import TOTALCOLUNAS


class Frame(LabelFrame):
    global TOTALCOLUNAS

    def __init__(self, master, title, **kwargs):
        super().__init__(master, text=title, padx=5, pady=5, **kwargs)
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def renderWidgets(self, leftElements=TOTALCOLUNAS):
        for i, widget in enumerate(self.widgets):
            side = "left"
            if i > leftElements -1:
                side = "right"
            widget.pack(side=side, padx=5, pady=5)

            
            

