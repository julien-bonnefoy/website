const happyArray = Array(6).fill({ h: 22.5, m: 7.5 });
const neutralArray = Array(6).fill({ h: 7.5, m: 7.5 });
const digitToHands = [[// 0
{ h: 6, m: 15 }, { h: 9, m: 30 }, { h: 6, m: 0 }, { h: 0, m: 30 }, { h: 3, m: 0 }, { h: 0, m: 45 }], [// 1
{ h: 7.5, m: 37.5 }, { h: 6, m: 30 }, { h: 7.5, m: 37.5 }, { h: 6, m: 0 }, { h: 7.5, m: 37.5 }, { h: 0, m: 0 }], [// 2
{ h: 3, m: 15 }, { h: 9, m: 30 }, { h: 6, m: 15 }, { h: 0, m: 45 }, { h: 0, m: 15 }, { h: 9, m: 45 }], [// 3
{ h: 3, m: 15 }, { h: 9, m: 30 }, { h: 3, m: 15 }, { h: 9, m: 0 }, { h: 3, m: 15 }, { h: 9, m: 0 }], [// 4
{ h: 6, m: 30 }, { h: 6, m: 30 }, { h: 0, m: 15 }, { h: 6, m: 0 }, { h: 7.5, m: 37.5 }, { h: 0, m: 0 }], [// 5
{ h: 6, m: 15 }, { h: 9, m: 45 }, { h: 0, m: 15 }, { h: 6, m: 45 }, { h: 3, m: 15 }, { h: 0, m: 45 }], [// 6
{ h: 6, m: 15 }, { h: 9, m: 45 }, { h: 6, m: 0 }, { h: 6, m: 45 }, { h: 0, m: 15 }, { h: 0, m: 45 }], [// 7
{ h: 3, m: 15 }, { h: 6, m: 45 }, { h: 7.5, m: 37.5 }, { h: 6, m: 0 }, { h: 7.5, m: 37.5 }, { h: 0, m: 0 }], [// 8
{ h: 6, m: 15 }, { h: 6, m: 45 }, { h: 0, m: 15 }, { h: 0, m: 45 }, { h: 0, m: 15 }, { h: 0, m: 45 }], [// 9
{ h: 6, m: 15 }, { h: 6, m: 45 }, { h: 3, m: 0 }, { h: 6, m: 0 }, { h: 3, m: 15 }, { h: 0, m: 45 }],
happyArray, neutralArray];
const months = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
const weekdays = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
const clocksIds = [
    "00", "01", "10", "11", "20", "21", "30", "31",
    "02", "03", "12", "13", "22", "23", "32", "33",
    "04", "05", "14", "15", "24", "25", "34", "35"
]
const timeZones = [
    "Pacific/Pago_Pago",
    "Pacific/Honolulu",
    "Pacific/Gambier",
    "America/Anchorage",
    "America/Los_Angeles",
    "Pacific/Galapagos",
    "America/Mexico_City",
    "America/New_York",
    "America/Santiago",
    "America/Noronha",
    "Atlantic/Cape_Verde",
    "Atlantic/Azores",
    "Europe/London",
    "Europe/Paris",
    "Europe/Moscow",
    "Asia/Dubai",
    "Asia/Karachi",
    "Asia/Dhaka",
    "Asia/Jakarta",
    "Asia/Hong_Kong",
    "Asia/Tokyo",
    "Australia/Brisbane",
    "Pacific/Noumea",
    "Pacific/Wallis",
]
const cities = [
 'Pago Pago','Honolulu', 'Gambier', 'Anchorage', 'Los Angeles', 'Galapagos',
 'Mexico City', 'New York', 'Santiago', 'Noronha', 'Cape Verde', 'Azores',
 'London', 'Paris', 'Moscow', 'Dubai', 'Karachi', 'Dhaka',
 'Jakarta', 'Hong Kong', 'Tokyo', 'Brisbane', 'Noumea', 'Wallis'
]



let dico = undefined
let type = undefined
let state = undefined
let interval = undefined
let specialState = undefined
let paris = undefined
let minutes = undefined
let hours = undefined
let values = undefined
let circle = undefined
let ticks = undefined
let zone = undefined
let time = undefined
let id = undefined

let minutesHands = document.querySelectorAll(".minutesHand")
let hoursHands = document.querySelectorAll(".hoursHand")

function convertTZ(date, tzString) {
    return new Date((typeof date === "string" ? new Date(date) : date).toLocaleString("en-US", {timeZone: tzString}));
}

function getDico() {

    let dtz = new Date(Date.now())
    dico = []
    for ( let i = 0; i < timeZones.length; i++) {
        id = clocksIds[i]
        zone = timeZones[i]
        time = convertTZ(dtz, zone)
        dico[id] = { "h": time.getHours(), "m" : time.getMinutes()}
    }
    return dico
}

dico = getDico()

function getDateTime() {
  const currentDataTime = new Date();
  let hh = currentDataTime.getHours();
  let mm = currentDataTime.getMinutes();
  let ss = currentDataTime.getSeconds();
  let ddd = currentDataTime.getDay();
  let dd = currentDataTime.getDate();
  let MM = currentDataTime.getMonth();

  return  {"ddd": ddd, "dd": dd, "MM": MM, "hh": hh, "mm": mm, "ss": ss}
}

function hourToDegrees(hour) {
  return hour * (360 / 12) - 90 ;
}

function minuteToDegrees(minute) {
  return minute * (360 / 60) - 90;
}

function defineLabels() {
  for (let i=0; i < clocksIds.length; i++) {
    let city_name = cities[i]
    let label = document.getElementById("label--" + clocksIds[i]);
    label.innerHTML = city_name
    label.style.opacity = 0;
    $("#label--" + clocksIds[i]).fitText(0.9);
  }
}

function expandTicks(clock) {
  let ticks = clock.querySelectorAll(".tick-radius")
  ticks.forEach(tick => {
    const min = parseInt(tick.dataset.minute);
    if ( min % 5 === 0)  {
      tick.classList.add("bold");
    } else if ( min === 0 ) {
      tick.classList.add("bold");
    }
    const degrees = min * 360 / 60;
    tick.style.transform = `rotate(${degrees}deg)`
  })
}

function showTicks(clock, delay) {
  let ticks = clock.querySelectorAll(".tick-radius")
  ticks.forEach(function(tick) {
    tick.style.opacity = 1
    tick.style.setProperty("transition-delay", delay)
  })
}

function showHands(clock, delay) {
  let hands = clock.querySelectorAll(".hand")
  hands.forEach(function(hand) {
    hand.style.opacity = 1
    hand.style.setProperty("transition-delay", delay)
  })
}
function showPegs(clock, delay) {
  let pegs = clock.querySelectorAll(".center-peg")
  pegs.forEach(function(peg) {
    peg.style.opacity = 1
    peg.style.setProperty("transition-delay", delay)
  })
}

function hideLabels() {
  let labels = document.querySelectorAll(".label")
  labels.forEach( function (label) {
    label.style.opacity = 0
    label.style.setProperty("transition-delay", "0s")
  })
}

function showLabels() {
  let labels = document.querySelectorAll(".label")
  labels.forEach(function(label) {
    label.style.opacity = 1
  })
}

function showClocks() {
  for (let i=0; i < clocksIds.length; i++) {
    let delay = (i*0.25).toString() + "s"
    let clock = document.getElementById("clock--" + clocksIds[i]);
    let label = document.getElementById("label--" + clocksIds[i]);
    setTimeout(function() {
;     expandTicks(clock, delay)
      showHands(clock, delay)
      showPegs(clock, delay)
      label.style.opacity = 1
      label.style.setProperty("transition-delay", delay)
    }, 250)
  }
}

function setHands(clock_id, hours, minutes, type) {
  // clock css variables
  let clock = document.getElementById('clock--' + clock_id);
  clock.style.setProperty('--' + type + '-hours', hourToDegrees(hours) + 'deg');
  clock.style.setProperty('--' + type + '-minutes', minuteToDegrees(minutes) + 'deg');
}

function localHands() {
  let dtz = new Date(Date.now())
  dico = getDico()
  for ( let i=0; i < clocksIds.length; i++ ) {
    let clockId = clocksIds[i];
    minutes = dico[clockId]["m"]
    hours = dico[clockId]["h"]
    // clock css variables
    setHands(clockId, hours, minutes, "local")
  }
}

function globalHands(specialState) {
  type = "special"
  if ( specialState === happyArray) {
    values = Array(4).fill(11)
  } else if ( specialState === neutralArray )  {
    values = Array(4).fill(12)
  } else { // i.e. "HH:MM"
    values = [specialState.charAt(0), specialState.charAt(1), specialState.charAt(3), specialState.charAt(4)]
  }
  for (let id = 0; id < 4; id++ ) {
    for (let x = 0; x < 6; x++) {
      let clockId = id.toString() + x.toString()
      setHands( clockId, digitToHands[values[id]][x].h, digitToHands[values[id]][x].m, type);
    }
  }
  hideLabels();
  animateHands();
  setTimeout( function () {
    specialListener();
  }, 15000);
}

function animateHands() {
  clearAnimations()
 ;   // animate hours Hand
  hoursHands.forEach(function (mnh) {
    mnh.style.setProperty("animation", "15s ease-in-out 0s normal forwards specialHours")
  })
  minutesHands.forEach(function (hrh) {
    hrh.style.setProperty("animation", "15s ease-in-out 0s normal forwards specialMinutes")
  })
  setTimeout ( function  () {
    localHands();
  }, 7500)
  setTimeout ( function  () {
      showLabels();
    clearAnimations();
  }, 15000)
}

function clearAnimations() {
  minutesHands.forEach( function (mnh) {
    mnh.style.setProperty("animation", "");
  })
  hoursHands.forEach( function (hrh) {
    hrh.style.setProperty("animation", "");
  })
}

function stopInterval() {
  clearInterval(interval)
}

function specialListener() {
  interval = setInterval( function () {
    triggerListener();
    let timer = new Date(Date.now() + 5000);
    specialState = timer.toTimeString().slice(0,5);
    if ( specialState !== state ) {
      state = specialState
      stopInterval();
      globalHands(specialState);
    }
  }, 1000)
}

function triggerListener() {
  document.querySelector('.trigger--left').addEventListener('click', function () {
    globalHands(happyArray);
  });
  document.querySelector('.trigger--right').addEventListener('click', function () {
    globalHands(neutralArray);
  });
  window.addEventListener('keydown', function (e) {
    if (e.key === "h") {
      globalHands(happyArray);
    }
    if (e.key === "n") {
      globalHands(neutralArray);
    }
  });
}

function appendParis() {
  paris = document.getElementById('clock--23')
  let redHand = document.createElement("div")
  redHand.className = "hand secondsHand"
  paris.appendChild(redHand)
  setInterval(function() {
    let cdt = new Date(Date.now())
    let seconds = cdt.getSeconds();
    let angle = seconds * 360 / 60;
    redHand.style.transform = `rotate(${angle}deg)`
  })
}

function startClock() {
  defineLabels(dico);
  localHands();
  showClocks();
  setTimeout(function() {
    appendParis();
    specialListener();
  }, 7000);
}

startClock();