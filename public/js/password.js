// Calls ajax to test for password correctness (set session loggedin) and return an output
$("#password-submit-button").click(() => {
    // Sends entered password to backend and returns a validation result
    $.post('/ajax/password-check', {password: $('#password-input').val()}, (is_valid) => {
        console.log(!!is_valid)
        if (!is_valid) {
            // Displays error
            $("#password-error").css("visibility", "visible");
        } else {
            // Redirects
            window.location.href = "/"
        }
    })
});