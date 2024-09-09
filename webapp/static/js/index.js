let tuser_id = 486190703;

function updateValue(id) {
    console.log(id)
    $("#list_non_expired").hide();
    $("#list_expired").hide();

    $("#add_drug_panel").hide();
    $("#buy_drug_panel").hide();

    switch (id) {
        case 0:
            $("#list_non_expired").show();
            $("#add_drug_panel").show();
            break;
        case 1:
            $("#list_expired").show();
            $("#buy_drug_panel").show();
            break;
    }
}