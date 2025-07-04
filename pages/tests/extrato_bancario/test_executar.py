from playwright.sync_api import Page, expect

from pages.extrato_bancario.automation_page import AutomationPage
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

    dados_esperados = [
        ["01/11/2024", "", "51", 32.02, "92137463482", "Pagamento com QR Pix BUSCH CONVENIENCIA", "Extrato"],
        ["02/11/2024", "", "51", 10.80, "91872709809", "Transferência Pix enviada LEONARDO SCHUTZ NETO", "Extrato"],
        ["02/11/2024", "", "51", 26.93, "92217801842", "Pagamento com QR Pix BUSCH CONVENIENCIA", "Extrato"],
        ["04/11/2024", "", "51", 89.01, "91687919980", "Pagamento com código QR Pix cancelado Igor LeÃ§a da Paz", "Extrato"],
        ["05/11/2024", "", "51", 920.00, "92123827001", "Transferência Pix enviada GRAZIELA FLONISIA SCHUTZ", "Extrato"],
        ["05/11/2024", "", "51", 400.00, "92514549550", "Transferência Pix enviada JULIANE OLIVEIRA BARRETO", "Extrato"],
        ["08/11/2024", "", "51", 624.06, "92772965048", "Pagamento de contas Confederação Nacional das Cooperativas Centrais Unicred Ltda –...", "Extrato"],
        ["09/11/2024", "", "51", 430.00, "92895212530", "Transferência Pix enviada Suze Maria Pedro", "Extrato"],
        ["10/11/2024", "", "51", 27.00, "92998918714", "Pagamento com QR Pix Kiwify Pagamentos, Tecnologia e Servicos Ltda", "Extrato"],
        ["12/11/2024", "", "51", 280.00, "92811506491", "Transferência Pix enviada BAZIL E SILVA COMERCIO E LOCACAO DE QUADRA LTDA", "Extrato"],
        ["12/11/2024", "", "51", 10.00, "93139664552", "Transferência Pix enviada I C DOS SANTOS ALMEIDA LTDA", "Extrato"],
        ["12/11/2024", "51", "", 27.00, "92998918714", "Transferência cancelada Kiwify Pagamentos, Tecnologia e Servicos Ltda", "Extrato"],
        ["12/11/2024", "", "51", 500.00, "92876429925", "Transferência Pix enviada ELANE DE OLIVEIRA PEREIRA", "Extrato"],
        ["14/11/2024", "", "51", 67.00, "93088672653", "Pagamento com QR Pix Kiwify Pagamentos, Tecnologia e Servicos Ltda", "Extrato"],
        ["17/11/2024", "", "51", 750.00, "93649460420", "Transferência Pix enviada JANSER OLIVEIRA BARRETO", "Extrato"],
        ["19/11/2024", "", "51", 170.00, "93840441288", "Transferência Pix enviada CRISTOVAM SIQUEIRA", "Extrato"],
        ["21/11/2024", "51", "", 67.00, "93088672653", "Transferência cancelada", "Extrato"],
        ["22/11/2024", "", "51", 40.00, "93807442857", "Pagamento com QR Pix NUCLEO DE INFORMACAO E COORDENACAO DO PONTO BR - NIC BR", "Extrato"]
    ]

    with page.expect_response(
            lambda response: "/api/extratos-bancarios/ler-extrato" in response.url and response.status == 200) as resp_info:
            carregar_extrato_bancario(page, "pages/tests/extrato_bancario/recursos/Extrato mercado pago.pdf")

    response = resp_info.value
    json_data = response.json()
    lancamentos = json_data["dadosTelaExtratos"]

    assert len(lancamentos) == len(dados_esperados), f"Esperava {len(dados_esperados)} lançamentos, mas vieram {len(lancamentos)}"

    for i, esperado in enumerate(dados_esperados):
        item = lancamentos[i]

        assert item["data"] == esperado[0], f"Linha {i + 1} Data: esperado '{esperado[0]}', obtido '{item['data']}'"
        if item["debito"] is not None:
            assert esperado[1] == "51", f"Linha {i + 1} deveria ter débito"
            assert esperado[2] == "", f"Linha {i + 1} não deveria ter crédito"
        elif item["credito"] is not None:
            assert esperado[1] == "", f"Linha {i + 1} não deveria ter débito"
            assert esperado[2] == "51", f"Linha {i + 1} deveria ter crédito"
        else:
            raise AssertionError(f"Linha {i + 1} não tem débito nem crédito!")
        assert item["valor"] == esperado[3], f"Linha {i + 1} Documento: esperado '{esperado[3]}', obtido '{item['documento']}'"
        assert item["documento"] == esperado[4], f"Linha {i + 1} Documento: esperado '{esperado[4]}', obtido '{item['documento']}'"
        assert item["complemento"] == esperado[5], f"Linha {i + 1} Documento: esperado '{esperado[5]}', obtido '{item['documento']}'"
        assert item["origem"] == esperado[6], f"Linha {i + 1} Origem: esperado '{esperado[6]}', obtido '{item['origem']}'"
