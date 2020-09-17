$(document).ready(function() {

  const email = $("#email");
  const btn = $("#submit-btn")
  email.on("input",
    () => {
      if (email.val().match(/([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)/) == null) {
        $("#emailError").text("Please enter valid Email-id.");
        btn.hide()
      } else {
        $("#emailError").text("");
        btn.show()
      }
    });
})