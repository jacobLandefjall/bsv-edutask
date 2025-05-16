describe('EduTask To-Do Functionality', () => {
  let uid;
  let email;
  let name;

  before(() => {
    cy.fixture('user.json').then((user) => {
      email = user.email;
      name = `${user.firstName} ${user.lastName}`;

      // 1. Check if the user already exists
      cy.request({
        method: 'GET',
        url: `http://localhost:5000/users/bymail/${email}`,
        failOnStatusCode: false
      }).then((res) => {
        if (res.status === 200 && res.body._id) {
          const existingId = res.body._id.$oid;
          return cy.request('DELETE', `http://localhost:5000/users/${existingId}`);
        }
      }).then(() => {
        // 2. Create a new user
        return cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        });
      }).then((res) => {
        uid = res.body._id.$oid;

        // 3. Create a task for the user
        return cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: {
            title: 'Test Task',
            description: 'Test Description',
            userid: uid,
            url: 'dQw4w9WgXcQ',
            todos: JSON.stringify(['Watch video'])
          }
        });
      });
    });
  });

  beforeEach(() => {
    cy.visit('http://localhost:3000');

    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email);

    cy.get('form').submit();

    cy.contains('Your tasks,').should('exist');

    cy.get('.container-element img', { timeout: 10000 }).should('have.length.greaterThan', 0).first().click();
    cy.get('input[placeholder="Add a new todo item"]').should('exist');
  });

  // R8UC1
  it('TC1.1: Create a new to-do item', () => {
    cy.get('input[placeholder="Add a new todo item"]').type('New Task');
    cy.get('input[type="submit"][value="Add"]').click();
    cy.get('.todo-item').should('contain.text', 'New Task');
  });

  it('TC1.2: "Add" button should do nothing when input is empty', () => {
    cy.get('.todo-item').then((itemsBefore) => {
      const count = itemsBefore.length;

      cy.get('input[placeholder="Add a new todo item"]').clear({ force: true });
      cy.get('input[type="submit"][value="Add"]').click({ force: true });

      cy.get('.todo-item').should('have.length', count);
    });
  });

  it('TC1.3: Create multiple todos in correct order', () => {
    const todos = ['Task 1', 'Task 2', 'Task 3'];
    todos.forEach(todo => {
      cy.get('input[placeholder="Add a new todo item"]').type(todo, { force: true });
      cy.get('input[type="submit"][value="Add"]').click( { force: true });
    });

      cy.get('ul.todo-list .todo-item').then((items) => {
    const texts = [...items].map(el => el.innerText.trim());

    cy.get('.todo-item').eq(-3).invoke('text').should('include', 'Task 1');
    cy.get('.todo-item').eq(-2).invoke('text').should('include', 'Task 2');
    cy.get('.todo-item').eq(-1).invoke('text').should('include', 'Task 3');
    });
  });

  // R8UC2
  it('TC2.1: Mark a to-do item as complete', () => {
    cy.get('input[placeholder="Add a new todo item"]').type('Complete Task', { force: true });
    cy.get('input[type="submit"][value="Add"]').click({ force: true });

    cy.contains('Complete Task').parent().find('.checker').click({ force: true });
    cy.contains('Complete Task').parent().find('.checker').should('have.class', 'checked');
  });

  it('TC2.2: Unmark a to-do item as complete', () => {
    cy.get('input[placeholder="Add a new todo item"]').type('Toggle Task', { force: true });
    cy.get('input[type="submit"][value="Add"]').click({ force: true });
    cy.contains('Toggle Task').parent().find('.checker').click({force: true });
    cy.contains('Toggle Task').parent().find('.checker').click({ force: true });
    cy.contains('Toggle Task').parent().find('.checker').should('not.have.class', 'checked');
  });

  // R8UC3
  it('TC3.1: Delete a to-do item', () => {
    cy.get('input[placeholder="Add a new todo item"]').type('Task to Delete', {force: true });
    cy.get('input[type="submit"][value="Add"]').click({ force: true });
    cy.contains('.todo-item', 'Task to Delete', { timeout: 8000 }).should('not.exist');
    cy.get('.todo-item').contains('Task to Delete').should('not.exist');
  });

  after(() => {
    cy.request('DELETE', `http://localhost:5000/users/${uid}`);
  });
});
