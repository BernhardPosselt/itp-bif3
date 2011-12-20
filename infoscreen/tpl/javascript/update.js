/**
 * This is the updater class which handles when something should be updated
 * 
 * @param screen: 0 for left screen, 1 for right screen
 * @param mission: 0 for peace, 1 for mission
 * @param last_change: an array with the last changed timestamp of all reloadable elements
 * @param nr_elements: an array with the count of all reloadable elements
 */
function Update(screen, mission) {
    
    // TODO: implement more than 1 concurrent mission
    
    this.screen = screen;
    this.mission = mission;
    
    // url which should be called for checking changes
    this.url_update = '{% url screen:update %}';
    
    // urls to redirect
    this.url_peace_left = '{% url screen:bildschirm_frieden_links %}';
    this.url_peace_right = '{% url screen:bildschirm_frieden_rechts %}';
    this.url_mission_left = '{% url screen:bildschirm_einsatz_links %}';
    this.url_mission_right = '{% url screen:bildschirm_einsatz_rechts %}';
    
    // urls for reloads
    this.url_update_welcome = '{% url screen:update_welcome %}';
    this.url_update_news = '{% url screen:update_news %}';
    this.url_update_vehicles = '{% url screen:update_vehicles %}';
    this.url_update_utils = '{% url screen:update_utils %}';
    this.url_update_vehicle_order = '{% url screen:update_vehicle_order %}';
    this.url_update_mission = '{% url screen:update_mission %}';
    this.url_running_mission = '{% url screen:running_missions %}';
    
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
    
    // run initial reloads
    this.update();
    
    // set update interval in seconds
    this.screen_view_change_interval = -1;
    this.update_interval = 7;
    this.update_timer = setTimeout('this.update', this.update_interval*1000);

}

/**
 * Periodically checks the server for updates
 */
Update.prototype.update = function () {
    var self = this;
    $.getJSON(self.url_update, function(data){
    
        // check if we have to change the context
        if(self.mission !== data.mission){
            self.change_context(self.screen, data.mission);
        }
        
        // check if we have to change the update interval
        if(self.screen_view_change_interval !== data.update_interval ||
           self.screen_view_change_interval < 0){
            self.set_screen_view_change_interval(data.update_interval);
        }
    
        // run website reloads
        this.screen_update(); 
           
    });
}

/**
 * Sets a new screen change interval. We need screen changes for changing between
 * News, Vehicles and Utils or when multiple missions are running
 *
 * @param seconds: The screen change interval in seconds
 */
Update.prototype.set_screen_view_change_interval = function (seconds) {
    // check for too low update interval
    if(seconds < 3){
        seconds = 3;
    }
    this.screen_view_change_interval = seconds;
    if(this.screen_timer){
        clearTimeout(this.screen_timer);
    }
    this.screen_timer = setTimeout('this.screen_view_change', this.screen_view_change_interval*1000);
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
 * Reloads all elements on the screen 
 */
Update.prototype.screen_update = function () {
    if(this.screen === 0){
        if(mission === 0){
            this.screen_peace_left_update();
        } else {
            this.screen_mission_left_update();            
        }
    } else {
        if(mission === 0){
            this.screen_peace_right_update();
        } else {
            this.screen_mission_right_update();
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
 * Reloads and sets all elements on the peace left screen
 */
Update.prototype.screen_peace_left_update = function(){
    $.getJSON(self.url_peace_left, function(data){
        $('#' + this.welcome_id).html(data.welcome_msg);
    }
}

/**
 * Reloads and sets all elements on the peace right screen
 */
Update.prototype.screen_peace_right_update = function(){
    $.getJSON(self.url_peace_right, function(data){
        $('#' + this.welcome_id).html(data.welcome_msg);
    }
}

/**
 * Reloads and sets all elements on the mission left screen
 */
Update.prototype.screen_mission_left_update = function(){
    $.getJSON(self.url_mission_left, function(data){
        $('#' + this.welcome_id).html(data.welcome_msg);
    }
}


/**
 * Reloads and sets all elements on the peace left screen
 */
Update.prototype.screen_mission_right_update = function(){
    $.getJSON(self.url_mission_right, function(data){
        $('#' + this.welcome_id).html(data.welcome_msg);
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
