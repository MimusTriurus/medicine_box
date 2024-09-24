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

let del_drug_url = NaN;
function set_del_drug_url(value) {
    del_drug_url = value;
}

let del_expired_drug_url = NaN;
function set_del_expired_drug_url(value) {
    del_expired_drug_url = value;
}

function handler(entries, observer) {
    for (const entry of entries) {
        if (entry.intersectionRatio === 1) {
            let drug_item = entry.target.closest('.swipe-box');
            const drug_id = drug_item.getAttribute('data-drug-id');
            const drug_type = drug_item.getAttribute('data-drug-type');
            let target_url = del_drug_url;
            if (drug_type === EXPIRED) {
                target_url = del_expired_drug_url;
            }
            $.ajax({
                type: 'DELETE',
                url: target_url,
                data: { 'drug_id': drug_id }
            }).done(function () {
                drug_item.remove();
                observer.unobserve(entry.target);
            });
        }
    }
}