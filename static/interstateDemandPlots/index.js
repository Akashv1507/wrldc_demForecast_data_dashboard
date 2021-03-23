//For multi select options
$(document).ready(function() {

    var multipleEntityTag = new Choices('#entityTag', {
        removeItemButton: true,
        maxItemCount: 8,
        searchResultLimit: 8,
        renderChoiceLimit: 8
    });

})


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
document.getElementById("endDate").setAttribute("max", today);
document.getElementById("startDate").setAttribute("max", today);


//custom validation before form submit
function validateForm() {

    var selectedEntityList = [];
    var startDate = document.forms["myForm"]["startDate"].value;
    var endDate = document.forms["myForm"]["endDate"].value;
    var errorDiv = document.getElementById("errorDiv");
    //this wont work because page is refreshed and we dont have form input
    // var modelNameDiv = document.getElementById("modelNameDiv");
    // var modelNames = document.getElementsByName('modelName');
    // var modelName;
    // for (var i = 0; i < modelNames.length; i++) {
    //     if (modelNames[i].checked) {
    //         modelName = modelNames[i].value;
    //         modelName = modelName.toUpperCase();
    //     }
    // }
    // outputRes = `Showing ${modelName} plots between ${startDate} and ${endDate}`
    // console.log(outputRes)
    //if endDate not slected , set endDate=startDate
    if (endDate == "") {
        document.forms["myForm"]["endDate"].value = startDate;
        endDate = document.forms["myForm"]["endDate"].value;
    }

    //putting all selected entity in selectedEntity List
    for (var option of document.getElementById('entityTag').options) {
        if (option.selected) { selectedEntityList.push(option.value); }
    }

    if (endDate < startDate) {
        errorDiv.innerHTML = "<b> Error !!!! End Date Should Be Greater Than Or Equal To Start Date</b> ";
        return false;
    }

    if (selectedEntityList.length == 0) {
        errorDiv.innerHTML = "<b>Error !!!! Select entity from dropdown </b> ";
        return false;
    }

    //true will submit form false will not
    return true;

}

window.onload = (error) => {
    for (let entityInd = 0; entityInd < plotData.length; entityInd++) {
        let traceData = [];
        const layout = {
            title: {
                text: plotData[entityInd].title,
                font: {
                    size: 20
                }
            },
            // plot_bgcolor:"black",
            // paper_bgcolor:"#FFF3",
            showlegend: true,
            legend: {
                "orientation": "h",
                y: -0.2,
                font: {
                    family: 'sans-serif',
                    size: 15,
                }
            },

            autosize: true,
            height: 600,
            width: 1500,
            xaxis: {
                showgrid: false,
                zeroline: true,
                showspikes: true,
                spikethickness: 1,
                showline: true,
                titlefont: { color: '#000', size: 22 },
                tickfont: { color: '#000', size: 15 },
                // tickmode: "linear",
                // tick0: startTime,
                // dtick: 15 * 60 * 1000,
                automargin: true,
                tickangle: 283

            },
            yaxis: {
                title: 'MW ',
                showgrid: true,
                zeroline: true,
                showspikes: true,
                spikethickness: 1,
                showline: true,
                titlefont: { color: '#000' },
                tickfont: { color: '#000', size: 18 },
                tickformat: "digits",
            }
        }
        for (let traceInd = 0; traceInd < plotData[entityInd].traces.length; traceInd++) {
            var trace = {
                x: plotData[entityInd].traces[traceInd].xVals,
                y: plotData[entityInd].traces[traceInd].yVals,
                mode: 'lines',
                name: plotData[entityInd].traces[traceInd].traceName,
                type: 'scatter',
                line: {
                    width: 5
                },
                hovertemplate: '(%{x}' + ', %{y:.0f}Mw)'
            };
            traceData.push(trace);
        }
        Plotly.newPlot(plotData[entityInd].divName, traceData, layout);
    }

}