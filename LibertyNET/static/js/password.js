/**
 * Created by taiowawaner on 5/31/14.
 */
function checkPasswordMatch() {
    var password = $("#id_password").val();
    var confirmPassword = $("#id_password2").val();

    if (password != confirmPassword)
        $("#divCheckPasswordMatch").html("Passwords do not match!");
    else
        $("#divCheckPasswordMatch").html("Passwords match.");
}

$(document).ready(function () {
   $("#txtConfirmPassword").keyup(checkPasswordMatch);
});

function passwordMatcher(pOne, pTwo){
    function checkPasswordMatch() {
    var password = $("#pOne").val();
    var confirmPassword = $("#pTwo").val();

    if (password != confirmPassword)
        $("#divCheckPasswordMatch").html("Passwords do not match!");
    else
        $("#divCheckPasswordMatch").html("Passwords match.");
}

$(document).ready(function () {
   $("#pTwo").keyup(checkPasswordMatch);
});
}
