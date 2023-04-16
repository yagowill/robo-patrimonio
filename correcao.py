import pyautogui as pg
from time import sleep

def corrigir():
    # corrigido = 0
    with open("rps_errados.txt", "r") as rps:
        for rp in rps:
            pg.moveTo(479, 250)
            pg.click()
            pg.write(rp.strip(), 0.02)
            pg.moveTo(1234, 268)
            pg.click()
            sleep(5)
            pg.moveTo(1317, 392)
            pg.click()
            pg.moveTo(481, 247)
            pg.click()
            pg.write("e", 0.02)
            pg.scroll(-10, 233, 552)
            pg.click()
            # corrigido += 1
            # log = open("robo.log", "a")
            # log.write(f"Patrimonio: \33[1;35m{rp.strip()}\33[92m OK\33[1;37m - Progresso: \33[1;96m{corrigido}/309\33[m\n")
            # log.close
            sleep(5)

sleep(5)
corrigir()