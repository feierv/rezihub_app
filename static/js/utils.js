function apiRetrieveTodo(url, callback){
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {

        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const fields = response.task.fields
            callback(fields);
          }
        }
    }
    xhr.send();
}

function apiRequestGetAllTodo(url, type, data=null){
    const xhr = new XMLHttpRequest();
    xhr.open(type, url, true);

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.setRequestHeader('Content-Type', 'application/json');

    
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          // const response = JSON.parse(xhr.responseText);
          // console.log(response)
          // const newTasks = JSON.parse(response.tasks);
          const newTasks = JSON.parse(xhr.responseText)['tasks'];

          todoItemsDiv.innerHTML = '';

          for (const task of newTasks) {
            const taskElement = document.createElement('div');
            taskElement.setAttribute('data-task-id', task.pk);
            taskElement.innerHTML = `
            <div class="todo__card" data-task-id='${task.pk}'>
            <div class="todo__card--content">
                <input type="checkbox" class="todo__card--checkbox"
                ${task.fields.is_completed ? 'checked' : ''}
                 id='task_${task.pk}'>
                <label for="task_${task.pk}"></label>
                <div class="todo__card--content-info">
                    <div class="todo__card--title">${task.fields.description}</div>
                    <div class="todo__card--date">${task.fields.deadline}</div>
                </div>
            </div>
            <div class="todo__card--actions" data-task-id='${task.pk}'>
                <button class="button__actions button__actions--edit"><i
                        class="fa-solid fa-pencil"></i></button>
                <button class="button__actions button__actions--delete"><i
                        class="fa-solid fa-trash"></i></button>
            </div>
        </div>`
            todoItemsDiv.appendChild(taskElement);
          }
        } else {
          // Request failed, handle error
        }
      }
    };
    if (data){
        data = JSON.stringify(data)
    }
    xhr.send(data);
}

function addRetrieveEventTodo(retrieveUrl, updateUrl) {
    const todoItemsDiv = document.querySelector('.todo__list'); // Use a constant parent element
    todoItemsDiv.addEventListener('click', event => {
      const clickedElement = event.target;
      if (clickedElement.classList.contains('button__actions--edit') ||
      clickedElement.classList.contains('fa-pencil')) {
        // Find the nearest parent div with the data-task-id attribute
        const taskDiv = clickedElement.closest('[data-task-id]');
        
        // Get the data-task-id attribute value
        const taskId = taskDiv.getAttribute('data-task-id');
        updatedRetrieveUrl = retrieveUrl.replace('0', taskId);
        apiRetrieveTodo(updatedRetrieveUrl, function(fields) {
            // Now you have access to the fields variable
            $('#updateModal').modal('show');
            // Set the task description
            $('#updateModal').find('#first-name').val(fields.description);
            // Set the deadline date
            $('#updateModal').find('#todo-date').val(fields.deadline);
            updatedUpdateUrl = updateUrl.replace('0', taskId);
            const form = $('#updateModal').find('.auth-form');
            form.attr('action', updatedUpdateUrl);
            form.attr('method', 'POST');
        });
      }
    });
  }

function addRemoveEventTodo(deleteUrl) {
    const todoItemsDiv = document.querySelector('.todo__list'); // Use a constant parent element
    todoItemsDiv.addEventListener('click', event => {
      const clickedElement = event.target;
      if (clickedElement.classList.contains('button__actions--delete') ||
      clickedElement.classList.contains('fa-trash')) {
        // Find the nearest parent div with the data-task-id attribute
        const taskDiv = clickedElement.closest('[data-task-id]');
        
        // Get the data-task-id attribute value
        const taskId = taskDiv.getAttribute('data-task-id');
        
        // Use the taskId for your logic
        updatedDeleteUrl = deleteUrl.replace('0', taskId);
        apiRequestGetAllTodo(updatedDeleteUrl, 'DELETE')
      }
    });
  }

function UpdateTasksPositions(event, detailUrl, deleteUrl) {
    const checkbox = event.target;
    if (checkbox.classList.contains('todo__card--checkbox')) { // Check if it's a todo-element checkbox
      const taskId = checkbox.closest('[data-task-id]').getAttribute('data-task-id');
      detailUrl = detailUrl.replace('0', taskId);
      apiRequestGetAllTodo(detailUrl, 'PUT', {check: true})
    }
  }

  