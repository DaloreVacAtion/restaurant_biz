(function() {
 let GET_RESERVATIONS_URL = `/api/variants/`;
 const tableReservations = document.querySelector(`.custom-table`);
 const tableReservationsBody = tableReservations.querySelector(`tbody`);
 const strokesFragment = document.createDocumentFragment();
 let copyData = [];
 const renderStrokes = (data) => {
    for (let i = 0; i < data.length; i++) {
      strokesFragment.appendChild(window.blogTemplates.createStroke(data[i]));
    }

    tableReservationsBody.appendChild(strokesFragment);
  };

   const successHandler = (data) => {
       console.log('i am here')
       console.log(data)
    if (data.data.length > 0) {
      document.querySelector('div.reservations').classList.remove('d-none');
      copyData = data.data.slice();
      renderStrokes(copyData);
    } else {
      document.querySelector(`h2`).insertAdjacentHTML(`afterEnd`, `<p class="h3">Здесь будут отображаться Ваши заметки<p>`);
    }

  };

  const errorHandler = (error) => {
      if (error.status === 400) {
        alert('Не забудьте выбрать время и указать количество человек!')
      }
    console.log(error.status);
  };

  const createStrokesFragment = () => {
    let peoples = $('#num_peoples').val()
    let time = $('#time').val()
    window.backend.get('api/variants/?' + peoples + '&' + time, successHandler, errorHandler);
  };

  $('button.booking').on('click', function () {
    createStrokesFragment();
  })

})();