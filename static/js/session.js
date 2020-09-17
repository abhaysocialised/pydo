$(document).ready(function() {
  const todo = $("#todo");
  const add_btn = $("#add_todo");

  const todoParent = $("#todo-list");
  const todoRoot = $("#todo-root");
  const alerts = $("#alerts");
  const emptyTodo = $("#empty-todo");


  function updateTodo(id) {
    $(`#${id}`).on("click", function() {
      let is_done = this.checked;
      $.ajax({
        url: "/ajax/update-todo/",
        type: "post",
        data: {
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          id: id,
          is_done: is_done,
        },
        success: (data, status = null, xhr = null) => {
          if (data.updated) {
            if (data.is_done == "true") {
              $(`#${id}`).attr("checked", "true")
              alerts.html(`<div class="alert alert-success alert-dismissible fade show" role="alert">
                <small><strong>Congrats !!!</strong> You have completed your ToDo <label for="${id}-delete" class="text-primary">Delete ToDo</label>...</small>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
                </div>`);
            } else {
              $(`#${id}`).attr("checked", "false")
              alerts.html(`<div class="alert alert-warning alert-dismissible fade show" role="alert">
                <small><strong>You</strong> must complete this todo as fast as possible...</small>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
                </div>`)
            }
          } else {
            alerts.html(`<div class="alert alert-danger alert-dismissible fade show" role="alert">
              <small><strong>${data.error}</strong></small>
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
              </button>
              </div>`)
          }
        },
        error: (data, status = null, xhr = null) => {
          alert("Bad Request....");
        }
      });
    })
  }

  function deleteTodo(id) {
    $(`input[uuid='${id}']`).on('click', function() {
      $.ajax({
        url: "/ajax/delete-todo/",
        type: "post",
        data: {
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          id: id,
        },
        success: (data, status = null, xhr = null) => {
          if (data.deleted) {
            alerts.html(`<div class="alert alert-warning alert-dismissible fade show" role="alert">
              <small><strong>Sucessfully Deleted</strong>!!!</small>
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
              </button>
              </div>`);
            $(`#${id}-parent`).remove()
            if (todoParent.children(".todo-list-item").length === 0) {
              emptyTodo.show();
            }
          } else {
            alerts.html(`<div class="alert alert-danger alert-dismissible fade show" role="alert">
              <small><strong>${data.error}</strong></small>
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
              </button>
              </div>`)
          }
        },

        error: (data = null, status = null, xhr = null) => {
          alert("Bad Request....")
        }
      })
    })
  }

  $.ajax({
    url: "/ajax/get-todos/",
    type: "post",
    data: {
      csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    },
    success: (data,
      status = null,
      xhr = null) => {
      let len = 0
      for (let todo in data) {
        len += 1;
        if (data[todo].is_done) {
          todoRoot.after($(`<li class="list-group-item text-dark text-center todo-list-item" id="${todo}-parent">
            <div class="row">
            <div class="col-1 text-center d-inline-block"><input type="checkbox" id="${todo}" checked/></div>
            <label for="${todo}" class="col-7 text-center overflow-auto d-inline-block"><input type="text" class="w-100 border-top-0 border-left-0 border-right-0 todo-txt bg-light text-dark" value="${data[todo].todo}" disabled></label>
            <div class="col-3 text-center d-inline-block"><input type="button" onclick="deleteTodo(this)" uuid="${todo}" class="btn btn-danger delete-btn" value="Delete" id="${todo}-delete" ></div>
            </div>
            </li>`));

        } else {
          let root = $("<li>")
          todoRoot.after($(`<li class="list-group-item text-dark text-center todo-list-item" id="${todo}-parent">
            <div class="row">
            <div class="col-1 text-center d-inline-block"><input type="checkbox" id="${todo}" /></div>
            <label for="${todo}" class="col-7 text-center d-inline-block"><input type="text" class="w-100 border-top-0 border-left-0 border-right-0 todo-txt bg-light text-dark" value="${data[todo].todo}" disabled></label>
            <div class="col-3 text-center d-inline-block"><input type="button" onclick="deleteTodo(this)" uuid="${todo}" class="btn btn-danger delete-btn" value="Delete" id="${todo}-delete" ></div>
            </div>
            </li>`));
        }
        // for btn
        deleteTodo(todo)
        // for checkbox
        updateTodo(todo)

      }
      if (len != 0) {
        emptyTodo.hide()
      }
    },
    error: (data, status = null, xhr = null) => {
      alert("Bad Request....")
    }
  })

  add_btn.on("click",
    () => {
      $.ajax({
        url: "/ajax/create-todo/",
        type: "post",
        data: {
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          todo: todo.val().toLowerCase(),
        },
        success: (data, status = null, xhr = null) => {
          if (data.created == true) {
            emptyTodo.hide();
            todoRoot.after($(`<li class="list-group-item text-dark text-center todo-list-item " id="${data.id}-parent">
              <div class="row">
              <div class="col-1 text-center d-inline-block"><input type="checkbox" id="${data.id}" /></div>
              <label for="${data.id}" class="col-7 text-center overflow-auto d-inline-block"><input type="text" class="w-100 border-top-0 border-left-0 border-right-0 todo-txt bg-light text-dark" value="${data.todo}" disabled></label>
              <div class="col-3 text-center d-inline-block"><input type="button" onclick="deleteTodo(this)" uuid="${data.id}" class="btn btn-danger delete-btn" value="Delete" id="${data.id}-delete" ></div>
              </div>
              </li>`));
            // for btn
            deleteTodo(data.id);
            // for checkbox
            updateTodo(data.id);
          } else {
            alerts.html(`<div class="alert alert-danger alert-dismissible fade show" role="alert">
              <small><strong>${data.error}</strong></small>
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
              </button>
              </div>`)
          }
          todo.val("")
        },
        error: (data = {}, status = null, xhr = null) => {
          alert("Bad Request....")
        },
      });
    });
});