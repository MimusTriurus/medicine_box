//let tuser_id = window.Telegram.WebApp.initDataUnsafe.user.id;
let tuser_id = 486190703;
function updateValue(id) {
    $("#non_expired").hide();
    $("#expired").hide();

    $("#add_drug_panel").hide();
    $("#buy_drug_panel").hide();

    switch (id) {
        case 0:
            $("#non_expired").show();
            $("#add_drug_panel").show();
            break;
        case 1:
            $("#expired").show();
            $("#buy_drug_panel").show();
            break;
    }
}