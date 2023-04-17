from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime as time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


navegador = webdriver.Firefox()

def acessar_governo_digital():
    navegador.maximize_window()
    navegador.get('https://www.sistemas.pa.gov.br/governodigital/public/main/index.xhtml')

def efetuar_login():
    navegador.find_element(By.ID, "form_login:login_username").send_keys('yago.martins')
    navegador.find_element(By.ID, "form_login:login_password").send_keys('7366yawi')
    navegador.find_element(By.ID, "form_login:button_login").click()

def acessar_sispat():
    navegador.get('https://www.sistemas.pa.gov.br/sispat')

def acessar_cadastro_patrimonial():    
    btn = WebDriverWait(navegador, timeout=20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[1]/div/form/div[2]/div[3]/table/tbody/tr/td[2]')))
    btn.click()
    navegador.find_element(By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[1]/div/form/div[2]/div[3]/div[6]/table/tbody/tr/td[2]').click()

def acessar_entrada_por_transferencia():
    btn = WebDriverWait(navegador, timeout=20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[1]/div/form/div[2]/div[3]/table/tbody/tr/td[2]')))
    btn.click()
    navegador.find_element(By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[1]/div/form/div[2]/div[3]/div[6]/table/tbody/tr/td[2]').click()
    navegador.find_element(By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/input').click()
    navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:descricaomaterial"]').send_keys('leitor biometrico')
    navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:j_id433"]').click()

def incorporar():
    cadastrados = 0
    with open("rps_que_faltam.txt", "r") as rps:
        for rp in rps:
            cadastrados += 1
            navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:j_id457"]').click()
            navegador.find_element(By.XPATH, 'html body div#wrap div#content table#defaultPanel tbody tr td.c3 div#cont2.ft2 form#incorporar_bem_destinado_ao_orgao_form_cad div#incorporar_bem_destinado_ao_orgao_form_cad:j_id411.rich-panel div#incorporar_bem_destinado_ao_orgao_form_cad:j_id411_body.rich-panel-body.grd_cadastro table.grd_consult_campo tbody tr td.imput_colunm_form_150 input').send_keys(rp.strip())
            navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_cad:Incorporar"]').click()
            timestamp = datetime.datetime.now()
            msg = "\33[1;96m{timestamp}\33[1;37m - Patrimonio: \33[1;35m{rp.strip()}\33[92m OK\33[1;37m - Progresso: \33[1;96m{cadastrados}/353\33[m\n"
            log = open("robo.log", "a")
            print(f"{msg}")
            log.write(f"{msg}")
            log.close
