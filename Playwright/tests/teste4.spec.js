import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.demoblaze.com/index.html');
  await page.getByRole('link', { name: 'Log in' }).click();
  await page.locator('#loginusername').click();
  await page.locator('#loginusername').fill('ananan');
  await page.locator('#loginusername').press('Tab');
  await page.locator('#loginpassword').fill('123456');
  await page.locator('#loginpassword').press('Enter');
  await page.locator('#loginpassword').press('Enter');
  await page.locator('#loginpassword').click();
  await page.getByRole('button', { name: 'Log in' }).click();
});

//test generator

//gravar testes

//npx playwright codegen -> abre o ambiente
//npx playwright codegen --help -> acesso aos comandos do codegen
//npx playwright codegen -o tests/teste4.spec.js -> abre o ambiente, cria um arquivo no caminho indicado e automaticamente
//grava o teste nele ao parar a gravação
//npx playwright codegen --device "iPhone13" -> simulará o ambiente do celular
//npx playwright codegen --viewport-size "1280, 720" -> altera tamanho da janela de visualização

//gerar locators 
//clicar na opção pick locator e selecionar o elemento desejado
