import { test, expect } from '@playwright/test';

test('Login + Importação Extrato', async ({ page }) => {
  test.setTimeout(600000); 

  await page.goto('https://staging.automationweb.com.br/login');

  const tentarLogin = async () => {
    await page.fill('input[type="text"]', 'ana@qualidade.com.br');
    await page.fill('input[type="password"]', '@aut1234');
    await page.click('#signInButton');

    const dashboard = page.locator('.layout-vertical-nav');
    await expect(dashboard).toBeVisible({ timeout: 10000 });
  };

  try {
    await tentarLogin();
    console.log('Login efetuado');
  } catch (erro) {
    console.log('Tentando login novamente...');
    await tentarLogin();
  }

  await page.locator('.layout-vertical-nav').hover();
  await page.getByText('Contábil').click();
  await page.getByText('Extrato Bancário').click({ timeout: 5000 });

  await page.locator('.v-col.v-col-6').first().click();
  await page.getByText('SO LEVE PAPEIS LTDA').click();
  await page.locator('.dx-dropdowneditor-icon').first().click();
  await page.getByRole('gridcell', { name: '1.1.01.01.01.00' }).nth(0).click();
  await page.setInputFiles('input[type="file"]', 'C:/Pilar/Ana Clara Maiberg/Extratos e Comprovantes (Arquivos)/Extratos/Banco do Brasil/Modelo 1/Formato 2/AGOSTO.pdf');
  await page.click('#btnExecutar');

  try {
    const quantidade = page.locator('span', { hasText: 'Quantidade:' });
    const texto = await quantidade.textContent();
    const numeroQuantidade = texto.numeroQuantidade(/Quantidade:\s*(\d+)/);

    if (numeroQuantidade && parseInt(numeroQuantidade[1]) > 0) {
      console.log('Leitura feita com sucesso');
    } 
  } catch (error) {
    console.error('Não foi realizada a leitura');
    await page.screenshot({ path: 'erro_leitura.png' });
    throw error;
  }
});