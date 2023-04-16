import pyautogui as pg
import datetime
from time import sleep

def incorporar():
	cadastrados = 2
	with open("rps.txt", "r") as rps:
		for rp in rps:
			cadastrados += 1
			pg.moveTo(1344,372)
			pg.click()
			pg.moveTo(476,246, 4)
			pg.click()
			pg.write(rp.strip(), 0.02)
			sleep(1)
			pg.scroll(-10, 235, 554)
			pg.click()
			timestamp = datetime.datetime.now()
			log = open("robo.log", "a")
			log.write(f"\33[1;96m{timestamp}\33[1;37m - Patrimonio: \33[1;35m{rp.strip()}\33[92m OK\33[1;37m - Progresso: \33[1;96m{cadastrados}/353\33[m\n")
			log.close
			sleep(5)

sleep(5)
incorporar()