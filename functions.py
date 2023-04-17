from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime as time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 


navegador = webdriver.Edge()

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

def corrigir():
    with open("E:/Users/Yago/Projetos/robo-patrimonio/robo_web/rps_errados.txt", "r") as rps:
        for rp in rps:
            codigobem = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="doacao_form_pesq:codigobem"]')))
            codigobem.send_keys(rp.strip())
            navegador.find_element(By.XPATH, '//*[@id="doacao_form_pesq:j_id436"]').click()
            editar_cadastro = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="doacao_form_lista:registros:0:j_id462"]')))
            editar_cadastro.click()
            editar_rp = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_cad:j_id411_body"]/table[2]/tbody/tr[2]/td[2]/input')))
            editar_rp.send_keys("e")
            sleep(5)
            navegador.find_element(By.CSS_SELECTOR, '#incorporar_bem_destinado_ao_orgao_form_cad\:alterar').click()
            timestamp = time.now()
            log = open("E:/Users/Yago/Projetos/robo-patrimonio/robo_web/correcoes.log", "a")
            log.write(f"\33[1;96m{timestamp}\33[1;37m - \33[1;37mPatrimonio: \33[1;35m{rp.strip()}\33[92m OK\33[m\n")
            log.close
            navegador.quit()