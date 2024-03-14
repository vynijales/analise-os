import customtkinter

from utils.base import open_json, resource_path
from utils.constants import TOTALCOLUNAS


class Model:
    data = open_json(resource_path('data/db.json'))


class Payload(customtkinter.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=300, wrap="word",
                         font=customtkinter.CTkFont(size=14))