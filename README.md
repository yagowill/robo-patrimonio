# 🤖 Robô Patrimônio SispatWeb

Este projeto Python é um robô de automação web desenvolvido para interagir com o sistema SispatWeb, otimizando tarefas repetitivas como a incorporação e o recebimento de termos de patrimônio. A automação é realizada utilizando a biblioteca Playwright, e a interface gráfica é construída com PySide6 para uma experiência de usuário responsiva. Dados como órgãos e unidades de localização são gerenciados via SQLite.

## ✨ Funcionalidades

- **Login Automatizado:** Acessa o Governo Digital e navega até o SispatWeb.
- **Incorporação de Patrimônios:**
  - Permite filtrar bens por órgão de origem, número do termo e descrição.
  - Adiciona múltiplos números de RP (Registro de Patrimônio) via entrada manual, sequência (`100:105`), ou lista separada por vírgulas/quebra de linha.
  - Automatiza o processo de incorporação dos bens listados a um destino específico.
- **Recebimento de Termos:**
  - Automatiza o recebimento de termos de empréstimo/transferência/manutenção que estão "distribuídos não recebidos".
  - Configura a data de recebimento para o dia atual automaticamente.
- **Interface Gráfica (GUI):** Desenvolvida com PySide6 para facilitar a interação e exibir o log das operações em tempo real. As tarefas de automação rodam em segundo plano para manter a interface responsiva.
- **Gerenciamento de Dados:** Utiliza um banco de dados SQLite para armazenar as listas de Órgãos de Origem e Unidades de Localização.
- **Segurança:** Credenciais são armazenadas em um arquivo `.env`, não rastreado pelo controle de versão.

## 🚀 Tecnologias Utilizadas

- **Python**
- **Playwright:** Para automação web.
- **PySide6:** Para a construção da interface gráfica do usuário (GUI).
- **SQLite:** Para gerenciamento de dados persistentes.
- **python-dotenv:** Para carregamento seguro de variáveis de ambiente.

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar e executar o projeto em sua máquina:

### Pré-requisitos

Certifique-se de ter o Python instalado.

### 1. Clonar o Repositório (ou baixar o código)

```bash
git clone https://github.com/yagowill/robo-patrimonio
cd robo-patrimonio
```

(Se você baixou um ZIP, descompacte-o e navegue até a pasta raiz.)

### 2. Criar e Ativar o Ambiente Virtual

É altamente recomendado usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

### 3. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 4. Instalar os Browsers do Playwright

O Playwright precisa dos executáveis dos navegadores.

```bash
playwright install
```

### 5. Configurar as Credenciais (.env)

Crie um arquivo chamado `.env` na **raiz do projeto** (no mesmo diretório deste `README.md`). Adicione suas credenciais do SispatWeb neste arquivo:

```text
SISPAT_USUARIO=seu_usuario_aqui
SISPAT_SENHA=sua_senha_aqui
```

**Importante:** Substitua `seu_usuario_aqui` e `sua_senha_aqui` pelas suas credenciais reais. Nunca compartilhe este arquivo! Ele já está configurado para ser ignorado pelo Git.

## ▶️ Como Executar

Com todas as configurações feitas, você pode iniciar a interface gráfica do robô:

```bash
python main.py
```

A interface gráfica será aberta, permitindo que você preencha os detalhes e inicie as tarefas de automação.

## ⚠️ Observações e Solução de Problemas

- **Log de Operações:** A interface gráfica possui uma área de log que exibe o progresso e quaisquer mensagens de erro durante a automação. Para logs detalhados, um arquivo `relatório.log` também é gerado na raiz do projeto.
- **TimeoutError / Elemento Não Encontrado:** O SispatWeb é um sistema dinâmico. Se a automação travar em um `TimeoutError` (indicando que um elemento não foi encontrado), isso pode ser devido a:
- Alterações na estrutura HTML da página (seletor desatualizado).
- Atrasos na rede ou no carregamento do JavaScript.
- Problemas específicos do ambiente.
    Para depurar, altere `headless=True` para `headless=False` na função `start_browser()` em `src/sispat.py`. Isso fará o navegador ficar visível, permitindo que você observe o que está acontecendo e inspecione os elementos problemáticos com as ferramentas de desenvolvedor (F12).
- **"Target page, context or browser has been closed"**: Este erro geralmente ocorre como uma consequência de um erro anterior (como um timeout não tratado) que leva o navegador a um estado inválido ou a ser fechado prematuramente. Corrigir o erro subjacente (geralmente um seletor ou espera) resolverá isso.

## 🤝 Contribuição

Contribuições são bem-vindas! Se você encontrar um bug ou tiver uma ideia de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença [MIT License](https://opensource.org/licenses/MIT).

---
