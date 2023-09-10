// This script will trigger focus on the input element when the modal is shown
$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus');
});

// Trigger the modal and focus on input when button is clicked
$('#launchModalButton').click(function () {
    $('#exampleModal').modal('show');
    $('#modalInput').trigger('focus');
});
$('#close-todo-modal').click(function () {
    $('#exampleModal').modal('hide')
});
$('#close-todo-modal-update').click(function () {
    $('#updateModal').modal('hide')
});


const detailUrl = `{% url 'todo-detail' todo_id=0 %}`
const updateUrl = `{% url 'update-todo' todo_id=0 %}`
const deleteUrl = `{% url 'todo-delete' todo_id=0 %}`
const retrieveUrl = `{% url 'get-todo' todo_id=0 %}`

addRemoveEventTodo(deleteUrl)
addRetrieveEventTodo(retrieveUrl, updateUrl)
const todoItemsDiv = document.querySelector('.todo__list');
todoItemsDiv.addEventListener('change', event => {
    UpdateTasksPositions(event, detailUrl, deleteUrl)
});