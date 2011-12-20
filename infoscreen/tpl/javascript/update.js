/**
 * This is the updater class which handles when something should be updated
 * 
 * @param screen: 0 for left screen, 1 for right screen
 * @param mission: 0 for peace, 1 for mission
 * @param last_change: an array with the last changed timestamp of all reloadable elements
 * @param nr_elements: an array with the count of all reloadable elements
 */
function Update(screen, mission, last_change, nr_elements) {
    
    // TODO: implement more than 1 concurrent mission
    
    this.screen = screen;
    this.mission = mission;
    
    // url which should be called for checking changes
    this.update_url_left = '{% url screen:update "0" %}';
    this.update_url_right = '{% url screen:update "1" %}';
    
    // urls to redirect
    this.url_peace_left = '{% url screen:bildschirm_frieden_links %}';
    this.url_peace_right = '{% url screen:bildschirm_frieden_rechts %}';
    this.url_mission_left = '{% url screen:bildschirm_einsatz_links %}';
    this.url_mission_right = '{% url screen:bildschirm_einsatz_rechts %}';
    
    // url for reloads
    this.reload_url = '{% url screen:reload_data %}';
    
    if(screen === 0){
        this.update_url = this.update_url_left;
    } else {
        this.update_url = this.update_url_right;
    }
    
    // ids of each div field we need to load data into
    // peace left
    this.welcome_id = 'willkommen';
    // peace right
    this.news_id = 'news';
    this.utils_id = 'geraete';
    this.vehicles_id = 'fahrzeuge';
    // mission left
    this.vehicle_order_id = 'fahrzeugordnung';
    this.mission_data_id = 'einsatzdaten';
    // mission right
    this.dispo_id = 'dispos';
    // loading element
    this.loading_class = 'loading';
    
    
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
    $.getJSON(self.update_url, function(data){
        // when the timestamp != the timestamp from the server or the number
        // of elements is not the same as on the server, reload the area which needs
        // reloading
        if(!self.last_change.compare(data.letze_aenderung) || 
           !self.nr_elements.compare(data.anzahl)){
            self.screen_update(data.letzte_aenderung, data.anzahl, data.willkommen);
        }

        // check if we have to change the context
        if(self.mission !== data.einsatz){
            self.change_context(self.screen, data.einsatz, data.willkommen);
        }
        
        // check if we have to change the update interval
        if(self.update_interval !== data.update_interval){
            self.change_update_interval(data.update_interval, data.willkommen);
        }
        
        // trigger welcome message update
        if(screen === 0 && data.einsatz === 0){
            self.screen_update([], [], data.willkommen);
        }
    });
}

/**
 * Sets a new update interval
 *
 * @param seconds: The update interval in seconds
 */
Update.prototype.change_update_interval = function (seconds) {
    // check for wrong arguments
    if(seconds < 1){
        seconds = 1;
    }
    this.update_interval = seconds;
    clearTimeout(this.timer);
    this.timer = setTimeout('this.update', this.update_interval*1000);
}

/**
 * Handles the reloadable elements on the page
 *
 * @param last_change: an array with the last changed timestamp of all reloadable elements
 * @param nr_elements: an array with the count of all reloadable elements
 * @param welcome_msg: The welcome message for the leftmost screen, peace
 */
Update.prototype.screen_update = function (last_change, nr_elements, welcome_msg) {
    if(this.screen === 0){
    
        // peace left
        if(mission === 0){
        
            $('#' + this.welcome_id).html(welcome_msg);
            
        // mission left
        } else {
        
            // order: mission, vehicle_order_id
            if( last_change[0]  != this.last_change[0] ||
                nr_elements[0] != this.nr_elements[0]){
                this.reload(this.mission_data_id);
            }
            if( last_change[1]  != this.last_change[1] ||
                nr_elements[1] != this.nr_elements[1]){
                this.reload(this.vehicle_order_id);
            }
            
        }
        
    } else {
    
        // peace right
        if(mission === 0){
        
            // order: news, geraet, fahrzeug
            if( last_change[0]  != this.last_change[0] ||
                nr_elements[0] != this.nr_elements[0]){
                this.reload(this.news_id);
            }
            if( last_change[1]  != this.last_change[1] ||
                nr_elements[1] != this.nr_elements[1]){
                this.reload(this.utils_id);
            }
            if( last_change[2]  != this.last_change[2] ||
                nr_elements[2] != this.nr_elements[2]){
                this.reload(this.vehicles_id);
            }
        
        // mission right
        } else {
        
            // order: einsatz, dispo
            if( last_change[0]  != this.last_change[0] ||
                nr_elements[0] != this.nr_elements[0]){
                // to reload the map we have to do a redirect
                window.location = this.url_mission_right;
            }
            if( last_change[1]  != this.last_change[1] ||
                nr_elements[1] != this.nr_elements[1]){
                this.reload(this.dispo_id);
            }
            
        }
    }
    this.last_change = last_change;
    this.nr_elements = nr_elements;
}

/**
 * Redirects to the new context
 *
 * @param screen: 0 for left screen, 1 for right screen
 * @param mission: 0 for peace, 1 for mission
 */
Update.prototype.change_context = function (screen, mission) {
    if(this.screen === 0){
        if(mission === 0){
            window.location = this.url_peace_left;
        } else {
            window.location = this.url_mission_left;
        }
    } else {
        if(mission === 0){
            window.location = this.url_peace_right;
        } else {
            window.location = this.url_mission_right;
        }
    }
}

/**
 * Redirects to the new context
 *
 * @param screen: 0 for left screen, 1 for right screen
 * @param mission: 0 for peace, 1 for mission
 */
Update.prototype.change_context = function (screen, mission) {
    if(this.screen === 0){
        if(mission === 0){
            window.location = this.url_peace_left;
        } else {
            window.location = this.url_mission_left;
        }
    } else {
        if(mission === 0){
            window.location = this.url_peace_right;
        } else {
            window.location = this.url_mission_right;
        }
    }
}


/**
 * Loads new data into the given field
 *
 * @param div_id: The id of the div element where we want to reload our data
 */
Update.prototype.reload_data = function (div_id) {
    var data = { id: div_id };
    // fade out div element and fade in loading div 
    $('#' + div_id).fadeOut(function(){
        $('#' + this.div_id + ' .' + this.loading_class).fadeIn(function(){
            $('#' + div_id).load(this.reload_url, data, function(){
                $('#' + this.div_id + ' .' + this.loading_class).fadeOut(function(){
                    $('#' + div_id).fadeIn();
                });
            });
        });
    });
    
    
}
