/**
 * This is the updater class which handles when something should be updated
 * 
 * @param screen: 0 for left screen, 1 for right screen
 * @param peace: 0 for peace, 1 for mission
 * @param last_change: an array with the last changed timestamp of all reloadable elements
 * @param nr_elements: an array with the count of all reloadable elements
 */
function Update(screen, peace, last_change, nr_elements) {
    // TODO: extend loader
    
    this.screen = screen;
    this.peace = peace;
    
    // url which should be called for checking changes
    this.url_left = '{% url screen:update "0" %}';
    this.url_right = '{% url screen:update "1" %}';
    
    // urls to redirect
    this.url_peace_left = '{% url screen:bildschirm_frieden_links %}';
    this.url_peace_right = '{% url screen:bildschirm_frieden_rechts %}';
    this.url_mission_left = '{% url screen:bildschirm_einsatz_links %}';
    this.url_mission_right = '{% url screen:bildschirm_einsatz_rechts %}';
    
    if(screen === 0){
        this.url = this.url_left;
    } else {
        this.url = this.url_right;
    }
    
    // update interval in seconds
    this.update_interval = 5;
    
    // context, 0 is for peace, 1 for mission
    this.context = 0;
    
    // welcome screen timestamp and number of entries
    this.last_change = last_change;
    this.nr_elements = nr_elements;
    
    // set timer to 
    this.timer = setTimeout('this.update', this.update_interval*1000);
}


/**
 * Periodically checks the server for updates
 */
Update.prototype.update = function () {
    var self = this;
    $.getJSON(self.url, function(data){
        // when the timestamp != the timestamp from the server or the number
        // of elements is not the same as on the server, reload the area which needs
        // reloading
        if(!self.last_change.compare(data.letze_aenderung) || 
           !self.nr_elements.compare(data.anzahl)){
            self.screen_update(data.letzte_aenderung, data.anzahl);
        }

        // check if we have to change the context
        if(self.peace !== data.frieden){
            self.change_context(self.screen, data.frieden);
        }
        
        // check if we have to change the update interval
        if(self.update_interval !== data.update_interval){
            self.change_update_interval(data.update_interval);
        }
    });
}

/**
 * Sets a new update interval
 *
 * @param seconds: The update interval in seconds
 */
Update.prototype.change_update_interval (seconds) {
    clearTimeout(this.timer);
    this.timer = setTimeout('this.update', this.update_interval*1000);
}

/**
 * Handles the reloadable elements on the page
 *
 * @param last_change: an array with the last changed timestamp of all reloadable elements
 * @param nr_elements: an array with the count of all reloadable elements
 */
Update.prototype.change_update_interval (last_change, nr_elements) {
    // TODO: write reloads
    this.last_change = last_change;
    this.nr_elements = nr_elements;
}

/**
 * Redirects to the new context
 *
 * @param screen: 0 for left screen, 1 for right screen
 * @param peace: 0 for peace, 1 for mission
 */
Update.prototype.change_context (screen, peace) {
    if(this.screen === 0){
        if(peace === 0){
            window.location = this.url_peace_left;
        } else {
            window.location = this.url_peace_right;
        }
    } else {
        if(peace === 0){
            window.location ) = this.url_mission_left;
        } else {
            window.location = this.url_mission_right;
        }
    }
}
