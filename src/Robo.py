from datetime import datetime as time
from time import sleep
import PySimpleGUI as sg
import json
import re
from selenium.webdriver.common.by import By
# from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Robo:
    def __init__(self, headless, tipo, cli):
        self.service = Service(ChromeDriverManager().install())
        #self.service.creationflags = CREATE_NO_WINDOW
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
            
        
    def acessar_entrada_por_transferencia_nao_incorporado(self):
        entrada_por_transferencia_nao_incorporado = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[3]/div/table/tbody/tr/td[1]/a')
        
        self.mensagem("Acessando entrada por tranferência não incorporados...")
        
        entrada_por_transferencia_nao_incorporado.click()
        
    def incorporar_pistolas(self):
        origem = 'FISP - FUNDO DE INVESTIMENTO EM SEGURANÇA PÚBLICA'
        ntermo = '2023/30'
        descricao = 'PISTOLA SEMIAUTOMATICA, OXIDADA, CALIBRE 9MM, P/ 15 TIROS'
        destino = 'UNIDADE DE PATRIMONIO'
        cadastrados = 0  
        total = 612
        
        self.acessar_entrada_por_transferencia_nao_incorporado()
        
        self.mensagem("pesquisando...")
        self.filtrar(origem, ntermo, descricao)

        sleep(5)
        cout = total
        while cout > 0:
            incorporar_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[3]/td[8]/a')
            
            self.navegador.execute_script("arguments[0].click();", incorporar_btn)
            
            sleep(1)
            
            rp = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[8]/tbody/tr[4]/td[2]/span').text + '-'
                       
            input_rp = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')
            input_rp.send_keys(rp)
            
            btn_pesquisa = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/fieldset/table/tbody/tr/td[2]/table/tbody/tr/td[2]/input')
            
            self.navegador.execute_script("arguments[0].click();", btn_pesquisa)
            
            sleep(.5)
            
            input_pesquisa = self.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/input')
            
            input_pesquisa.send_keys(destino)
            
            btn_pesquisar = self.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[2]/table/tbody/tr/td/input')
            
            self.navegador.execute_script("arguments[0].click();", btn_pesquisar)
            
            sleep(.5)
            
            btn_destino = self.espera_elemento('/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/span/table/tbody/tr/td[3]/a')
            
            self.navegador.execute_script("arguments[0].click();", btn_destino)
            
            sleep(0.5)
            
            confirmar_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[1]')
            
            self.navegador.execute_script("arguments[0].click();", confirmar_btn)
            
            sleep(1)
            
            confirmacao = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
            log = open('atividade.log', 'a')
            
            try:
                assert confirmacao.text == "Bem foi incorporado ao órgão com sucesso."
                timestamp = time.now().strftime("%d/%m/%Y %H:%M:%S")
                cadastrados += 1
                self.mensagem(f'{timestamp} - Descrição: {descricao} Patrimonio: {rp} Incorporado {cadastrados}/{total}')
                log.write(f'{timestamp} - Descrição: {descricao} Patrimonio: {rp} Incorporado {cadastrados}/{total}\n')
                log.close()
                cout -= 1
            except:
                aviso = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div/table/tbody/tr/td/span[2]')
                
                self.mensagem(aviso.text, text_color='red')
                log.write(aviso.text)
                self.navegador.close()
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
        
        pesquisar = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[1]/div/div/div/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr/td/input[1]')
        
        self.navegador.execute_script("arguments[0].click();", pesquisar)
            
    
    def incorporar(self, origem, ntermo, descricao, patrimonios, destino):
        rps = patrimonios
        cadastrados = 0  
        total = len(rps)
                    
        self.acessar_entrada_por_transferencia_nao_incorporado()
        
        self.mensagem("pesquisando...")
        self.filtrar(origem, ntermo, descricao)
        sleep(1)
        log = open('relatório.log', 'a')
        for rp in rps:
            selecionar_ben_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form[2]/span/table/tbody/tr[1]/td[8]/a/img')
            selecionar_ben_btn.click()   
            
            input_rp = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/table[2]/tbody/tr[2]/td[2]/input')
            input_rp.send_keys(rp)
            
            btn_pesquisa = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/div/div/fieldset/table/tbody/tr/td[2]/table/tbody/tr/td[2]/input')
            btn_pesquisa.click()
            
            input_pesquisa = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/input'
            
            input_pesquisa.send_keys(destino)
            
            btn_pesquisar = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/table[2]/tbody/tr/td[2]/table/tbody/tr/td/input'
            
            self.navegador.execute_script("arguments[0].click();", btn_pesquisar)
            
            sleep(1)
            
            btn_destino = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/form/span/table/tbody/tr/td[3]/a'
            
            self.navegador.execute_script("arguments[0].click();", btn_destino)
            
            sleep(1)
            
            confirmar_btn = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/form/table/tbody/tr/td/input[1]')
            
            self.navegador.execute_script("arguments[0].click();", confirmar_btn)
            
            sleep(1)
            
            
            confirmacao = self.espera_elemento('/html/body/div/div[1]/table/tbody/tr/td[3]/div/div[1]/table/tbody/tr/td/span[2]')
            
            if confirmacao.text == "Bem foi incorporado ao órgão com sucesso.":
                btn_imprimir_depois = '/html/body/div[2]/div[2]/div/div[2]/table/tbody/tr[2]/td/div/div[2]/input[2]'
                self.navegador.execute_script("arguments[0].click();", btn_imprimir_depois) 
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
    sispat.acessar_sispatweb()
    sispat.incorporar_pistolas()
    