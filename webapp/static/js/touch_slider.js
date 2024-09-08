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

function handler(entries, observer) {
  for (const entry of entries) {
    if (entry.intersectionRatio === 1) {
      entry.target.closest('.swipe-box').remove();
      observer.unobserve(entry.target);
    }
  }
}

let i = 0;

function addTestDrug() {
    let drug = {};
    drug["element_id"] = `drug_${i}`;
    drug["title"] = `Aspirin_${i}`;
    drug["date"] = `${i}.${i}.2024`;
    drug["description"] = `description ${i}`;
    i++;
    addDrug(drug);
}

function addDrug(drug) {
    let swipeBox = document.createElement('li');
    swipeBox.className = 'swipe-box';
    swipeBox.innerHTML = `
        <div class="drug__item">
            <div class="swipe-box__scroller">
                <div class="swipe-box__item observe-item">
                  <label class="drug-action action--delete-left">
                      <span class="glyphicon glyphicon-trash"/>
                  </label>
                </div>

                <div class="swipe-box__item">
                    <input type="radio" name="accordion" id="${drug["element_id"]}"/>
                    <section class="box">
                        <label class="box-title" for="${drug["element_id"]}">
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
    document.getElementById('list').appendChild(swipeBox);

    swipe_box_initialization(swipeBox);
}