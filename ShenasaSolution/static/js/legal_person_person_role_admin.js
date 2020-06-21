/**
 * Created by Ali.NET on 6/8/2020.
 */

function bind_selector() {
    var role_field = document.getElementById('id_role');
    var role_fields = document.querySelectorAll('[id^=id_legalpersonpersonrole_set-][id$=-role]');
    if (!role_fields || role_fields.length == 0) {
        setTimeout(bind_selector, 1000);
        return;
    }

    role_fields.forEach(function (item, index) {
        var stocks = document.getElementById('id_legalpersonpersonrole_set-{0}-number_of_stocks'.format(index));
        var investment = document.getElementById('id_legalpersonpersonrole_set-{0}-amount_of_investment'.format(index));
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