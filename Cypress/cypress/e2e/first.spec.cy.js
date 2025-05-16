describe('template spec', () => {
  it('passes', () => {
    cy.visit('/auth/login')
    cy.get("[name='username']").type('Admin')
    cy.get("[name='password']").type('admin123')
    cy.get('.oxd-button').click()
    cy.get("[href='/web/index.php/pim/viewMyDetails']").click()
    cy.get('.employee-image').click()
    cy.get("[type='file']").selectFile('guax.jpg', {force: true})
    cy.get('.oxd-button').click()
  })
})