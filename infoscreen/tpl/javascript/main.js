$(document).ready(function(){
    // initialize the loader with the default values for the corresponding screen
    // and load the default values into the html elements
    var screen, 
        peace, 
        last_change, 
        nr_elements;
    screen = {{ screen }}
    peace = {{ peace }}
    loader = new Loader(screen, peace, last_change, nr_elements);
});


