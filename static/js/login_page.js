'use strict';
(function () {
  const CODE_LENGTH = 5;
  const form = document.querySelector(`.form-container`);
  const phone = form.querySelector(`.js-phone`);
  const code = form.querySelector(`.js-code`);
  const codeInput = code.querySelector(`input`);
  const checkbox = form.querySelector(`.js-checkbox`);
  const checkboxInput = checkbox.querySelector(`input`);
  const message = form.querySelector(`.js-message small`);
  const codeMessage = form.querySelector(`.js-code-message small`);

  let newData;

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  const csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  const phoneMask = IMask(phone, {
    mask: '+{7} 000 000 00 00',
    prepare: function (appended, masked) {
      if (appended === `8` && masked.value === ``) {
        return ``;
      }
      return appended;
    }
  });

  const codeMask = IMask(codeInput, {
    mask: Number
  });

  const clearMessage = () => {
    message.textContent = ``;
    codeMessage.textContent = ``;
  };

  const successHandler = (data) => {
    if (data.success) {
      window.location.href = data.url;
    } else {
      checkboxInput.checked = false
      codeMessage.textContent = data.message;
    }
  };

  const errorHandler = (data) => {
    console.log('Упал в ошибку')
    console.log(data);
  };

  const phoneSuccessHandler = (data) => {
    // console.log(data);
    if (data.success) {
      code.classList.remove(`d-none`);
      codeInput.focus();
      codeMask.on(`accept`, checkForm);
      checkbox.classList.remove(`d-none`);
      checkboxInput.addEventListener(`change`, checkForm);
    } else {
      message.textContent = data.message;
    }
  };

  const phoneErrorHandler = (data) => {
    console.log(data);
  };

  const checkForm = () => {
    clearMessage();
    if (checkboxInput.checked && codeInput.value.length === CODE_LENGTH) {
      let data = {
        username: newData.username,
        code: codeInput.value
      };

      $.ajax({
        type: 'POST',
        data: data,
        headers:{"X-CSRFToken": csrftoken},
        success: successHandler,
        error: errorHandler
      });
    }
  };

  phoneMask.on(`complete`, function () {
    clearMessage();
    newData = {
      username: `+${phoneMask.unmaskedValue}`
    };
    $.ajax({
      type: 'POST',
      url: '',
      data: newData,
      success: phoneSuccessHandler,
      error: phoneErrorHandler
    });
    // window.backend.post(``, phoneSuccessHandler, phoneErrorHandler, newData);
  });
})();