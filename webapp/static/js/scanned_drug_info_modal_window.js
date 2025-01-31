let add_scanned_drug_url = null;

let current_drug_data = null;
let scanned_drug_already_added = false;

function set_add_scanned_drug_url(value) {
    add_scanned_drug_url = value;
}

function initialize_add_scanned_drug_modal(drug_data) {
    current_drug_data = drug_data;
    let drug_name = current_drug_data['name'];
    let exp_date = current_drug_data['date'];
    let desc = current_drug_data['description'];
    let expired = current_drug_data['expired'] === 'true';
    scanned_drug_already_added = current_drug_data['exist'] === 'true';

    const scanned_drug_name = document.getElementById('scanned_drug_name');
    const scanned_drug_exp_date = document.getElementById('scanned_drug_exp_date');
    const scanned_drug_info = document.getElementById('scanned_drug_info');

    const add_scanned_drug_win_title = document.getElementById('add_scanned_drug_win_title');

    const add_scanned_drug_panel = document.getElementById('add_scanned_drug_panel');
    const COLLAPSE = 'collapse';
    const VISIBLE = 'visible';
    add_scanned_drug_panel.classList.remove(COLLAPSE);
    add_scanned_drug_panel.classList.remove(VISIBLE);
    add_scanned_drug_panel.classList.add(scanned_drug_already_added ? COLLAPSE : VISIBLE);

    scanned_drug_name.textContent = drug_name;
    scanned_drug_exp_date.textContent = BEST_BEFORE + exp_date;
    const drug_is_expired_title = document.getElementById('drug_is_expired_title');
    drug_is_expired_title.classList.remove(COLLAPSE);
    drug_is_expired_title.classList.remove(VISIBLE);
    drug_is_expired_title.classList.add(expired ? VISIBLE : COLLAPSE);

    const iconWarning = document.getElementById('iconWarning');
    iconWarning.classList.remove(COLLAPSE);
    iconWarning.classList.remove(VISIBLE);
    iconWarning.classList.add(scanned_drug_already_added ? VISIBLE : COLLAPSE);

    scanned_drug_info.textContent = desc;
    add_scanned_drug_win_title.textContent = scanned_drug_already_added ? DRUG_ALREADY_EXIST : ADD_DRUG;

    $('#addScannedDrugModal').modal('show');
}

function add_scanned_drug() {
    current_drug_data['user_id'] = tuser_id;

    $.ajax({
        type: 'POST',
        url: add_drug_url,
        data: current_drug_data
    }).done(function (data) {
        if (data['target_table'] === current_tab) {
            add_drug_item(data, data['target_table']);
        } else {
            drugs_local.push(data);
        }
    });
}