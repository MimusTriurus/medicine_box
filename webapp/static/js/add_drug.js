let months = NaN;
let years = NaN;

// todo: move to function
let drug_candidates = {}
let update_drugs_candidates_url = NaN;
let add_drug_url = NaN;

let years_titles = []
const months_titles = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
];

function add_carousel_item(title, target) {
    let carousel_item = document.createElement('div');
    carousel_item.className = 'carousel-cell';
    carousel_item.innerHTML = `
            <label class="carousel-title">${title}</label>
        `;
    document.getElementById(target).appendChild(carousel_item);
}


let start_year = new Date().getFullYear();
for (let i = 0; i < 5; ++i) {
    const year = start_year++;
    years_titles.push(year)
}

function add_years() {
    for (let i = 0; i < years_titles.length; ++i) {
        add_carousel_item(years_titles[i], 'years_carousel');
    }
}

function add_months() {
    months_titles.forEach((element) => {
        add_carousel_item(element, 'months_carousel');
    });
}

function open_transition_end() {
    console.log('Transition opened ended');
}

function close_transition_end() {
    document.getElementById('control_panel').style = 'background: rgba(0, 0, 0, 0%); top: -100%';
}

function open_drug_window() {
    document.getElementById('control_panel').style = 'background: rgba(0, 0, 0, 30%);';
    document.getElementById('dialogAddDrug').className = 'opened';

    const transition_opened = document.querySelector(".opened");
    transition_opened.removeEventListener('transitionend', close_transition_end);
    transition_opened.addEventListener('transitionend', open_transition_end);
}

function close_drug_window() {
    document.getElementById('dialogAddDrug').className = 'closed';

    const transition_closed = document.querySelector(".closed");
    transition_closed.removeEventListener('transitionend', open_transition_end);
    transition_closed.addEventListener('transitionend', close_transition_end);
}

let i = 0;

function addTestDrug() {
    let drug = {};
    drug["element_id"] = `drug_${i}`;
    drug["title"] = `Aspirin_${i}`;
    drug["date"] = `${i}.${i}.2024`;
    drug["description"] = `description ${i}`;
    i++;
    addDrugItem(drug, 'list_non_expired');
}

function set_update_drugs_candidates_url(value) {
    update_drugs_candidates_url = value;
}

function set_add_drug_url(value) {
    add_drug_url = value;
}

function add_drug_item(drug, target) {
    let swipeBox = document.createElement('li');
    swipeBox.className = 'swipe-box';
    swipeBox.setAttribute('data-drug-id', drug["id"]);
    swipeBox.innerHTML = `
        <div class="drug__item">
            <div class="swipe-box__scroller">
                <div class="swipe-box__item observe-item">
                  <label class="drug-action action--delete-left">
                      <span class="glyphicon glyphicon-trash"/>
                  </label>
                </div>

                <div class="swipe-box__item">
                    <input type="radio" name="accordion" id="${drug["id"]}"/>
                    <section class="box">
                        <label class="box-title" for="${drug["id"]}">
                            <span>${drug["title"]}</span>
                            <br><span style="white-space: pre-line">${drug["date"]}</span>
                        </label>
                        <label class="box-close" for="acc-close"></label>
                        <div class="box-content">
                            ${drug["description"]}
                        </div>
                    </section>
                </div>

                <div class="swipe-box__item observe-item">
                  <label class="drug-action action--delete-right">
                      <span class="glyphicon glyphicon-trash"/>
                  </label>
                </div>
            </div>
        </div>
    `;
    document.getElementById(target).appendChild(swipeBox);

    swipe_box_initialization(swipeBox);
}

function add_drug() {
    const drug_name = document.getElementById('medicine_name').value;
    const id = drug_candidates[drug_name];

    const date = years_titles[years.selectedIndex] + '-' + (months.selectedIndex + 1);

    let drug_data = {
        'user_id': tuser_id,
        'name': drug_name,
        'date': date,
        'drug_id': id
    }

    $.ajax({
        type: "POST",
        url: add_drug_url,
        data: drug_data
    }).done(function (data) {
        add_drug_item(data,'list_non_expired');
    });
    //close_drug_window();
}

function updateDrugsCandidates(e) {
    $.ajax({
        type: "POST",
        url: update_drugs_candidates_url,
        data: e.target.value
    }).done(function (data) {
        drug_candidates = data;
        const drugs_titles = Object.keys(drug_candidates);
        $('#medicine_name').autocomplete({
            source: drugs_titles,
            minLength: 1
        });
    });
}

document.addEventListener('DOMContentLoaded', function () {
    let months_carousel = document.querySelector('#months_carousel');
    months = new Flickity(months_carousel, {
        accessibility: true,
    });

    let years_carousel = document.querySelector('#years_carousel');
    years = new Flickity(years_carousel, {
        accessibility: true,
    });

    $('#control_panel').click(function (e) {
        if (e.target.id === 'control_panel') {
            close_drug_window();
        }
    });

    const input = document.getElementById("medicine_name");
    input.addEventListener("input", updateDrugsCandidates);
});