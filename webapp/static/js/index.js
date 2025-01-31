let tg = window.Telegram.WebApp;
tg.expand();
let tuser_id = tg.initData ? tg.initDataUnsafe.user.id : 486190703;
//let userLanguage = tg.initData ? tg.initDataUnsafe.user.language_code : 'ru';
let userLanguage = 'ru';

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
        type: 'GET',
        data: {user_id: tuser_id},
        dataType: 'html',
        success: function (response) {
            let drugs = JSON.parse(response);
            drugs.forEach(drug => {
                add_drug_item(drug, target_table);
                document.querySelectorAll("[data-i18n-key]").forEach(translateElement);
            });
        },
        error: function (xhr, textStatus, error) {
            console.error(error)
        }
    });
}

let current_tab = NON_EXPIRED;

function switch_tab(id) {
    current_tab = id;
    switch (current_tab) {
        case NON_EXPIRED:
            $(`#${EXPIRED}`).hide();

            $(`#${NON_EXPIRED}`).show();
            $("#add_drug_panel").show();
            $("#scan_drug_panel").show();
            break;
        case EXPIRED:
            $(`#${NON_EXPIRED}`).hide();
            $("#add_drug_panel").hide();
            $("#scan_drug_panel").hide();

            $(`#${EXPIRED}`).show();
            break;
    }
    while (drugs_local.length !== 0) {
        const data = drugs_local[drugs_local.length - 1];
        add_drug_item(data, data['target_table']);
        drugs_local.pop();
    }
}

window.translations = {};
window.translations_count = 0;

function translateElement(element) {
    if (window.translations_count === 0) {
        return;
    }
    const key = element.getAttribute('data-i18n-key');
    const translation = window.translations[key];
    if (translation === undefined) {
        return;
    }
    if (element.placeholder) {
        element.placeholder = translation;
    } else {
        element.innerText = translation;
    }
}