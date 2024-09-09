function swipe_box_initialization(swipeBox) {
    const scroller = swipeBox.querySelector('.swipe-box__scroller');
    scroller.scrollLeft += scroller.scrollWidth / 3;

    const observerOptions = {
        root: scroller,
        threshold: 1.0
    };
    const observer = new IntersectionObserver(handler, observerOptions);

    const items = scroller.querySelectorAll('.observe-item');
    items.forEach(item => {
        observer.observe(item);
    });
}

function swipe_boxes_initialization() {
    const swipeBoxes = document.querySelectorAll('.swipe-box');

    swipeBoxes.forEach(swipeBox => {
        swipe_box_initialization(swipeBox);
    });
}

document.addEventListener('DOMContentLoaded', swipe_boxes_initialization);

let del_drug_url = NaN;
function set_del_drug_url(value) {
    del_drug_url = value;
}

function handler(entries, observer) {
    for (const entry of entries) {
        if (entry.intersectionRatio === 1) {
            let drug_item = entry.target.closest('.swipe-box');
            const drug_id = drug_item.getAttribute('data-drug-id');

            $.ajax({
                type: "DELETE",
                url: del_drug_url,
                data: { "drug_id": drug_id }
            }).done(function () {
                console.log(drug_id);
                drug_item.remove();
                observer.unobserve(entry.target);
            });
        }
    }
}