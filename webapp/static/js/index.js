let tg = window.Telegram.WebApp;
tg.expand();
let tuser_id = tg.initData ? tg.initDataUnsafe.user.id : 486190703;
let userLanguage = tg.initData ? tg.initDataUnsafe.user.language_code : 'ru';
console.log(userLanguage);

let get_non_expired_url = NaN;

function set_get_non_expired_url(url) {
    get_non_expired_url = url;
}

let get_expired_url = NaN;

function set_get_expired_url(url) {
    get_expired_url = url;
}

function request_drugs(url, target_table) {
    $.ajax({
        url: url,
        type: "GET",
        data: {usr_id: tuser_id},
        dataType: 'html',
        success: function (response) {
            let drugs = JSON.parse(response);
            drugs.forEach(drug => {
                //drug['title'] = 'аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин аспирин '
                add_drug_item(drug, target_table);
                document.querySelectorAll("[data-i18n-key]").forEach(translateElement);
            });
        },
        error: function (xhr, textStatus, error) {
            console.error(error)
        }
    });
}

function switch_tab(id) {
    switch (id) {
        case NON_EXPIRED:
            $(`#${EXPIRED}`).hide();

            $(`#${NON_EXPIRED}`).show();
            $("#add_drug_panel").show();
            break;
        case EXPIRED:
            $(`#${NON_EXPIRED}`).hide();
            $("#add_drug_panel").hide();

            $(`#${EXPIRED}`).show();
            break;
    }
}