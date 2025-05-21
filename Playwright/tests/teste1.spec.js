const {test, expect} = require('@playwright/test');

test('Home Page', async ({page})=>{
    await page.goto('https://www.demoblaze.com/index.html');

    const pageTitle = page.title();
    console.log('Page title is: ', pageTitle);
    await expect(page).toHaveTitle('STORE');

    await expect(page).toHaveURL('https://www.demoblaze.com/index.html');
    const pageURL =  page.url();
    console.log('page url: ', pageURL);

    await page.close();
})

/*  
async + await para tratar a forma assíncrona que o js opera como uma forma síncrona,
ou seja, em vez de executar tudo em um bloco vai executar linha por linha (ou step by step).

npx playwright test -> todos os testes em todos os browsers
npx playwright test Testando.spec.js -> arquivo de teste específico em todos os browsers
npx playwright test Testando.spec.js --project=chromium -> arquivo específico em browser específico
npx playwright test Testando.spec.js --project=chromium --headed -> com interface gráfica aberta
npx playwright test Testando.spec.js --project=chromium --headed --debug -> teste passo a passo com o script

npx playwright show-report
*/