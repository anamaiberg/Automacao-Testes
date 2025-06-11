from playwright.sync_api import Page, expect

from pages.automation_page import AutomationPage
from pages.extrato_bancario.extrato_bancario_page import ExtratoBancarioPage


def carregar_extrato_bancario(page: Page, extrato: str):
    automation_page = AutomationPage(page)
    automation_page.login()
    automation_page.acessar("contabil/extrato-bancario", "h2:has-text('Extrato bancário')")
    expect(page).to_have_url("https://staging.automationweb.com.br/contabil/extrato-bancario")

    extrato_bancario_page = ExtratoBancarioPage(page)
    extrato_bancario_page.selecionar_empresa("#extrato-empresa > div > div > div.dx-texteditor-input-container > input", "33.278.206/0001-37")
    extrato_bancario_page.selecionar_conta("51")
    extrato_bancario_page.selecionar_extrato(extrato)
    extrato_bancario_page.executar()
    extrato_bancario_page.esperar_lancamento()

def test_access_extrato_bancario(page: Page):
    carregar_extrato_bancario(page, "E:\\workspace\\automation_teste\\tests\\extrato_bancario\\recursos\\Extrato mercado pago.pdf")
    #Regra de lançamento
    linhas = page.locator("//*[@id='extrato-grid-lancamentos']/div/div[6]/div/div/div[1]/div/table/tbody/tr")
    expect(linhas).to_have_count(18)
    expect(linhas.nth(0)).to_have_text("01/11/202451R$ 32,0292137463482Pagamento com QR Pix BUSCH CONVENIENCIAExtrato")
    # for linhaIndex in range(linhas.count()):
    #    colunas = linhas.nth(linhaIndex)

