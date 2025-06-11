# Projeto Seed Playwright com Python

Este projeto é um ponto de partida para testes automatizados utilizando Python e Playwright.

## Estrutura do Projeto

```
playwright_seed_project/
├── tests/                  # Contém os arquivos de teste
│   └── test_example.py
├── pages/                  # Contém os Page Objects
│   └── example_page.py
├── utils/                  # Contém funções utilitárias
│   └── utils.py
├── venv/                   # Ambiente virtual Python
├── requirements.txt        # Dependências do projeto
└── pytest.ini              # Configurações do Pytest
```

## Configuração do Ambiente

1.  **Clone o repositório (ou descompacte o arquivo):**

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd playwright_seed_project
    ```

2.  **Crie e ative o ambiente virtual:**

    ```bash
    py -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Instale os browsers do Playwright:**

    ```bash
    playwright install
    ```

## Executando os Testes

Para executar todos os testes, certifique-se de que o ambiente virtual esteja ativado e execute o Pytest:

```bash
pytest
```

## Exemplo de Teste (`test_example.py`)

Este arquivo contém um teste básico que navega até o Google, pesquisa por "Playwright Python" e verifica se o texto está presente nos resultados.

## Page Objects (`example_page.py`)

O `example_page.py` demonstra o uso do padrão Page Object para organizar os elementos da página e as interações.

## Utilitários (`utils.py`)

O `utils.py` inclui funções utilitárias, como a função para salvar screenshots com timestamp.


