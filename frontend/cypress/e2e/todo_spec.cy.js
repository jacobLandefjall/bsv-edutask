describe('EduTask To-Do Functionality', () => {

    // Starta om appen och klicka på en befintlig task (så att TaskDetail visas)
    beforeEach(() => {
        cy.visit('http://localhost:3000');

        // Vänta tills en task finns i listan och klicka för att öppna TaskDetail
        cy.get('.container-element img').first().click();

        // Vänta tills inputfältet i TaskDetail är synligt
        cy.get('input[placeholder="Add a new todo item"]').should('exist');
    });

    // R8UC1: Skapa en ny to-do
    it('TC1.1: Create a new to-do item', () => {
        cy.get('input[placeholder="Add a new todo item"]').type('New Task');
        cy.get('input[type="submit"][value="Add"]').click();
        cy.contains('New Task').should('exist');
    });

    it('TC1.2: "Add" button should be disabled when input is empty', () => {
        cy.get('input[placeholder="Add a new todo item"]').clear();
        cy.get('input[type="submit"][value="Add"]').should('be.disabled');
    });

    it('TC1.3: Create multiple todos in correct order', () => {
        const todos = ['Task 1', 'Task 2', 'Task 3'];
        todos.forEach(todo => {
            cy.get('input[placeholder="Add a new todo item"]').type(todo);
            cy.get('input[type="submit"][value="Add"]').click();
        });

        cy.get('ul.todo-list .todo-item').then(items => {
            expect(items[0]).to.contain.text('Task 1');
            expect(items[1]).to.contain.text('Task 2');
            expect(items[2]).to.contain.text('Task 3');
        });
    });

    // R8UC2: Toggla status
    it('TC2.1: Mark a to-do item as complete', () => {
        cy.get('input[placeholder="Add a new todo item"]').type('Complete Task');
        cy.get('input[type="submit"][value="Add"]').click();
        cy.contains('Complete Task').parent().find('.checker').click();
        cy.contains('Complete Task').parent().find('.checker').should('have.class', 'checked');
    });

    it('TC2.2: Unmark a to-do item as complete', () => {
        cy.get('input[placeholder="Add a new todo item"]').type('Toggle Task');
        cy.get('input[type="submit"][value="Add"]').click();
        cy.contains('Toggle Task').parent().find('.checker').click(); // mark as done
        cy.contains('Toggle Task').parent().find('.checker').click(); // unmark
        cy.contains('Toggle Task').parent().find('.checker').should('not.have.class', 'checked');
    });

    // R8UC3: Radera to-do
    it('TC3.1: Delete a to-do item', () => {
        cy.get('input[placeholder="Add a new todo item"]').type('Task to Delete');
        cy.get('input[type="submit"][value="Add"]').click();
        cy.contains('Task to Delete').parent().find('.remover').click();
        cy.contains('Task to Delete').should('not.exist');
    });
});
