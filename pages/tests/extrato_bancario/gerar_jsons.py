import os
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from pages.extrato_bancario.automation_page import AutomationPage
from pages.extrato_bancario.extrato_bancario_page import ExtratoBancarioPage

def carregar_extrato_bancario(page, extrato_path):
    print(f"Chamando carregar_extrato_bancario para: {extrato_path}")
    automation_page = AutomationPage(page)
    automation_page.login()
    automation_page.acessar("contabil/extrato-bancario", "h2:has-text('Extrato bancário')")
    extrato_bancario_page = ExtratoBancarioPage(page)
    extrato_bancario_page.selecionar_empresa(
        "#extrato-empresa > div > div > div.dx-texteditor-input-container > input",
        "33.278.206/0001-37"
    )
    extrato_bancario_page.selecionar_conta("51")
    extrato_bancario_page.selecionar_extrato(extrato_path)
    extrato_bancario_page.executar()
    extrato_bancario_page.esperar_lancamento()
    print(f"Carregar_extrato_bancario OK para {extrato_path}")

base = os.path.dirname(__file__)
recursos = os.path.join(base, "recursos")
todos_arquivos = os.listdir(recursos)

print(f"Encontrados {len(todos_arquivos)} PDFs em: {recursos}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for arquivo in todos_arquivos:
        page = browser.new_page()
        arquivo_path = os.path.join(recursos, arquivo)
        json_path = os.path.splitext(arquivo_path)[0] + ".json"

        if os.path.exists(json_path):
            print(f"JSON já existe, pulando: {json_path}")
            continue
        print(f"➡Processando: {arquivo}")

        try:
            print("Aguardando resposta da API...")
            with page.expect_response(
                lambda r: "/api/extratos-bancarios/ler-extrato" in r.url and r.status == 200) as resp_info:
                carregar_extrato_bancario(page, arquivo_path)

            response = resp_info.value
            json_data = response.json()
            print(f"API respondeu OK para {arquivo}")

            dados_esperados = []
            for item in json_data["dadosTelaExtratos"]:
                dados_esperados.append({
                    "data": item["data"],
                    "documento": item["documento"],
                    "complemento": item["complemento"],
                    "credito": bool(item["credito"]),
                    "debito": bool(item["debito"]),
                    "valor": item["valor"],
                    "origem": item["origem"]
                })

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(dados_esperados, f, indent=2, ensure_ascii=False)

            print(f"JSON salvo: {json_path}")

        except PlaywrightTimeoutError:
            print(f"Timeout ao processar: {arquivo}")
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
        finally:
            page.close()

    browser.close()

print("Finalizado gerar_jsons.py.")

# python -m pages.tests.extrato_bancario.gerar_jsons