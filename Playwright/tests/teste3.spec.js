import {test, expect} from '@playwright/test'

test('Built-inLocators', async ({page})=>{
    await page.goto('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login');

    //localizar um elemento pelo seu texto alternativo, geralmente uma imagem
    const logo = page.getByAltText('company-branding');
    await expect(logo).toBeVisible();

    //localizar elemento por placeholder, geralmente um input box
    await page.getByPlaceholder('Username').fill('Admin');
    await page.getByPlaceholder('Password').fill('admin123');

    //localizar por atributos de acessibilidade implícitos ou explícitos, geralmente um botão ou link
    page.getByRole('button',  {type: 'submit'}).click();

    //localizar pelo texto do elemento
    const name = await page.locator("//p[@class='oxd-userdropdown-name']").textContent();
    await expect(page.getByText(name)).toBeVisible();

    //page.getByLabel()
    //page.getByTitle()

    //o desenvolvedor e o qa podem se comunicar para aplicar data-testid nos elementos, a fim de localizar por um id específico para o qa
    //page.getByTestId( )
   
})

