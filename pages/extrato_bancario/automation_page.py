from warnings import catch_warnings

from playwright.sync_api import Page

class AutomationPage:
    def __init__(self, page: Page):
        self.page = page

    def login(self):
        tentativa = 0

        while (tentativa < 4):
            try:
                self.page.goto("https://staging.automationweb.com.br/")

                # Preencher campos de login
                input_email = self.page.locator("#login-email > div.dx-texteditor-container > div.dx-texteditor-input-container > input")
                input_email.click(delay=500)
                input_email.fill("pilar@qualidade.com.br")

                # Preencher campos de senha
                input_senha = self.page.locator("#login-senha > div.dx-texteditor-container > div.dx-texteditor-input-container > input")
                input_senha.click(delay=500)
                input_senha.fill("@aut1234")

                # Realizar login
                self.page.locator("#login-entrar").click(delay=500)
                if not self.page.is_visible("div[class='v-responsive v-img']"):
                    self.page.locator("#login-entrar").click(delay=500)

                self.page.wait_for_timeout(500)
                self.page.wait_for_selector("div[class='v-responsive v-img']", timeout=1000, state="visible")
                break
            except:
                continue
            finally:
                tentativa = tentativa + 1

    def acessar(self, pagina: str, selector_espera: str):
        self.page.goto("https://staging.automationweb.com.br/" + pagina)
        self.page.wait_for_selector(selector_espera, timeout=3000, state="visible")



