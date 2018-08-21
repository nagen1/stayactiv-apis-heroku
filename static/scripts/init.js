
$(document).ready(function(){
    //$('.collapse').sideNav();
    $('.parallax').parallax();
    $(".button-collapse").sideNav({menuWidth: 200});
    $('.carousel.carousel-slider').carousel({fullWidth: true});
    // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
    //$('.modal-trigger').leanModal();

    $("#autocomplete").autocomplete({
        minLength: 3,
      source: function( request, response ) {
        $.getJSON($SCRIPT_ROOT + "/autocomplete", {
            search: request.term
        }, function( data ) {
            response( $.map( data.results, function( item ) {
                return {
                    label: item.label,
                    value: item.value
                }
            }));
        });
       },
       select: function (event, ui) {
             $("#name").val(ui.item.label);
             $("#value").val(ui.item.value);
             return false;
       },
       focus: function(event, ui) {
        $("#autocomplete").val(ui.item.label);
        return false; // Prevent the widget from inserting the value.
       }
       //minLength: 3
   });

});