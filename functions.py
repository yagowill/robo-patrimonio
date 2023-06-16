from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime as time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.by import By

service = Service(executable_path="C:/Users/yago.martins/Projetos/robo-patrimonio/chromedriver.exe")
navegador = webdriver.Chrome(service=service)

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
    
def acessar_dist_nao_recebido():
    btn = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form_pendencias:list:1:pendencia_17"]')))
    btn.click()
    
def receber():    
    while True:
        data_btn = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[7]')))
        data_btn.click()
        data_btn2 = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/span/img')))
        data_btn2.click()
        data_btn3 = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/table/tbody/tr[4]/td[4]')))
        data_btn3.click()
        receber = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/input[1]')))
        receber.click()
        sleep(2.5)

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
            rp_ = rp.removeprefix('\ufeff').removesuffix('\n')
            cadastrar = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:0:incorporarbens"]')))
            input_rp = WebDriverWait(navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')))
            input_rp.send_keys(rp_)
            confirma = WebDriverWait(navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
            assert confirma.text == "Bem foi incorporado ao órgão com sucesso."
            timestamp = time.now()
            log = open("robo.log", "a")
            print(f"\33[1;96m{timestamp}\33[1;37m - Patrimonio: \33[1;35m{rp_}\33[92m OK\33[1;37m - Progresso: \33[1;96m{cadastrados}/164\33[m\n")
            msg_log = "{timestamp} - Patrimonio: {rp.strip()} OK - Progresso: {cadastrados}/353\n"
            log.write(msg_log)
            log.close

