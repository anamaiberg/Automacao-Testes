from playwright.sync_api import Page, expect

def test_example_page(page: Page):
    page.goto("https://www.google.com")
    expect(page).to_have_title("Google")
    page.locator("[aria-label=\"Pesquisar\"]").fill("Playwright Python")
    page.locator("[aria-label=\"Pesquisar\"]").press("Enter")
    expect(page.locator("#search")).to_contain_text("Playwright Python")

