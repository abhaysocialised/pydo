$(document).ready(function () {
  const name = $("#name");
  const email = $("#email");
  const password = $("#password");
  const btn = $("#submit-btn");

  const auths = []

  name.on("input", () => {
    if ((name.val().length > 50) || (name.val().length < 2)) {
      $("#nameError").text("Please enter Your Legal name and your name should not be greater than 50 Characters.");
    } else {
      $("#nameError").text("");
    }
  });

  email.on("input",
    () => {
      if (email.val().match(/([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)/) == null) {
        $("#emailError").text("Please enter valid Email-id.");
      } else {
        $("#emailError").text("");
      }
    });

  password.on("input",
    () => {
      if (password.val().length < 8) {
        $("#passwordError").text("Please create a password greater than or equal to 8.");
      } else {
        $("#passwordError").text("");
      }
    });

});