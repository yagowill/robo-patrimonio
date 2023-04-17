import pyautogui as pg
from time import sleep

def corrigir():
    with open("rps_errados.txt", "r") as rps:
        for rp in rps:
            pg.moveTo(491, 116)
            pg.click()
            pg.write(rp.strip(), 0.02)
            pg.moveTo(1234, 132)
            pg.click()
            sleep(4)
            pg.moveTo(1317, 256)
            pg.click()
            sleep(25)
            pg.moveTo(497, 124)
            pg.click()
            pg.write("e", 1)
            pg.press('esc')
            sleep(0.5)
            pg.press('pgdn')
            sleep(0.5)
            pg.moveTo(237, 660)
            pg.click()
            log = open("robo.log", "a")
            log.write(f"\n\33[1;37mPatrimonio: \33[1;35m{rp.strip()}\33[92m OK\33[m")
            log.close
            sleep(5)

sleep(5)
corrigir()