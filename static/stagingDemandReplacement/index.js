// setting maximum date to yesterday
var today = new Date();
var dd = today.getDate() - 1;
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
if (dd < 10) {
    dd = '0' + dd
}
if (mm < 10) {
    mm = '0' + mm
}
today = yyyy + '-' + mm + '-' + dd;
document.getElementById("sourceDate").setAttribute("max", today);
document.getElementById("targetDate").setAttribute("max", today);


//custom validation before form submit
function validateForm() {

    var targetDate = document.forms["myForm"]["targetDate"].value;
    var byDate = document.forms["myForm"]["sourceDate"].value;
    var errorDiv = document.getElementById("errorDiv");

    if (targetDate == "") {
        errorDiv.innerHTML = "<b> Error !!!! Please select Target Date which is to be replaced. ";
        return false;
    }
    if (byDate == "") {
        errorDiv.innerHTML = "<b> Error !!!! Please select Source Date by which target date is to be replaced  . ";
        return false;
    }


    //true will submit form ,false will not
    return confirm(`Are You Sure want to Replace ${targetDate} by ${byDate}`);



}