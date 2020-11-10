const dayjs = require('dayjs');
const localizedFormat = require('dayjs/plugin/localizedFormat');
const utc = require('dayjs/plugin/utc');


dayjs.extend(utc)
dayjs.extend(localizedFormat)

const h1 = document.querySelector('h1');

let specifiedDate = dayjs(document.querySelector('time').dateTime, 'YYYY-MM-DDTHH:mm:ss')
const specifiedPlatform = parseInt(h1.dataset.platform)
const specifiedActivity = parseInt(h1.dataset.activity)

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

let rc = document.getElementById('register-container');

let registeredHours;
//to deal with :30/:45 offsets
let localMinute = specifiedDate.utc().hour(00).minute(00).local().minute();


let localDayUtcStart = specifiedDate.hour(00).minute(localMinute).utc().format('YYYY-MM-DDTHH:mm');
let localDayUtcEnd = specifiedDate.hour(23).minute(localMinute).utc().format('YYYY-MM-DDTHH:mm');
let rosterUrl = `/hourmarker/${specifiedActivity}/${specifiedPlatform}/${specifiedDate.format('YYYY-MM-DD')}/?start=${localDayUtcStart}Z&end=${localDayUtcEnd}Z`

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
      registeredHours = data;
      buildList()
    });
  }
)


function buildList() {

  baseHours.forEach(bh => {

    let dt = specifiedDate.hour(bh).minute(localMinute);


    if (dt >= activityLive) {
      const hourBlockTemplate = document.querySelector('#hour-block-template');
      const hb = hourBlockTemplate.content.cloneNode(true);
    
      let inputId = 'hb-' + dt.format('YYYY-MM-DDTHH:mm')  
    
      const label = hb.querySelector('.hour-input label');
      label.htmlFor = inputId;
      label.dataset.date = dt.toISOString();
      let labelText = dt.format('LT');
      if ( dt.utc().diff(dt.utc().day(weeklyReset.day).hour(weeklyReset.hour).minute(weeklyReset.minute)) == 0) {
        labelText = `🔁 ${labelText}`;
        hb.querySelector('.hour-block').classList.add('weekly-reset')

      }
      label.innerHTML = labelText
      label.title = dt.utc().format('YYYY-MM-DDTHH:mm');
    
      const checkbox = hb.querySelector('.hour-input input');
      checkbox.id = inputId;
      checkbox.value = dt.format()
      if (dt < activityLive) {
        checkbox.disabled = true;
      }
  
      //set checked status
      const searchdate = dt.utc().format('YYYY-MM-DDTHH:mm:ss') + 'Z'
  
      let match = registeredHours.find((rh) => {
        return rh.marker_datetime === searchdate
      })
      if (match) {
        checkbox.checked = true;
        checkbox.dataset.hmId = match.id;
      }
    
      checkbox.addEventListener('change', (e) => {
        e.target.disabled = true;

        if (e.target.checked) {
          let data = {
            activity: activityId,
            platform: platformId,
            marker_datetime: e.target.value
          }
          fetch('/hourmarker/', {
            method: 'post',
            headers: {
              'Content-type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
          })
          .then(
            function(response) {
              response.json().then(function(data) {
                e.target.dataset.hmId = data.id
                  e.target.disabled = false;
              });
            }
          )
        } else {
          let data = {
            id: parseInt(e.target.dataset.hmId),
            activity: 1,
            marker_datetime: e.target.value
          }
          fetch(`/hourmarker/`, {
            method: 'DELETE',
            headers: {
              'Content-type': 'application/json',
              'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data)
          })
          .then(
            function(response) {
              response.json().then(function(data) {
                e.target.disabled = false;
              });
            }
          )
        }
      })
    
  
      rc.appendChild(hb)
  
    }
  
  
  
  });
}


//tags
const userTagControls = document.querySelectorAll('#user-tag-control input[type=checkbox]');

let userTags = [];

fetch('/tag/user/', {
  method: 'get',
  headers: {
    'Content-type': 'application/json',
    'X-CSRFToken': csrftoken
  }
})
.then(
  function(response) {
    response.json().then(function(data) {
      userTags = data;
      setUpTagControls()
    });
  }
)

function setUpTagControls() {

  userTagControls.forEach((cb) => {


    let match = userTags.find((ut) =>  {
      return ut.id == cb.value
    })
    if (match) {
      cb.checked = true;
    }
    cb.addEventListener('change', (e) => {
      cb.disabled = true;
      if (cb.checked) {
        let data = {
          id: cb.value
        };
        fetch('/tag/user/', {
          method: 'post',
          headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify(data)
        })
        .then(
          function(response) {
            response.json().then(function(data) {
              cb.disabled = false;
            });
          }
        )
      } else {
        let data = {
          id: cb.value
        };
        fetch('/tag/user/', {
          method: 'delete',
          headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify(data)
        })
        .then(
          function(response) {
            response.json().then(function(data) {
              cb.disabled = false;
            });
          }
        )
      }
    })

  });
}

