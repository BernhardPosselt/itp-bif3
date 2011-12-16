/**
 * This is the loader class which handles when something should be loaded
 */
function Loader() {
    
    // url which should be called for checking changes
    this.url = '{% url screen:update %}';
    
    // update interval in seconds
    this.update_interval = 5;
    
    // context, 0 is for peace, 1 for mission
    this.context = 0;
    
    // when the timestamp != the timestamp from the server or the number
    // of elements is not the same as on the server, reload the area which needs
    // reloading
    
    // welcome screen timestamp and number of entries
    this.welcome_screen_lm = 0;
    this.welcome_screen_elem = 0;
    
    // news screen timestamp and number of entries
    this.news_screen_lm = 0;
    this.news_screen_elem = 0; 
    
    // mission screen data timestamp and number of entries
    this.mission_screen_data_lm = 0;
    this.mission_screen_data_elem = 0;
    
    // mission screen map timestamp and number of entries
    this.mission_screen_map_lm = 0;
    this.mission_screen_map_elem = 0;
    
}


/**
 * 
 */
Loader.prototype.update = function () {
    $.getJSON('{% url screen:update %}', function(data){
        alert();
    });
}


