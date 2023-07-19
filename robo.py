import json
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from datetime import datetime as time
from time import sleep
import re
import PySimpleGUI as sg

class Sistema:
    def __init__(self, headless):
        self.service = Service(executable_path="./chromedriver.exe")
        self.service.creation_flags = CREATE_NO_WINDOW
        if headless:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.navegador = webdriver.Chrome(service=self.service, options=options)
        else:
            self.navegador = webdriver.Chrome(service=self.service)
    
    def login(self,tipo):
        with open("login.json") as file:
            login = json.load(file)
        self.usuario = login[tipo]["usuario"]
        self.senha = login[tipo]["senha"]
        if(self.usuario == '' or self.senha == '' ):
            print('Usuário e senha não definidos')
        else:
            #sg.Print("Acessando o Governo Digital...")
            self.navegador.get('https://www.sistemas.pa.gov.br/governodigital/public/main/index.xhtml')
            #sg.Print("Efetuando o login...")
            self.navegador.find_element(By.ID, "form_login:login_username").send_keys(self.usuario)
            self.navegador.find_element(By.ID, "form_login:login_password").send_keys(self.senha)
            self.navegador.find_element(By.ID, "form_login:button_login").click()
            WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form_sistema:submit_area"]/div/div[3]/div[1]/a/img')))
            #sg.Print("Login efetuado com sucesso!", text_color='green')
            self.navegador.get('https://www.sistemas.pa.gov.br/sispat')
            #sg.Print("Acessando o SispatWeb...")
        
    def acessar_dist_nao_recebido(self):
        dist_nao_recebido = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="form_pendencias:list:1:pendencia_17"]')))
        sg.Print('Acessando distribuídos não recebidos...')
        dist_nao_recebido.click()
    
    def receber(self):
        self.acessar_dist_nao_recebido()                
        transferencia_nao_recebida_btn = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[7]')))
        while transferencia_nao_recebida_btn:
            transferencia_nao_recebida_btn.click()
            calendario_btn = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/span/img')))
            calendario_btn.click()
            data_btn = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div')))
            data_btn.click()
            receber = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/input[1]')))
            receber.click()
            confirmacao = WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
            assert re.search("recebido com sucesso.",confirmacao.text) != None
            timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
            sg.Print(f'{timestamp} {confirmacao.text}')
        self.navegador.quit()
            
        
    def acessar_entrada_por_transferência_nao_incorporado(self):
        entrada_por_transferência_nao_incorporado = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[3]/div/table/tbody/tr/td[1]/a')))
        
        #sg.Print("Acessando entrada por tranferência não incorporados...")
        
        entrada_por_transferência_nao_incorporado.click()
        

        
    def incorporar(self, origem, ntermo, descricao, patrimonios):
        rps = patrimonios
        cadastrados = 0  
        total = len(rps)
            
        
        self.acessar_entrada_por_transferência_nao_incorporado()
        
        orgao_origem_selection = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[1]/fieldset/table[1]/tbody/tr/td[2]/select')))
        orgao_origem_selection.click()
        
        origem_option =  WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, f'//option[contains(text(),"{origem}")]')))
        origem_option.click()
        
        n_termo = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[1]/fieldset/table[2]/tbody/tr[1]/td[2]/input')))
        n_termo.send_keys(ntermo)
        
        descricao_input = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:descricaomaterial"]')))
        descricao_input.send_keys(descricao)
        
        pesquisar = self.navegador.find_element(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:j_id433"]')
        pesquisar.click()
        
        #sg.Print("pesquisando...")
        
        sleep(5)
        
        resultado = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]')))
        
        total = 1000
        
        while resultado:
            incorporar_btn = WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')))
            incorporar_btn.click()
            
            rp = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[8]/tbody/tr[4]/td[2]/span'))).text + '*'
                       
            input_rp = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')))
            input_rp.send_keys(rp)
            
            ActionChains(self.navegador).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
            
            confirmacao = WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
            log = open('atividade.log', 'a')
            
            try:
                assert confirmacao.text == "Bem foi incorporado ao órgão com sucesso."
                timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
                cadastrados += 1
                sg.Print(f'{timestamp} - Descrição: {descricao} Patrimonio: {rp} Incorporado {cadastrados}/{total}')
                log.write(f'{timestamp} - Descrição: {descricao} Patrimonio: {rp} Incorporado {cadastrados}/{total}\n')
                log.close()
            except:
                aviso = WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/span[2]')))
                
                sg.Print(aviso.text, text_color='red')
                log.write(aviso.text)
                self.navegador.close()
                self.navegador.quit()
            
        
        # for rp in rps:
        #     incorporar_btn = WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')))
        #     incorporar_btn.click()
            
        #     input_rp = WebDriverWait(self.navegador, timeout=30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')))
        #     input_rp.send_keys(rp)
            
        #     ActionChains(self.navegador).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
            
        #     confirmacao = WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')))
            
        #     try:
        #         assert confirmacao.text == "Bem foi incorporado ao órgão com sucesso."
        #         timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
        #         cadastrados += 1
        #         sg.Print(f'{timestamp} - Patrimonio: {rp} Incorporado {cadastrados}/{total}')
        #     except:
        #         aviso = WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/span[2]')))
        #         sg.Print(aviso.text, text_color='red')
        #         self.navegador.quit()
                
        self.navegador.close()
        self.navegador.quit()

if __name__ == '__main__':
    sispat = Sistema(headless=False)
    sispat.login(tipo='operacional')
    sispat.incorporar('FISP - FUNDO DE INVESTIMENTO EM SEGURANÇA PÚBLICA', '2023/30', 'PISTOLA SEMIAUTOMATICA, OXIDADA, CALIBRE 9MM, P/ 15 TIROS', [])