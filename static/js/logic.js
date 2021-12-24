//  F U N C T I O N S

// Random number generator between min and max
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}

// Function to prepopulate questionnaire from a random participant in DB
function survey_prefill() {
  // Objects that will use d3 to get responses from Postgres DB
  const allResponses = d3.json("/questionnaireDB");

  // Query the Postgres DB and put responses into responseData
  allResponses.then(function(responseData) {
    var recordNumber = getRandomInt(0, responseData.length);
    randomParticipant = responseData[recordNumber];

    console.log(`Record: ${recordNumber} identifes as ${randomParticipant['INTROVERT_EXTROVERT']}`);

    // Use only the questions columns, ignore other columns
    const regex = new RegExp('Q.*A');

    // Add all responses from the randomParticipant
    for (let qNumber in randomParticipant) {
      let numberResponse = randomParticipant[qNumber];
      if (regex.test(qNumber)) {
        // console.log(`d3.select(#${qNumber}${numberResponse}).attr("checked", "")`);
        d3.select(`#${qNumber}${numberResponse}`).attr("checked", "");
      };
    }; // End randomParticipant loop

  }); // End allResponses read

}; // End function survey_prefill()


// main function to initialize the questionnaire
function init() {

  // Objects that will use d3 to get questionslist from Postgres DB
  const allQuestions = d3.json("/questionslistDB");

  // Query the Postgres DB and put questionslist into myData
  allQuestions.then(function(myData) {
   
    for (let i = 0; i < myData.length; i++) {
      questionText = Object.values(myData[i])[0];
      questionNum  = Object.values(myData[i])[1];
      // console.log(`${questionNum} : ${questionText} : index ${i}`);

      // Add the question and options to the questionnaire HTML
      d3.select(".qform").append("div")
                         .attr("class", `qseparator ${questionNum}`);
      d3.select(`.${questionNum}`).append("p");
      d3.select(`.${questionNum}`).append("p")
                           .text(`${questionNum}: ${questionText}`);
      
      for (let j = 1; j < 6; j++) {
        // The correct label text has to be displayed
        if (j == 1) inputText = "- Disagree"
        else if (j == 2) inputText = "- Slightly disagree"
        else if (j == 3) inputText = "- Neutral "
        else if (j == 4) inputText = "- Slightly agree"
        else inputText = "- Agree";

        d3.select(`.${questionNum}`).append("input")
                             .attr("type", "radio")
                             .attr("id", `${questionNum}A${j}`)
                             .attr("name", `${questionNum}A`)
                             .attr("value", j);
        d3.select(`.${questionNum}`).append("label")
                             .attr("for", `${questionNum}A${j}`)
                             .text(inputText);

        // Pre-select all questions to neutral
        if (j == 3) d3.select(`#${questionNum}A${j}`).attr("checked", "");
      } // End for j loop

      d3.select(`${questionNum}`).append("br"); 

    }; // End for i loop

    // Add survey submission button at end of questionnaire
    d3.select(".qform").append("div")
                          .attr("id", "submitbutton")
                        .append("button")
                          .attr("type", "submit")
                          .attr("id", "submit")
                          .text("Submit Questionnaire");
    
    // Populate questionnaire with a random participant responses from DB
    // survey_prefill();

  }); // end of d3.json()

}; // end of function init()

// Call the initialize function (the last line in this code)
init();