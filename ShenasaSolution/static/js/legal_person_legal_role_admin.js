/**
 * Created by Ali.NET on 6/8/2020.
 */

var counter = 0;
function bind_selector() {
    var role_fields = document.querySelectorAll('[id^=id_legal_person_legal_role_target_person-][id$=-role]');
    if (!role_fields || role_fields.length == 0) {
        if (counter > max_try) return
        setTimeout(bind_selector, 1000);
        return;
    }

    role_fields.forEach(function (item, index) {
        var stocks = document.getElementById('id_legal_person_legal_role_target_person-{0}-number_of_stocks'.format(index));
        var investment = document.getElementById('id_legal_person_legal_role_target_person-{0}-amount_of_investment'.format(index));
        if (!stocks) return;
        init(item.value);
        item.onchange = function () {
            init(this.value);
        }

        function init(value) {
            stocks.style.display = value == 'ST' ? 'block' : 'none';
            investment.style.display = ['IN', 'IF', 'IV', 'IA'].includes(value) ? 'block' : 'none';
        }
    })

    document.querySelector('[id=legalperson_form] tr[class=add-row] a').onclick = function () {
        bind_selector();
    }
}


bind_selector();