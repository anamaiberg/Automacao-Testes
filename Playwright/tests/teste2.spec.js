import {test, expect} from '@playwright/test'

test('Locators', async ({page})=>{
    await page.goto('https://www.demoblaze.com/index.html');

    //usando propriedade
    //await page.locator('id=login2').click();
    await page.click('id=login2')

    //usando css
    await page.fill('#loginusername', 'ananan');
    //page.type('loginusername');

    await page.fill("input[id='loginpassword']", '123456');
    await page.click("//button[normalize-space()='Log in']");
    const logoutlink = page.locator("//a[normalize-space()='Log out']");
    await expect(logoutlink).toBeVisible({timeout:16_000});

    const products = await page.$$("//div[@id='tbodyid']//div//h4/a");
    for(const product of products) {
        const productName = await product.textContent();
        console.log(productName);
    }

    await page.close();
})

//xpath com SelectorsHub