$(document).ready(function(){
    // initialize the loader with the default values for the corresponding screen
    // and load the default values into the html elements
    var screen, 
        peace, 
        last_change, 
        nr_elements;
    screen = {{ screen }};
    mission = {{ mission }};
    update = new Update(screen, mission, last_change, nr_elements);
});


