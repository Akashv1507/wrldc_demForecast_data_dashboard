$(document).ready(function(){

    var multipleCancelButton = new Choices('#entityTag', {
    removeItemButton: true,
    maxItemCount:8,
    searchResultLimit:8,
    renderChoiceLimit:8
    });
 
   
    });

$(document).ready(function(){

    var multipleCancelButton = new Choices('#revisionNo', {
    removeItemButton: true,
    maxItemCount:18,
    searchResultLimit:18,
    renderChoiceLimit:18
    });
    
    
    });

$(document).ready(function() {
    $('#displayDfm1Forecast').DataTable({
        dom: 'Bfrtip',
        
        lengthMenu: [ 96, 192, 188],
        fixedHeader:{
            header:true
        } ,
        buttons: {
            dom: {
              button: {
                tag: 'button',
                className: ''
              }
            },
            buttons: [  
                {  
                    extend: 'pageLength',  
                    className: 'btn btn-dark rounded-0',  
                    text: '<i class="far fa-page"></i> Show Entries'  
                },
                {  
                    extend: 'copy',  
                    className: 'btn btn-dark rounded-0',  
                    text: '<i class="far fa-copy"></i> Copy'  
                },  
                {  
                    extend: 'excel',  
                    className: 'btn btn-dark rounded-0',  
                    text: '<i class="far fa-file-excel"></i> Excel'  
                },  
                {  
                    extend: 'pdf',  
                    className: 'btn btn-dark rounded-0',  
                    text: '<i class="far fa-file-pdf"></i> Pdf'  
                },  
                {  
                    extend: 'csv',  
                    className: 'btn btn-dark rounded-0',  
                    text: '<i class="fas fa-file-csv"></i> CSV'  
                },  
                {  
                    extend: 'print',  
                    className: 'btn btn-dark rounded-0',  
                    text: '<i class="fas fa-print"></i> Print'  
                }  
            ]
        
    }
    });
    } );


