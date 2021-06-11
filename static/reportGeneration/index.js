// setting maximum date to tommorow
var today = new Date();
var dd = today.getDate() + 1;
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
if (dd < 10) {
  dd = "0" + dd;
}
if (mm < 10) {
  mm = "0" + mm;
}
today = yyyy + "-" + mm + "-" + dd;
document.getElementById("reportDate").setAttribute("max", today);

$("#myForm").submit(function (event) {
  // event.preventDefault();
  var reportDate = document.forms["myForm"]["reportDate"].value;
  var modelName = document.forms["myForm"]["modelName"].value;
  var errorDiv = document.getElementById("errorDiv");

  if (reportDate == "") {
    errorDiv.innerHTML = "<b> Error !!!! Plzz Select Report Date</b> ";
    return false;
  }

  //making api call
  // fetch("http://localhost:8085/createForecastingReport", {
  //   method: "post",
  //   headers: {
  //     mode: "cors",
  //     Accept: "application/json",
  //     "Content-Type": "application/json",
  //   },
  //   body: JSON.stringify({ reportDate: reportDate, modelName: modelName }),
  // })
  //   .then(function (response) {
  //     if (response.ok) {
  //       return response.json();
  //     }
  //     return Promise.reject(response);
  //   })
  //   .then(function (data) {
  //     errorDiv.innerHTML = data.message;
  //   })
  //   .catch(function (error) {
  //     console.warn("Something went wrong.", error);
  //   });
});

//custom validation before form submit
// function validateForm(event) {
//   event.preventDefault();
//   return false;
//   var reportDate = document.forms["myForm"]["reportDate"].value;
//   var errorDiv = document.getElementById("errorDiv");

//   //if endDate not slected , set endDate=startDate
//   if (reportDate == "") {
//     errorDiv.innerHTML = "<b> Error !!!! Plzz Select Report Date</b> ";
//     return false;
//   }

//   //true will submit form ,false will not
//   return true;
// }
