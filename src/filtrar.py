from playwright.sync_api import Page, TimeoutError

# O prefixo comum para os 'name'/'id' dos campos dentro do formulário de pesquisa.
FORM_PREFIX = 'incorporar_bem_destinado_ao_orgao_form_pesq'

locators = {
    # Seletor exato para o select do Órgão de Origem.
    "org_origem_select": f'select[name="{FORM_PREFIX}:j_id425"]',
    
    # Seletor exato para o campo "Nº do Termo de Transferência".
    "n_termo_input": f'input[name="{FORM_PREFIX}:descricaobem"]', 
    
    # Seletor exato para o campo "Descrição do Bem".
    "descricao_input": f'input[name="{FORM_PREFIX}:descricaomaterial"]', 
    
    # Seletor exato para o botão "Pesquisar", usando o atributo 'name' e 'value'.
    # Este seletor é agora robusto.
    "pesquisar_button": f'input[name="{FORM_PREFIX}:j_id438"][value="Pesquisar"]'
}

def filtrar(page: Page, origem: str, ntermo: str, descricao: str, log_callback=None):
    _log = log_callback if log_callback else print
    _log(f"Preenchendo filtros: Origem='{origem}', Nº Termo='{ntermo}', Descrição='{descricao}'")

    try:
        # Esperamos que o seletor do dropdown esteja visível.
        page.wait_for_selector(locators["org_origem_select"]) 
        _log("Elemento 'Órgão Origem' visível e pronto para interação.")

        # Selecionar o texto visível no dropdown
        page.select_option(locators["org_origem_select"], label=origem)
        _log(f"Origem '{origem}' selecionada.")

        # Preencher o número do termo
        page.fill(locators["n_termo_input"], ntermo)
        _log(f"Nº Termo '{ntermo}' preenchido.")

        # Preencher a descrição
        page.fill(locators["descricao_input"], descricao)
        _log(f"Descrição '{descricao}' preenchida.")

        # Clicar no botão de pesquisa
        page.click(locators["pesquisar_button"])
        
        # Esperar que o estado da rede fique "ocioso" após a pesquisa,
        # indicando que os resultados carregaram.
        page.wait_for_load_state('networkidle') 
        _log("Botão 'Pesquisar' clicado e resultados carregados.")

    except TimeoutError as e:
        _log(f"Erro de Timeout ao filtrar: {e}")
        _log("Não foi possível encontrar ou interagir com um dos elementos do formulário de filtro (Órgão Origem, Nº Termo, Descrição ou botão Pesquisar) dentro do tempo limite.")
        _log("Por favor, verifique se os seletores CSS em `src/filtrar.py` estão corretos para a página atual do SispatWeb.")
        _log("Mantenha 'headless=False' em `src/sispat.py` para observar a página no momento do erro.")
        raise
    except Exception as e:
        _log(f"Erro inesperado ao filtrar: {e}")
        raise