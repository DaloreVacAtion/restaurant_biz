'use strict';
(function () {
  const DEBOUNCE_INTERVAL_IN_MS = 500;
  window.utils = {
    createMiddleFormatDate: (date) => {
      let dateCreate = new Date(date);
      let middleDate = `${dateCreate.getDate() < 10 ? `0` : ``}${dateCreate.getDate()}.${dateCreate.getMonth() < 9 ? `0` : ``}${dateCreate.getMonth() + 1}.${dateCreate.getFullYear()} ${dateCreate.getHours() < 10 ? `0` : ``}${dateCreate.getHours()}:${(dateCreate.getMinutes() < 10 ? `0` : ``)}${dateCreate.getMinutes()}`;

      return middleDate;
    },

    createShortFormatDate: (date) => {
      let dateCreate = new Date(date);
      let shortDate = `${dateCreate.getDate() < 10 ? `0` : ``}${dateCreate.getDate()}.${dateCreate.getMonth() < 9 ? `0` : ``}${dateCreate.getMonth() + 1}.${dateCreate.getFullYear()}`;

      return shortDate;
    },

    createTimeDate: (date) => {
      let dateCreate = new Date(date);
      let timeDate = `${dateCreate.getHours() < 10 ? `0` : ``}${dateCreate.getHours()}:${(dateCreate.getMinutes() < 10 ? `0` : ``)}${dateCreate.getMinutes()}`;

      return timeDate;
    },

    turnDateFront: (date) => {
      return date.split(`.`).reverse().join(`-`)
    },

    getIDURL: (url) => {
      let currentURL = new URL(url);

      return currentURL.pathname.replace(/\D/g, ``);
    },

    createIcon: (className) => {
      let icon = document.createElement(`i`);
      icon.className = className;

      return icon;
    },

    debounce: (cb) => {
      let lastTimeout = null;

      return () => {
        if (lastTimeout) {
          window.clearTimeout(lastTimeout);
        }
        lastTimeout = window.setTimeout(function () {
          cb();
        }, DEBOUNCE_INTERVAL_IN_MS);
      };
    }
  };
})();