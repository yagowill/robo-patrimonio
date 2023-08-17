from datetime import datetime as time
from time import sleep
import PySimpleGUI as sg
import json
import re
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Robo:
    def __init__(self, headless, tipo, cli):
        self.service = Service(executable_path="./chromedriver.exe")
        self.service.creation_flags = CREATE_NO_WINDOW
        with open("src/login.json") as file:
            login = json.load(file)
        self.usuario = login[tipo]["usuario"]
        self.senha = login[tipo]["senha"]
        self.cli = cli
        if headless:
            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            self.navegador = webdriver.Chrome(service=self.service, options=options)
        else:
            self.navegador = webdriver.Chrome(service=self.service)
            
    def espera_elemento(self, xpath):
        return WebDriverWait(self.navegador, timeout=60).until(EC.presence_of_element_located((By.XPATH, xpath)))
        
    def mensagem(self, msg, text_color=None):
        if self.cli:
            print(msg)
        else:
            sg.Print(msg, text_color=text_color)
            
    def login(self):
        self.mensagem("Acessando o Governo Digital...")
        self.navegador.get('https://www.sistemas.pa.gov.br/governodigital/public/main/index.xhtml')
        self.mensagem("Efetuando o login...")
        self.espera_elemento('//*[@id="form_login:login_username"]').send_keys(self.usuario)
        self.espera_elemento('//*[@id="form_login:login_password"]').send_keys(self.senha)
        self.espera_elemento('//*[@id="form_login:button_login"]').click()
        self.mensagem("Login efetuado com sucesso!", 'green')
        
    def acessar_sispatweb(self):
        self.espera_elemento('//*[@id="form_sistema:submit_area"]/div/div[3]/div[1]/a/img')
        self.navegador.get('https://www.sistemas.pa.gov.br/sispat')
        self.mensagem("Acessando o SispatWeb...")
        
    def acessar_dist_nao_recebido(self):
        dist_nao_recebido = self.espera_elemento('//*[@id="form_pendencias:list:1:pendencia_17"]')
        
        self.mensagem('Acessando distribuídos não recebidos...')
       
        dist_nao_recebido.click()
    
    def receber(self):
        self.acessar_dist_nao_recebido()
                        
        transferencia_nao_recebida_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[7]')
        
        while transferencia_nao_recebida_btn:
            transferencia_nao_recebida_btn.click()
            calendario_btn = self.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/span/img')
            calendario_btn.click()
            data_btn = self.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/fieldset/div/table/tbody/tr[4]/td[2]/table/tbody/tr[9]/td/table/tbody/tr/td[5]/div')
            data_btn.click()
            receber = self.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/div/input[1]')
            receber.click()
            confirmacao = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
            assert re.search("recebido com sucesso.",confirmacao.text) != None
            timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
            self.mensagem(f'{timestamp} {confirmacao.text}')
        self.navegador.quit()
            
        
    def acessar_entrada_por_transferência_nao_incorporado(self):
        entrada_por_transferência_nao_incorporado = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[3]/div/table/tbody/tr/td[1]/a')
        
        self.mensagem("Acessando entrada por tranferência não incorporados...")
        
        entrada_por_transferência_nao_incorporado.click()
        
    def incorporar_pistolas(self):
        origem = 'FISP - FUNDO DE INVESTIMENTO EM SEGURANÇA PÚBLICA'
        ntermo = '2023/30'
        descricao = 'PISTOLA SEMIAUTOMATICA, OXIDADA, CALIBRE 9MM, P/ 15 TIROS'
        cadastrados = 0  
        total = 998
        
        self.acessar_entrada_por_transferência_nao_incorporado()
        
        self.mensagem("pesquisando...")
        self.filtrar(origem, ntermo, descricao)
        
        sleep(5)
        
        resultado = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]')
        
        
        while resultado:
            incorporar_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')
            incorporar_btn.click()
            
            rp = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[8]/tbody/tr[4]/td[2]/span').text + '-'
                       
            input_rp = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')
            input_rp.send_keys(rp)
            
            ActionChains(self.navegador).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
            
            confirmacao = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
            log = open('atividade.log', 'a')
            
            try:
                assert confirmacao.text == "Bem foi incorporado ao órgão com sucesso."
                timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
                cadastrados += 1
                self.mensagem(f'{timestamp} - Descrição: {descricao} Patrimonio: {rp} Incorporado {cadastrados}/{total}')
                log.write(f'{timestamp} - Descrição: {descricao} Patrimonio: {rp} Incorporado {cadastrados}/{total}\n')
                log.close()
            except:
                aviso = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/span[2]')
                
                self.mensagem(aviso.text, text_color='red')
                log.write(aviso.text)
                self.navegador.close()
                self.navegador.quit()
                
        self.navegador.close()
        self.navegador.quit()
        
    def pegar_dados_pistola(self):
        origem = 'FISP - FUNDO DE INVESTIMENTO EM SEGURANÇA PÚBLICA'
        ntermo = '2023/30'
        total = 997
            
        self.acessar_entrada_por_transferência_nao_incorporado()
        
        orgao_origem_selection = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[1]/fieldset/table[1]/tbody/tr/td[2]/select')
        orgao_origem_selection.click()
        
        origem_option =  self.espera_elemento(f'//option[contains(text(),"{origem}")]')
        origem_option.click()
        
        n_termo = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[1]/fieldset/table[2]/tbody/tr[1]/td[2]/input')
        n_termo.send_keys(ntermo)
        
        pesquisar = self.espera_elemento('//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:j_id433"]')
        pesquisar.click()
        
        sleep(5)
        numero_serie_pistola = open('numeros de serie pistolas.csv', 'a')
        for j in range(1,101):
            lista_resultado = self.navegador.find_elements(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_lista:patrimonios:tb"]/tr')
            tamanho_lista = len(lista_resultado)
            for i in range(1, (tamanho_lista+1)):
                lupa = self.espera_elemento(f'/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[{i}]/td[7]/a')
                self.navegador.execute_script("arguments[0].click();", lupa)
                nserie = self.espera_elemento('//*[@id="j_id465_body"]/table[6]/tbody/tr[4]/td[2]/span')
                sleep(1)
                nserie = self.espera_elemento('//*[@id="j_id465_body"]/table[6]/tbody/tr[4]/td[2]/span')
                print(nserie.text)
                numero_serie_pistola.write(nserie.text + '\n')
                fechar_modal = self.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/div/img')
                self.navegador.execute_script("arguments[0].click();", fechar_modal)
                sleep(0.5)
            
                
            avançar =  self.espera_elemento('//*[@id="incorporar_bem_destinado_ao_orgao_form_lista:paginador_table"]/tbody/tr/td[15]')
            self.navegador.execute_script("arguments[0].click();", avançar)
            
        numero_serie_pistola.close()
        self.navegador.quit()
        
        
    def filtrar(self, origem, ntermo, descricao):
        orgao_origem_selection = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[1]/fieldset/table[1]/tbody/tr/td[2]/select')
        orgao_origem_selection.click()
        
        origem_option =  self.espera_elemento(f'//option[contains(text(),"{origem}")]')
        origem_option.click()
        
        n_termo = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[1]/fieldset/table[2]/tbody/tr[1]/td[2]/input')
        n_termo.send_keys(ntermo)
        
        descricao_input = self.espera_elemento('//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:descricaomaterial"]')
        descricao_input.send_keys(descricao)
        
        pesquisar = self.espera_elemento(By.XPATH, '//*[@id="incorporar_bem_destinado_ao_orgao_form_pesq:j_id433"]')
        pesquisar.click()
            
    
    def incorporar(self, origem, ntermo, descricao, patrimonios):
        rps = patrimonios
        cadastrados = 0  
        total = len(rps)
                    
        self.acessar_entrada_por_transferência_nao_incorporado()
        
        self.mensagem("pesquisando...")
        self.filtrar(origem, ntermo, descricao)
        sleep(1)
        log = open('relatório.log', 'a')
        for rp in rps:
            selecionar_ben_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')
            selecionar_ben_btn.click()   
            
            input_rp = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')
            input_rp.send_keys(rp)
            
            confirmar_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[1]')
            self.navegador.execute_script("arguments[0].click();", confirmar_btn)
            sleep(1)
            
            confirmacao = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
            
            if confirmacao.text == "Bem foi incorporado ao órgão com sucesso.": 
                timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
                cadastrados += 1
                msg = f'{timestamp} - Patrimônio: {rp} Descrição: {descricao} Incorporado {cadastrados}/{total}\n'
                self.mensagem(msg, 'green')
                log.write(msg)
            else:
                aviso = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/span[2]')
                self.mensagem(aviso.text, text_color='red')
                log.write(aviso.text + '\n')
                cancelar_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[2]')
                self.navegador.execute_script("arguments[0].click();", cancelar_btn)
                
                self.filtrar(origem, ntermo, descricao)
                
        log.close()        
        self.navegador.close()
        self.navegador.quit()
        self.mensagem("Finalizado", text_color='green')

if __name__ == '__main__':
    sispat = Robo(headless=False, tipo='operacional', cli=True)
    sispat.login()
    