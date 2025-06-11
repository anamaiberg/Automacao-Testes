from threading import Thread

from playwright.sync_api import Page

class ExtratoBancarioPage:
    def __init__(self, page: Page):
        self.page = page

    def selecionar_empresa(self, selector_empresa: str, empresa_cnpj: str):
        input_empresa = self.page.locator(selector_empresa)
        input_empresa.click(delay= 500)
        input_empresa.press_sequentially(empresa_cnpj, delay=500)
        input_empresa.press("Enter", timeout= 3000)

    def selecionar_conta(self, conta_analitica):
        input_upload = self.page.locator("#extrato-conta-selecionar > div.dx-dropdowneditor-input-wrapper > div > div.dx-texteditor-input-container > input")
        input_upload.click(delay= 500)
        input_upload.press_sequentially(conta_analitica, delay=500)
        input_upload.press("Enter", timeout= 3000)

    def selecionar_extrato(self, caminho_extrato: str):
        file_input = self.page.locator("#extrato-selecionar-extrato")
        file_input.set_input_files(caminho_extrato)

    def executar(self):
        self.page.locator("#btnExecutar").click(delay= 500)

    def esperar_lancamento(self):
        tentativa = 0
        while (tentativa < 10):
            if self.page.is_visible("#extrato-grid-lancamentos > div > div.dx-datagrid-rowsview.dx-datagrid-nowrap.dx-scrollable.dx-visibility-change-handler.dx-scrollable-both.dx-scrollable-simulated.dx-last-row-border > div > div > div.dx-scrollable-content > div > table > tbody > tr:nth-child(1)", timeout=2000):
                break

            if self.page.is_visible("span[text='Nenhuma informação encontrada']"):
                raise Exception("Layout inválido, verifique se o extrato é correto")

            tentativa = tentativa + 1
            self.page.wait_for_timeout(1000)

