const dayjs = require('dayjs');
const localizedFormat = require('dayjs/plugin/localizedFormat');
const utc = require('dayjs/plugin/utc');

dayjs.extend(utc)
dayjs.extend(localizedFormat)


// let times = document.querySelectorAll('time');
  
// for(let timeTag of times) {
//   let dt = timeTag.dateTime;
//   let f = dayjs(dt);
//   let g = f.format('LLL');

//   timeTag.innerHTML = g;

// }


const navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

if (navbarBurgers.length > 0) {

  navbarBurgers.forEach( el => {
    el.addEventListener('click', () => {

      const targetId = el.dataset.target;
      const target = document.getElementById(targetId);

      el.classList.toggle('is-active');
      target.classList.toggle('is-active');

    });
  });
}

//help content

const showHelpButton = document.querySelector('.show-help');
const closeHelpButton = document.querySelector('.close-help');
const helpContent = document.querySelector('.instructions');

showHelpButton.addEventListener('click', e => {
  const instructionType = helpContent.dataset.instructions;
  localStorage.removeItem(`${instructionType}-instructions`);
  if (helpContent) {
    helpContent.classList.remove('hide');
  }
});

closeHelpButton.addEventListener('click', e => {
  const instructionType = helpContent.dataset.instructions;
  localStorage.setItem(`${instructionType}-instructions`, 'hide');
  if (helpContent) {
    helpContent.classList.add('hide');
  }
});

//default instructions check
if (helpContent.dataset.instructions == 'register') {
  if (localStorage.getItem('register-instructions')){
    helpContent.classList.add('hide');
  } else {
    helpContent.classList.remove('hide');
  }
}
if (helpContent.dataset.instructions == 'activity') {
  if (localStorage.getItem('activity-instructions')){
    helpContent.classList.add('hide');
  } else {
    helpContent.classList.remove('hide');
  }
}
