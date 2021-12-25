//  F U N C T I O N S

// Random number generator between min and max
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}


// main function to initialize the questionnaire
function init() {
  var loc = window.location.pathname;
  var dir = loc.substring(0, loc.lastIndexOf('/'));
  console.log(dir, loc)

}; // end of function init()

// Call the initialize function (the last line in this code)
init();