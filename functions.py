from time import sleep
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime as time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By

navegador = webdriver.Chrome()

def acessar_governo_digital():
    navegador.minimize_window()
    login = input("login: ")
    senha = input("senha: ")
    navegador.get('https://www.sistemas.pa.gov.br/governodigital/public/main/index.xhtml')
    efetuar_login(login,senha)

def efetuar_login(login,senha):
    navegador.find_element(By.ID, "form_login:login_username").send_keys(login)
    navegador.find_element(By.ID, "form_login:login_password").send_keys(senha)
    navegador.find_element(By.ID, "form_login:button_login").click()

def acessar_sispat():
    acessar_governo_digital()
    navegador.get('https://www.sistemas.pa.gov.br/sispat')

def acessar_entrada_por_transferência_nao_incorporado():
    entrada_por_transferência_nao_incorporado = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[3]/div/table/tbody/tr/td[1]/a')))
    entrada_por_transferência_nao_incorporado.click()
    sleep(10)
    

def acessar_entrada_por_transferencia():
    btn_novo = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td/input')))
    btn_novo.click()
    descbem = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:descricaomaterial"]')))
    descbem.send_keys('leitor biometrico')
    pesquisar = navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:j_id433"]')
    pesquisar.click()
    
def incorporar():
    cadastrados = 0
    with open("rps.txt", "r") as rps:
        for rp in rps:
            cadastrados += 1
<<<<<<< HEAD
            navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:j_id457"]').click()
            navegador.find_element(By.XPATH, 'html body div#wrap div#content table#defaultPanel tbody tr td.c3 div#cont2.ft2 form#incorporar_bem_destinado_ao_orgao_form_cad div#incorporar_bem_destinado_ao_orgao_form_cad:j_id411.rich-panel div#incorporar_bem_destinado_ao_orgao_form_cad:j_id411_body.rich-panel-body.grd_cadastro table.grd_consult_campo tbody tr td.imput_colunm_form_150 input').send_keys(rp.strip())
            navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_cad:Incorporar"]').click()
            timestamp = time.datetime.now()
            msg = "\33[1;96m{timestamp}\33[1;37m - Patrimonio: \33[1;35m{rp.strip()}\33[92m OK\33[1;37m - Progresso: \33[1;96m{cadastrados}/353\33[m\n"
            msg_log = "{timestamp} - Patrimonio: {rp.strip()} OK - Progresso: {cadastrados}/353\n"
            log = open("robo.log", "a")
            print(f"{msg}")
            log.write(msg_log)
=======
            rp_ = rp.removeprefix('\ufeff').removesuffix('\n')
            cadastrar = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:incorporarbens"]')))
            pyautogui.click(x=1344, y=321, duration=0.25)
            input_rp = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')))
            input_rp.send_keys(rp_)
            pyautogui.scroll(-100)
            pyautogui.click(x=235, y=624, duration=0.25)
            confirma = WebDriverWait(navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
            assert confirma.text == "Bem foi incorporado ao órgão com sucesso."
            timestamp = time.now()
            log = open("robo.log", "a")
            print(f"\33[1;96m{timestamp}\33[1;37m - Patrimonio: \33[1;35m{rp_}\33[92m OK\33[1;37m - Progresso: \33[1;96m{cadastrados}/164\33[m\n")
            log.write(f"{timestamp} - Patrimonio: {rp_} OK - Progresso: {cadastrados}/164\n")
>>>>>>> 4328fd15df2d66bc589c7ea1a9d8455143f5d6fe
            log.close

