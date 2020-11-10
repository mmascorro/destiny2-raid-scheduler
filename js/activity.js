const dayjs = require('dayjs');
const localizedFormat = require('dayjs/plugin/localizedFormat');
const utc = require('dayjs/plugin/utc');


dayjs.extend(utc)
dayjs.extend(localizedFormat)

const h1 = document.querySelector('h1');

let specifiedDate = dayjs(document.querySelector('time').dateTime, 'YYYY-MM-DD')

//set up hour grid for display
let baseHours = []

let start = 0;
let end = 23;
let count = end-start+1;

while (count--) {
  baseHours[count] = end--
}

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const activityId = parseInt(h1.dataset.activity)
const platformId = parseInt(h1.dataset.platform)
const activityLive = dayjs(h1.dataset.activityLive);
const weeklyReset = {
  day: 2,
  hour: 17,
  minute: 00 
}

let roster_detail;
//to deal with :30/:45 offsets
let localMinute = specifiedDate.utc().hour(00).minute(00).local().minute();
let localDayUtcStart = specifiedDate.hour(00).minute(localMinute).utc().format('YYYY-MM-DDTHH:mm');
let localDayUtcEnd = specifiedDate.hour(23).minute(localMinute).utc().format('YYYY-MM-DDTHH:mm');
let rosterUrl = `/roster/${activityId}/${platformId}/${specifiedDate.format('YYYY-MM-DD')}?start=${localDayUtcStart}Z&end=${localDayUtcEnd}Z`

fetch(rosterUrl, {
  method: 'get',
  headers: {
    'Content-type': 'application/json',
    'X-CSRFToken': csrftoken
  }
})
.then(
  function(response) {
    response.json().then(function(data) {
      roster_detail = data;
      buildList()
    });
  }
)

const hourList = document.getElementById('hour-list');
const hourListItemTemplate = document.getElementById('hour-list-item-template');

buildList = () => {
  baseHours.forEach(bh => {

    const hourListItemNode = hourListItemTemplate.content.cloneNode(true);
    const hourListItem = hourListItemNode.querySelector('.hour-list-item')

    let currentLocalHour = specifiedDate.hour(bh).minute(localMinute);
    let hliId = `hli-${currentLocalHour.format('HHmm')}`;
    hourListItem.id = hliId;
    
    if ( currentLocalHour >= activityLive) {

      let h2 = hourListItem.querySelector('h2');
      let title = currentLocalHour.format('LT');
      if ( currentLocalHour.utc().diff(currentLocalHour.utc().day(weeklyReset.day).hour(weeklyReset.hour).minute(weeklyReset.minute)) == 0) {
        title += ' (Weekly Reset)';
        h2.classList.add('weekly-reset')
      }
      h2.innerHTML = title;
      h2.title = currentLocalHour.utc().format('YYYY-MM-DDTHH:mm');


      let pingBuilderStart = hourListItem.querySelector('.build-ping');

      pingBuilderStart.addEventListener('click', e => {
        let hli = document.getElementById(hliId);
        let hourCheckboxes = document.querySelectorAll(`#${hliId} input[type=checkbox]:checked`);

        if (hli.classList.contains('ping-builder')) {
          hli.classList.remove('ping-builder');
          hourCheckboxes.forEach(c => {
            c.checked = false;
          })
        } else { 
          hli.classList.add('ping-builder');
        }
      })

      let pingBuilderCopy = hourListItem.querySelector('.copy-users-btn');
      pingBuilderCopy.addEventListener('click', e => {
        
        let hourCheckboxes = document.querySelectorAll(`#${hliId} input[type=checkbox]:checked`);
        let pingList = '';
        hourCheckboxes.forEach((hcb) => {
          pingList += hcb.value + ' ';
        });
        if (hourCheckboxes.length) {
          navigator.clipboard.writeText(pingList).then(function() {
            console.log('copied..')
          });
        }
      })



      let currentLocalHourFormatted = currentLocalHour.format('YYYY-MM-DDTHH:mm')
      let currentUtcHourFormatted = currentLocalHour.utc().format('YYYY-MM-DDTHH:mm')
  
      if (roster_detail[currentUtcHourFormatted]) {
        let ol = hourListItem.querySelector('ol');
    
        roster_detail[currentUtcHourFormatted].forEach((rd) => {
          let li = document.createElement('li');
          let discordAt = `@${rd.user.name}`;
          let pingCheckbox = document.createElement('input');
          pingCheckbox.type = 'checkbox';
          pingCheckbox.value = discordAt;

          let span = document.createElement('span');
          span.classList.add('username');
          span.innerHTML = discordAt;
          span.title = `${discordAt} registered at ${rd.register_on}`;

          li.appendChild(pingCheckbox);
          li.appendChild(span);
          ol.appendChild(li);

          if (rd.user.tags) {
            rd.user.tags.forEach((tag) => {
              let span = document.createElement('span');
              span.classList.add('tag');
              span.classList.add(tag.slug);
              span.classList.add('is-light');
              span.title = tag.description;
              span.innerHTML = tag.name;
              li.appendChild(span);

            });
          }
        });
      } else  {
        hourListItem.classList.add('no-registrations');
      }
      
      //check if item is older than viewer's actual time
      if (currentLocalHour.isBefore(dayjs(), 'hour')) {
        hourListItem.classList.add('before');
      }

      hourList.appendChild(hourListItem);

    }

  

  
  
  });
}

//tags
const tagToggles = document.querySelectorAll('.tag-toggle');

tagToggles.forEach((cb) => {

  cb.addEventListener('change', (e) =>{
    let spans = document.querySelectorAll(`span.${e.target.value}`);
    spans.forEach((tag) => {
      tag.classList.toggle('is-dark');
      tag.classList.toggle('is-light');
    }); 
  })
})