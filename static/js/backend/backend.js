'use strict';
(function () {
  const TIMEOUT_IN_MS = 10000;
  const StatusCode = {
    OK: [200, 201, 204]
  };

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  const csrftoken = getCookie('csrftoken');

  const createXHR = (method, url, onSuccess, onError) => {
    let xhr = new XMLHttpRequest();

    xhr.responseType = `json`;

    xhr.addEventListener(`load`, () => {
      if (StatusCode.OK.includes(xhr.status)) {
        onSuccess(xhr.response);
      } else {
        onError(xhr);
      }
    });

    xhr.addEventListener(`error`, () => {
      onError(`Произошла ошибка соединения`);
    });

    xhr.addEventListener(`timeout`, () => {
      onError(`Запрос не успел выполниться за ${xhr.timeout}мс`);
    });

    xhr.timeout = TIMEOUT_IN_MS;

    xhr.open(method, url);

    if (method === `DELETE` || method === `POST` || method === `PATCH`) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
      xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    }

    return xhr;
  };

  const getData = (url, onSuccess, onError) => {
    createXHR(`GET`, url, onSuccess, onError).send();
  };

  const postData = (url, onSuccess, onError, data) => {
    createXHR(`POST`, url, onSuccess, onError).send(JSON.stringify(data));
  };

  const patchData = (url, onSuccess, onError, data) => {
    createXHR(`PATCH`, url, onSuccess, onError).send(JSON.stringify(data));
  };

  const deleteData = (url, onSuccess, onError, data) => {
    createXHR(`DELETE`, url, onSuccess, onError).send(JSON.stringify(data));
  };

  window.backend = {
    get: getData,
    post: postData,
    patch: patchData,
    delete: deleteData
  };
})();