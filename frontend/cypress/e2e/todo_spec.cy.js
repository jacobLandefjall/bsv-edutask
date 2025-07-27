describe('Todo Operations', () => {
  let taskId;
  let userId;
  let email;
  let name;


    const setupTestEnvironment = () => {
    // Login
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email);
    cy.get('form').submit();

    // Create task if it doesn't exist
    cy.contains('Test Task').should('not.exist').then(() => {
      cy.get('#title').type('Test Task');
      cy.get('#url').type('ooOELrGMn14');
      cy.get('form.submit-form').submit();
    });

    // Click on task
    cy.contains('Test Task').should('be.visible').click();
    cy.wait(1000);
  };

  before(function () {
    // Create initial test user
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        userId = response.body._id.$oid;
        email = user.email;
        name = user.firstName + ' ' + user.lastName;
      });
    });
  });

describe('Add Todo Item (R8UC1)', () => {
  beforeEach(() => {
    setupTestEnvironment();
  });

  it('should add valid todo item', () => {
    // Find the add todo form and input
    cy.get('.inline-form input[type="text"]')
      .scrollIntoView()
      .should('exist')
      .type('Study chapter 1', { force: true });

    // Submit the form
    cy.get('.inline-form input[type="submit"]')
      .click({ force: true });

    // Verify todo was added
    cy.get('.todo-list')
      .should('contain', 'Study chapter 1');

    // Verify todo is not marked as done
    cy.contains('Study chapter 1')
      .parent('.todo-item')
      .find('.checker')
      .should('have.class', 'unchecked');

    // Verify input was cleared
    cy.get('.inline-form input[type="text"]')
      .should('have.value', '');
  });

  it('should not allow empty todo submission', () => {
    cy.get('.todo-item').then($initialItems => {
      const initialCount = $initialItems.length;


      cy.get('.inline-form input[type="text"]')
        .invoke('val', '')
        .trigger('input', { force: true });


      cy.get('.inline-form input[type="submit"]')
        .click({ force: true });

      cy.get('.todo-item').should('have.length', initialCount);
    });
  });
});

  describe('Toggle Todo Status (R8UC2)', () => {
    beforeEach(() => {
      setupTestEnvironment();
    });

    it('should toggle todo status', () => {
      cy.get('.todo-item .checker')
        .first()
        .click();

      cy.get('.todo-item')
        .first()
        .find('.checker')
        .should('have.class', 'checked');
    });
  });

  describe('Delete Todo (R8UC3)', () => {
    beforeEach(() => {
      setupTestEnvironment();
    });

    it('should delete todo item', () => {

      cy.get('.todo-item').then($itemsBefore => {
        const initialLength = $itemsBefore.length;


        cy.get('.todo-item .remover')
          .first()
          .click();


        cy.get('.todo-item')
          .should('have.length.lessThan', initialLength);
      });
    });
  });

  after(function () {
    // Cleanup
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${userId}`
    });
  });
});

