/**
 * Created by Ali.NET on 6/8/2020.
 */

function bind_selector() {
    var role_field = document.getElementById('id_role');
    if (!role_field) {
        setTimeout(bind_selector, 1000);
        return;
    }

    var shares = document.getElementsByClassName('fieldBox field-number_of_shares')[0];
    var investment = document.getElementsByClassName('fieldBox field-amount_of_investment')[0];

    init(role_field.value);
    role_field.onchange = function () {
        init(this.value);
    }

    function init(value) {
        shares.style.display = value == 'ST' ? 'block' : 'none';
        investment.style.display = ['IN', 'IF', 'IV', 'IA'].includes(value) ? 'block' : 'none';
    }
}


bind_selector();