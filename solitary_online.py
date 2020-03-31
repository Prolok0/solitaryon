from socket import *
from random import randint, choice
import threading

quotes = ["A fantasia é um jeito fácil de dar sentido ao mundo. Para dar escape à nossa dura realidade.",
"Ele desapareceu e agora somos nós dois.",
"Exciting times in the world.",
"Melhor um mal conhecido do que um desconhecido.",
"Nós destruímos partes nossas todos os dias. Nós editamos nossas verrugas, modificamos as partes que as pessoas odeiam.",
"Todos vivemos nas paranoias uns dos outros.",
"Quebre os cadeados, se solte das correntes, viva a vida como ela é. Não como a sociedade te obriga.",
"O verdadeiro hacker não se autodenomina com este título, ele é denominado.",
"Se eu não escuto meu amigo imaginário, porque caralhos eu devia escutar o seu?",
"O paraíso é um conto de fadas para pessoas com medo do escuro.",
"Hackear não é algo sobre como quebrar sistemas, é algo sobre como quebrar mentes.",
"A arte desafia a tecnologia, e a tecnologia inspira a arte."]

powers = {'fire':7, 'poison':5, 'regeneration':8}

def main():
	username = "player" + str(randint(8,9898989) * randint(9,898989))
	print("\033[1;34m{}\033[m".format(choice(quotes)))
	print("\nUsername: \033[32m" + username)
	while True:
		menu = str(input("""
	\033[36mBem vindo ao  \033[33ms o l i t a r y\033[m

	\033[36m[1]\033[m Entrar em uma partida
	\033[36m[2]\033[m Hospedar uma partida
	\033[36m[3]\033[m Trocar nome de usuário
	\033[36m[4]\033[m EXIT

	>>> """))
		if not menu in "123":
			pass
		if menu == "1":
			host = str(input("\nDigite o IP: "))
			port = int(input("Digite a PORTA: "))
			join(host,port,username)

		if menu == "2":
			host = str(input("\nDigite o IP: "))
			port = int(input("Digite a PORTA: "))
			hostsrv(host,port,username)
		if menu == "3":
			username = str(input("Username> "))
			print("Username: " + username)

		if menu == "4":
			print("Goodbye, friend.")
			break

def join(host,port,username):
	s = socket(AF_INET, SOCK_STREAM)
	try:
		s.connect((host,port))
		print("\nConectado!")
		print("Você entrou na partida de: \033[32m" + s.recv(1024).decode("ISO-8859-1")+"\033[m")
		s.send(bytes(username, "ISO-8859-1"))
		battle(s)
	except Exception as erro:
		print("[!] Ocorreu um erro: {} [!]".format(erro))

def hostsrv(host,port,username):
	s = socket(AF_INET, SOCK_STREAM)
	s.bind((host,port))
	s.listen(5)
	c,e = s.accept()
	c.send(bytes(username, "ISO-8859-1"))
	print("\n\033[32m"+c.recv(1024).decode("ISO-8859-1") + "\033[m se conectou!")
	battle(c)

def battle(connection):
	pfire = False   ## P O D E R E S ##
	opfire = False
	ppoison = False
	oppoison = False
	preg = False
	opreg = False   ###################

	firecount = 0 ## C O N T A D O R E S ##
	ofc = 0
	poisoncount = 0
	opc = 0
	regcount = 0
	orc = 0       #########################

	turnos = 0

	life = 100   ## V I D A ##
	oplife = 100
	atk = 7      ## A T A Q U E ##
	opatk = 7
	mana = 1     ## M A N A ##
	opmana = 1
	countatk = 3 ## C O N T A D O R ##
	opcountatk = 3

	while True:
		comando = str(input("""
Seu HP = \033[1;31m{}\033[m / Ataque = \033[1;31m{}\033[m ({}) / Mana = {}
Oponente HP = \033[1;31m{}\033[m / Ataque = \033[1;31m{}\033[m ({})

	\033[36m[1]\033[m Ataque!
	\033[36m[2]\033[m Defesa!
	\033[36m[3]\033[m Melhorar ataque!
	\033[36m[7]\033[m Fire! (Mana = 7, acaba depois de 3 turnos) 
	\033[36m[8]\033[m Poison! (Mana = 5, acaba depois de 4 turnos)
	\033[36m[9]\033[m Regeneration! (Mana = 8, acaba depois de 3 turnos)

	>>> """.format(life,atk,countatk,mana,oplife,opatk,opcountatk)))
		print("Aguarde uma resposta do oponente!\n\n")
		connection.send(bytes(comando, "ISO-8859-1"))
		oponente = connection.recv(1024).decode("ISO-8859-1")

		if comando == "1" and not oponente == "2": #Se eu atacar e o oponente não defender
			oplife -= atk
			mana += 1
		if comando == "1" and oponente == "2": #Se eu atacar e o oponente defender
			oplife -= 1
			opmana += 1

		if oponente == "1":
			if comando == "2": #Se o oponente atacar e eu defender
				print("Você \033[1;34mdefendeu\033[m o ataque do adversário! \033[1;31m-1\033[m HP")
				life -= 1
				mana += 1
			else:
				print("O adversário te atacou! \033[1;31m-{}\033[m HP".format(opatk))
				life -= opatk
				opmana += 1

		if oponente == "2": #Se o oponente defender
			print("O adversário está em posição de \033[1;34mdefesa!\033[m")

		if comando == "3" and countatk >= 1: #Melhorar ataque
			print("Você melhorou o \033[33mataque!\033[m")
			atk += 2
			countatk -= 1
		if oponente == "3" and opcountatk >= 1: #Se o oponente melhorar o ataque
			print("O adversário melhorou o \033[33mataque!\033[m")
			opcountatk -= 1
			opatk += 2


################## F I R E ##################
		if comando == "7" and mana >= powers['fire']: #Se o player usar fogo
			opfire = True
			mana -= powers['fire']
		if opfire == True and ofc <= 3:
			ofc += 1
			oplife -= 9
			print("Inimigo \033[1;31mqueimando!\033[m")
		if ofc >= 4:
			opfire = False
			ofc = 0

		if oponente == "7" and opmana >= powers['fire']: #Se o oponente usar fogo
			print("Você está em \033[31mchamas!\033[m")
			pfire = True
			opmana -= powers['fire']

		if pfire == True and firecount <= 3:
			firecount += 1
			life -= 9
			print("Fogo: \033[1;31m-9\033[m HP")
		if firecount >= 4:
			pfire = False
			firecount = 0
##############################################
################## P O I S O N ##################
		if comando == "8" and mana >= powers['poison']: #Se o player usar veneno
			oppoison = True
			mana -= powers['poison']
		if oppoison == True and opc <= 4:
			opc += 1
			oplife -= 5
			print("Inimigo \033[1;32magonizando!\033[m")
		if opc >= 5:
			oppoison = False
			opc = 0

		if oponente == "8" and opmana >= powers['poison']: #Se o oponente usar veneno
			print("Você está em \033[32menvenenado!\033[m")
			ppoison = True
			opmana -= powers['poison']

		if ppoison == True and poisoncount <= 4:
			poisoncount += 1
			life -= 5
			print("Veneno: \033[1;31m-5\033[m HP")
		if poisoncount >= 5:
			ppoison = False
			poisoncount = 0
##############################################
################## R E G E N E R A T I O N ##################
		if comando == "9" and mana >= powers['regeneration']: #Se o player usar regeneração
			opreg = True
			mana -= powers['regeneration']
		if opreg == True and ofc <= 3:
			orc += 1
			life += 8
			print("\033[33mRegeneração: \033[1;33m+8\033[m HP")
		if orc >= 4:
			opreg = False
			orc = 0

		if oponente == "9" and opmana >= powers['regeneration']: #Se o oponente usar regeneração
			preg = True
			opmana -= powers['regeneration']
		if preg == True and regcount <= 3:
			regcount += 1
			oplife += 8
			print("Inimigo está \033[33mregenerando!\033[m")
		if regcount >= 4:
			preg = False
			regcount = 0
##############################################
		if oplife <= 0:
			print("Você \033[1;33mVENCEU!\033[m")
			break
		if life <= 0:
			print("Você \033[1;31mMORREU!\033[m")
			break
	print("f i m   d e   j o g o")

	connection.close()
main()
