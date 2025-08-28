import os
import json
import time
import glob
import pytest
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

# Parâmetro: cada PDF vira 1 teste!
base = os.path.dirname(__file__)
recursos = os.path.join(base, "recursos")
arquivos_pdf = [
    f for f in os.listdir(recursos) if f.endswith(".pdf")
]

@pytest.mark.parametrize("pdf_file", arquivos_pdf)
def test_access_extrato_bancario(page, pdf_file):
    pdf_path = os.path.join(recursos, pdf_file)
    json_path = pdf_path.replace(".pdf", ".json")

    assert os.path.exists(json_path), f"JSON de comparação não encontrado para {pdf_file}"

    with open(json_path, encoding="utf-8") as f:
        dados_esperados = json.load(f)

    # Captura a resposta real ao abrir o extrato
    with page.expect_response(lambda r: "/api/extratos-bancarios/ler-extrato" in r.url and r.status == 200) as resp_info:
        carregar_extrato_bancario(page, pdf_path)

    response = resp_info.value
    json_data = response.json()
    lancamentos = json_data["dadosTelaExtratos"]

    assert len(lancamentos) == len(dados_esperados), f"Qtd diferente: esperado {len(dados_esperados)}, veio {len(lancamentos)}"

    for i, esperado in enumerate(dados_esperados):
        item = lancamentos[i]
        assert item["data"] == esperado["data"]
        assert item["documento"] == esperado["documento"]
        assert item["complemento"] == esperado["complemento"]
        assert (item["credito"] is not None) == esperado["credito"]
        assert (item["debito"] is not None) == esperado["debito"]
        assert float(item["valor"]) == float(esperado["valor"])
        assert item["origem"] == esperado["origem"]

        #comparação dos lançamentos do início, meio e fim da grid com os dados esperados
        # === Validação dos lançamentos no grid ===

'''
        quantidade_ui = page.locator("span", has_text="Quantidade").inner_text()
        quantidade_ui_num = int(quantidade_ui.split(":")[1].strip())
        assert quantidade_ui_num == len(lancamentos), f"Quantidade exibida: {quantidade_ui_num} != {len(lancamentos)}"

        linhas_locator = page.locator("//tbody/tr[contains(@class, 'dx-data-row')]")
        assert linhas_locator.count() > 0, "A grid não tem linhas!"
        scrollable = page.locator("#extrato-grid-lancamentos .dx-scrollable-container")

        total_linhas = linhas_locator.count()
        blocos = [
            range(0, 5),
            range(total_linhas // 2, total_linhas // 2 + 5),
            range(total_linhas - 5, total_linhas)
        ]

        for bloco in blocos:
            for idx_bloco in bloco:
                linha = linhas_locator.nth(idx_bloco)

                try:
                    linha.scroll_into_view_if_needed(timeout=2000)
                except:
                    # fallback: scroll manual na div, caso precise
                    page.eval_on_selector(
                        "#extrato-grid-lancamentos .dx-scrollable-container",
                        f"(el) => el.scrollTop = {idx_bloco * 34}"  
                    )
                    time.sleep(0.2)  

                colunas = linha.locator("td")

                data_ui = colunas.nth(1).inner_text().strip()
                debito_ui = colunas.nth(2).inner_text().strip()
                credito_ui = colunas.nth(3).inner_text().strip()
                valor_ui = colunas.nth(4).inner_text().strip()
                documento_ui = colunas.nth(5).inner_text().strip()
                complemento_ui = colunas.nth(6).inner_text().strip()
                origem_ui = colunas.nth(7).inner_text().strip()

                # Faz o match dinâmico
                candidatos = [
                    e for e in dados_esperados if e[0] == data_ui and e[5] == complemento_ui
                ]
                assert candidatos, f"Nenhum lançamento esperado bate com data '{data_ui}' e complemento '{complemento_ui}'"
                esperado = candidatos[0]

                # Valida campos
                assert data_ui == esperado[0], f"Grid Linha {idx_bloco + 1}: Data esperado '{esperado[0]}', obtido '{data_ui}'"

                if debito_ui:
                    assert esperado[1] == "51", f"Grid Linha {idx_bloco + 1}: deveria ter débito"
                    assert esperado[2] == "", f"Grid Linha {idx_bloco + 1}: não deveria ter crédito"
                elif credito_ui:
                    assert esperado[1] == "", f"Grid Linha {idx_bloco + 1}: não deveria ter débito"
                    assert esperado[2] == "51", f"Grid Linha {idx_bloco + 1}: deveria ter crédito"
                else:
                    raise AssertionError(f"Grid Linha {idx_bloco + 1}: Nenhum débito/crédito")

                # Valor: parse exato!
                valor_float = float(
                    valor_ui.replace("R$", "")
                    .replace("\xa0", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
                assert valor_float == esperado[
                    3], f"Grid Linha {idx_bloco + 1}: Valor esperado '{esperado[3]}', obtido '{valor_float}'"

                assert documento_ui == esperado[
                    4], f"Grid Linha {idx_bloco + 1}: Documento esperado '{esperado[4]}', obtido '{documento_ui}'"
                assert complemento_ui == esperado[
                    5], f"Grid Linha {idx_bloco + 1}: Complemento esperado '{esperado[5]}', obtido '{complemento_ui}'"
                assert origem_ui == esperado[
                    6], f"Grid Linha {idx_bloco + 1}: Origem esperado '{esperado[6]}', obtido '{origem_ui}'"
'''
