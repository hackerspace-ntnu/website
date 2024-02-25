document.addEventListener("DOMContentLoaded", function(event) {
    // Vis og gjem deler som relateres til påmeldinger
    const reg_boxes = document.getElementsByClassName('reg-box');
    const reg_check = document.getElementsByName('registration')[0];
    const ext_reg = document.getElementsByClassName('ext-reg')[0];

    const setRegistrationHideClasses = checkbox => {
        if(checkbox.checked) {
            for (const reg_box of reg_boxes) {
                reg_box.classList.remove('hide')
            }
            ext_reg.classList.add('hide');
        } else {
            for (const reg_box of reg_boxes) {
                reg_box.classList.add('hide')
            }
            ext_reg.classList.remove('hide');
            document.getElementById('id_external_registration').value = '';
        }
    }

    setRegistrationHideClasses(reg_check);

    reg_check.onchange = function() { setRegistrationHideClasses(this) };
});
