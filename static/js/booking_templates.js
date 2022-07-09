'use strict';
(function () {
  const bookingTemplate = document.querySelector(`#reservationTemplate`).content.querySelector(`tr`);
  const createStroke = (booking) => {
    console.log('i am here')
    let stroke = bookingTemplate.cloneNode(true);
    let title = stroke.querySelector(`.title`);
    let tables_count = stroke.querySelector(`.tables_count`);
    let free_seats_count = stroke.querySelector(`.free_seats_count`);
    let avg_check = stroke.querySelector(`.avg_check`);
    let avg_time = stroke.querySelector(`.avg_time`);
    let showMoreBtn = stroke.querySelector(`.show-more`);

    stroke.id = `stroke-id-${booking.id}`;
    title.textContent = booking.name;
    free_seats_count.textContent = booking.available_seats;
    tables_count.textContent = booking.free_table_count;
    avg_check.textContent = booking.avg_cost;
    avg_time.textContent = booking.avg_time;
    showMoreBtn.href = booking.url;

    return stroke;
  };

  window.blogTemplates = {
    createStroke,
  };
})();