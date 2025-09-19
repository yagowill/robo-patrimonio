import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Playwright, TimeoutError

class GovernoDigital:
    def __init__(self, log_callback=None):
        self._playwright_instance: Playwright = None
        self.page: Page = None
        self.log_callback = log_callback if log_callback else print

    def _log(self, message):
        """Internal logging helper."""
        self.log_callback(f"[SISPAT] {message}")

    def start_browser(self):
        """Starts Playwright browser and returns a page object."""
        self._log("Iniciando navegador...")
        self._playwright_instance = sync_playwright().start()
        browser = self._playwright_instance.chromium.launch(headless=False) # Keep headless=False for testing
        context = browser.new_context()
        self.page = context.new_page()
        self.page.set_default_timeout(60000) # 60 seconds timeout for all actions
        self._log("Navegador iniciado.")
        return self.page

    def stop_browser(self):
        """Stops the Playwright browser."""
        if self._playwright_instance:
            self._log("Fechando navegador...")
            try:
                if self.page and not self.page.is_closed():
                    self.page.close()
            except Exception as e:
                self._log(f"Erro ao fechar a página: {e}")
            self._playwright_instance.stop()
            self._playwright_instance = None
            self.page = None
            self._log("Navegador fechado.")

    def login(self):
        """Performs login to Governo Digital and SispatWeb."""
        self._log("Acessando o Governo Digital...")
        self.page.goto('https://www.sistemas.pa.gov.br/governodigital/public/main/index.xhtml')

        self._log("Lendo credenciais do .env...")
        load_dotenv() # Load variables from .env file into the environment
        
        # Access variables from the environment
        usuario = os.getenv("GOVERNO_DIGITAL_USUARIO")
        senha = os.getenv("GOVERNO_DIGITAL_SENHA")

        if not usuario or not senha:
            self._log("ERRO: Credenciais SISPAT_USUARIO ou SISPAT_SENHA não encontradas.")
            self._log("Certifique-se de que o arquivo .env está na raiz do projeto com as linhas:")
            self._log("SISPAT_USUARIO=seu_usuario_aqui")
            self._log("SISPAT_SENHA=sua_senha_aqui")
            raise ValueError("Credenciais SISPAT_USUARIO ou SISPAT_SENHA não definidas no ambiente.")

        self._log("Efetuando o login...")
        try:
            self.page.fill('input[id="form_login:login_username"]', usuario)
            self.page.fill('input[id="form_login:login_password"]', senha)
            self.page.click('a[id="form_login:button_login"]') 
            sispat_link_selector_gov_digital = 'a[href="/sispat"][title="SispatWeb"]'
            self.page.wait_for_selector(sispat_link_selector_gov_digital) 
            self._log("Login no Governo Digital efetuado com sucesso!")
        except TimeoutError:
            self._log("Erro de Timeout ao clicar no botão de login ou ao aguardar o link 'SispatWeb' na página inicial do Governo Digital.")
            self._log("Possíveis causas: ")
            self._log("  - O seletor do botão de login está incorreto.")
            self._log("  - Credenciais de login inválidas.")
            self._log("  - O link 'SispatWeb' não apareceu na página principal do Governo Digital após o login.")
            self._log("  - Problemas de rede ou carregamento lento.")
            raise 

        self._log("Acessando o SispatWeb...")
        self.page.goto('https://www.sistemas.pa.gov.br/sispat')
        
        try:
            self.page.wait_for_selector('text="Entrada por Transferência Não Incorporado"', timeout=30000) 
            self._log("Página principal do SispatWeb acessada com sucesso!")
        except TimeoutError:
            self._log("Erro de Timeout ao aguardar o elemento na página principal do SispatWeb.")
            self._log("Isso pode indicar que a navegação para o SispatWeb não foi concluída com sucesso ou que o seletor para o elemento de verificação ('Entrada por Transferência Não Incorporado') está incorreto para esta página.")
            self._log("Verifique a URL final e o conteúdo da página para um seletor mais adequado.")
            raise 

    def navigate_to_nao_incorporado(self):
        """Navigates to the 'Entrada por Transferência Não Incorporado' page."""
        self._log("Acessando entrada por transferência não incorporados...")
        self.page.click('text="Entrada por Transferência Não Incorporado"')
        self._log("Página de não incorporados acessada.")

    def navigate_to_dist_nao_recebido(self):
        """Navigates to the 'Distribuídos Não Recebidos' page and performs an initial search."""
        self._log("Acessando distribuídos não recebidos...")
        
        self.page.goto("https://www.sistemas.pa.gov.br/sispat/movimentacao_bem/recebimento/recebimento_termo_bem_interno_operacional_lista.seam")
        
        try:
            self.page.wait_for_selector('text="Receber Termo de Empréstimo e Transferência Interna"', timeout=30000)
            self._log("Página 'Receber Termo de Movimentação' acessada com sucesso.")
        except TimeoutError:
            self._log("Erro de Timeout ao aguardar o texto de cabeçalho na página de 'Distribuídos Não Recebidos'.")
            self._log("Verifique se o texto 'Receber Termo de Empréstimo e Transferência Interna' está presente na página.")
            raise 

        pesquisar_button_selector = 'input[type="submit"][value="Pesquisar"]'
        
        try:
            self.page.click(pesquisar_button_selector)
            self.page.wait_for_load_state('networkidle') 
            self._log("Pesquisa inicial na página de distribuídos não recebidos realizada.")
        except TimeoutError:
            self._log(f"Timeout ao tentar clicar no botão Pesquisar ({pesquisar_button_selector}) na página de distribuídos não recebidos.")
            self._log("Verifique se o botão 'Pesquisar' existe com este seletor ou se a página carregou corretamente após a navegação.")
            raise 
