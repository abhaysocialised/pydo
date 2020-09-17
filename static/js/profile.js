$(document).ready(function () {
  const name = $("#name");
  const old_name = name.val()
  const oldPassword = $("#old-password");
  const newPassword = $("#new-password");
  const updateProfile = $("#update-profile");
  const deleteProfile = $("#delete-profile");
  const updates = $("#updates");
  const error = $("#error");

  name.on("input", () => {
    if ((name.val().length > 50) || (name.val().length < 2)) {
      $("#nameError").text("Please enter Your Legal name and your name should not be greater than 50 Characters.");
    } else {
      $("#nameError").text("");
    }
  });

  newPassword.on("input",
    () => {
      if (newPassword.val().length < 8) {
        error.text("Please create a password greater than or equal to 8.");
      } else {
        error.text("");
      }
    });

  updateProfile.on("click",
    () => {
      if (true) {
        $.ajax({
          url: "/ajax/update-profile/",
          type: "post",
          data: {
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            name: name.val(),
            old_password: oldPassword.val(),
            new_password: newPassword.val(),
          },
          success: (data, status = null, xhr = null) => {
            if (data.name_updated) {
              updates.append(`<div class="alert alert-success alert-dismissible fade show" role="alert">
                <small><strong>Congrats !!!</strong>Name updated Successfully...</small>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
                </div>`);
            } else {
              $("#nameError").text(`${data.nameError}`)
            }
            if (data.password_updated) {
              updates.append(`<div class="alert alert-success alert-dismissible fade show" role="alert">
                <small><strong>Congrats !!!</strong>Password updated Successfully...</small>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
                </div>`);
              oldPassword.val("")
              newPassword.val("")
            } else {
              error.text(data.passwordError)
            }
          },
          error: (data, status = null, xhr = null) => {
            alert("Bad Request....")
          },
        })
      }

    });

  const deleteConfirmBtn = $("#delete-confirm");
  const deleteConfirmPasswd = $("#delete-password-confirm");
  deleteConfirmPasswd.on("input", () => {
    $("#delete-error").text("")
  });
  deleteConfirmBtn.on("click", () => {
    if (deleteConfirmPasswd.val() == "") {
      $("#delete-error").text("Empty password not accepted...");
    } else {
      $.ajax({
        url: "/ajax/delete-account/",
        type: "post",
        data: {
          csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
          password: deleteConfirmPasswd.val(),
        },
        success: (data, status = null, xhr = null) => {
          if (data.deleted) {
            window.location = "/logout";
          } else {
            $("#delete-error").text(data.error);
          }
        },
        error: (data, status = null, xhr = null) => {
          alert("Bad Request...")
        },
      });
    }
  });
});