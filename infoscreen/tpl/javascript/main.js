$(document).ready(function(){
    // initialize the loader with the default values for the corresponding screen
    // and load the default values into the html elements
    var screen, 
        peace, 
        last_change, 
        nr_elements,
        update_url_left,
        update_url_right,
        update_url;
    screen = {{ screen }};

    // url which should be called for checking changes
    update_url_left = '{% url screen:update "0" %}';
    update_url_right = '{% url screen:update "1" %}';
    
    if(screen === 0){
        update_url = update_url_left;
    } else {
        update_url = update_url_right;
    }
    
    // get the rest of the data from the update url
    $.getJSON(update_url, function(data){
        update = new Update(screen, data.einsatz, data.letzte_aenderung, data.anzahl);
    });
    
});


