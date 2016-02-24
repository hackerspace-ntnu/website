$(function() {
    var showLogin = false;
    var timeout;
    $('#loginform').addClass('loginHide');
    $('#status').click(function() {
        showLogin = !showLogin;
        $('#loginform').removeClass('loginHide');
        $('#loginform').removeClass('loginStill');
        if (showLogin) {
            clearTimeout(timeout);
            $('#loginform').removeClass('loginOut');
            $('#loginform').addClass('loginIn');
            $('#loginform').css('display', 'inline');
            $("#loginform [name='username']").focus();
        } else {
            $('#loginform').removeClass('loginIn');
            $('#loginform').addClass('loginOut');
            timeout = setTimeout(function () {
                $('#loginform').css('display', 'none');
            }, 500);
        }
    });
});
