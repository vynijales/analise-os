import datetime, subprocess

arq = open("user/user.txt", "r")
user = arq.read()
arq.close()

arq = open(f"txt.txt", "r")
txt = arq.readlines()
arq.close()

fuso_horario = datetime.timedelta(hours=-3)

today = datetime.datetime.now()
#today += fuso_horario
td = today.strftime("%d/%m/%Y - %H:%M")

for l in range(len(txt)):
	if "-----" in txt[l]:
		txt[l-1] = f"{user} - {td}\n"
		pass

arq = open(f"txt.txt", "w")

for l in range(len(txt)):
	arq.writelines(txt[l])
arq.close()

subprocess.run(['notepad.exe', 'txt.txt'])
