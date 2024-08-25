document.addEventListener('DOMContentLoaded', function () {
  const swipeBoxes = document.querySelectorAll('.swipe-box');
  swipeBoxes.forEach(swipeBox => {
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
  });
});

function handler(entries, observer) {
  for (const entry of entries) {
    if (entry.intersectionRatio === 1) {
      entry.target.closest('.drug__item').remove()
      observer.unobserve(entry.target);
    }
  }
}