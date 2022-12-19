import pyperclip as pc

ctrlc = "CTRL + C automático"
pc.copy(ctrlc)

ctrlv = pc.paste()

print(ctrlv)
print(type(ctrlv))