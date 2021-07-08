$(document).ready(function () {
  //for select tag
  var multipleCancelButton = new Choices("#entityTag", {
    removeItemButton: true,
    maxItemCount: 8,
    searchResultLimit: 8,
    renderChoiceLimit: 8,
  });

  //for individual column search
  // Setup - add a text input to each footer cell
  // $('#displayDemand thead tr').clone(true).appendTo('#displayDemand thead');
  // $('#displayDemand thead tr:eq(1) th').each(function(i) {
  //     var title = $(this).text();
  //     $(this).html('<input type="text" placeholder="Search ' + title + '" />');

  //     $('input', this).on('keyup change', function() {
  //         if (table.column(i).search() !== this.value) {
  //             table
  //                 .column(i)
  //                 .search(this.value)
  //                 .draw();
  //         }
  //     });
  // });

  //for dataTable
  var table = $("#displayDemand").DataTable({
    dom: "Bfrtip",
    // dom: '<"dt-buttons"Bpi>rtp',
    // scrollY: 700,
    // scrollX: true,
    // scroller: true,
    fixedHeader: true,
    //orderCellsTop: true,
    lengthMenu: [96, 192, 188],

    buttons: {
      dom: {
        button: {
          tag: "button",
          className: "",
        },
      },
      buttons: [
        {
          extend: "pageLength",
          className: "btn btn-dark rounded-0",
          text: '<i class="far fa-page"></i> Show Entries',
        },
        {
          extend: "copy",
          className: "btn btn-dark rounded-0",
          text: '<i class="far fa-copy"></i> Copy',
        },
        {
          extend: "excel",
          className: "btn btn-dark rounded-0",
          text: '<i class="far fa-file-excel"></i> Excel',
        },
        {
          extend: "pdf",
          className: "btn btn-dark rounded-0",
          text: '<i class="far fa-file-pdf"></i> Pdf',
        },
        {
          extend: "csv",
          className: "btn btn-dark rounded-0",
          text: '<i class="fas fa-file-csv"></i> CSV',
        },
        {
          extend: "print",
          className: "btn btn-dark rounded-0",
          text: '<i class="fas fa-print"></i> Print',
        },
      ],
    },
  });
});
// setting maximum date to yesterday
var today = new Date();
var dd = today.getDate() - 1;
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
if (dd < 10) {
  dd = "0" + dd;
}
if (mm < 10) {
  mm = "0" + mm;
}
today = yyyy + "-" + mm + "-" + dd;
document.getElementById("endDate").setAttribute("max", today);
document.getElementById("startDate").setAttribute("max", today);

//custom validation before form submit
function validateForm() {
  var selectedEntityList = [];
  var startDate = document.forms["myForm"]["startDate"].value;
  var endDate = document.forms["myForm"]["endDate"].value;
  var errorDiv = document.getElementById("errorDiv");

  //if endDate not slected , set endDate=startDate
  if (endDate == "") {
    document.forms["myForm"]["endDate"].value = startDate;
    endDate = document.forms["myForm"]["endDate"].value;
  }

  //putting all selected entity in selectedEntity List
  for (var option of document.getElementById("entityTag").options) {
    if (option.selected) {
      selectedEntityList.push(option.value);
    }
  }

  if (endDate < startDate) {
    errorDiv.innerHTML =
      "<b> Error !!!! End Date Should Be Greater Than Or Equal To Start Date</b> ";
    return false;
  }

  if (selectedEntityList.length == 0) {
    errorDiv.innerHTML = "<b>Error !!!! Select entity from dropdown </b> ";
    return false;
  }

  //true will submit form ,false will not
  return true;
}
