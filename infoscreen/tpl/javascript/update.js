/**
 * This is the updater class which handles when something should be updated
 * 
 * @param screen: 0 for left screen, 1 for right screen
 * @param mission: 0 for peace, 1 for mission
 * @param last_change: an array with the last changed timestamp of all reloadable elements
 * @param nr_elements: an array with the count of all reloadable elements
 */
function Update(screen, mission) {
    this.screen = screen;
    this.mission = mission;
    
    // default values, do not change these
    this.screen_view_change_interval = -1;
    this.screen_view = -1;
    this.current_mission = -1;
    this.running_missions = [];
    
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
    this.url_update_dispos = '{% url screen:update_dispos %}';
    
    // ids of each div field we need to load data into
    this.welcome_id = 'willkommen';
    this.news_id = 'news';
    this.utils_id = 'geraete';
    this.vehicles_id = 'fahrzeuge';
    this.vehicle_order_id = 'fahrzeugordnung';
    this.mission_data_id = 'einsatzdaten';
    this.dispos_id = 'dispos';
    this.stats_id = 'stats';

    // ids of the mission div
    this.street_id = 'street';
    this.housenr_id = 'housenr';
    this.stairnr_id = 'stairnr';
    this.doornr_id = 'doornr';
    this.zip_id = 'zip';
    this.place_id = 'place';
    this.notes_id = 'notes';
    this.object_id = 'object';
    this.classification_id = 'classification';
    this.alarmnr = 'alarmnr';
    this.notifier = 'notifier';
        
    // run initial reloads
    this.update();
    
    // set update interval in seconds
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
        
        // currently running missions, if < 0 then we have the first load of 
        // the page, so set the current mission to the first one
        if(self.running_missions < 0 && this.mission){
            self.screen_view = 0;
            self.current_mission = data.running_missions[0];
        }
        self.running_missions = data.running_missions;
        
        // run website reloads
        self.screen_update(); 
           
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
    $('#' + this.news_id).load(this.url_update_news);
    $('#' + this.vehicles_id).load(this.url_update_vehicles);
    $('#' + this.utils_id).load(this.url_update_utils);
}

/**
 * Reloads and sets all elements on the mission left screen
 */
Update.prototype.screen_mission_left_update = function(){
    var data = { missionid: this.current_mission };
    $.getJSON(self.url_update_mission, data, function(data){
        $('#' + this.street_id).html(data.street);
        $('#' + this.housenr_id).html(data.housenr);
        $('#' + this.stairnr_id).html(data.stairnr);
        $('#' + this.doornr_id).html(data.doornr);
        $('#' + this.zip_id).html(data.zip);
        $('#' + this.place_id).html(data.place);
        $('#' + this.notes_id).html(data.notes);
        $('#' + this.object_id).html(data.object);
        $('#' + this.classification_id).html(data.classification);
        $('#' + this.alarmnr).html(data.alarmnr);
        $('#' + this.notifier).html(data.notifier);
    }   
    $('#' + this.vehicle_order_id).load(this.url_update_vehicle_order, data);
}

/**
 * Reloads and sets all elements on the mission right screen
 */
Update.prototype.screen_mission_right_update = function(){
    // FIXME: map reloading?
    var data = { missionid: this.current_mission };
    $('#' + this.dispos_id).load(this.url_update_dispos, data);
}


/**
 * Changes between different views on the page, either multiple missions or
 * the news screen
 */
Update.prototype.screen_view_change = function(){
    if(this.mission === 0){
        switch(this.screen_view){
            case 0:
                $('#' + this.news_id).fadeToggle(function(){
                    $('#' + this.stats_id).fadeToggle();
                });
                this.screen_view = 1;
                break;
            case 1:
                $('#' + this.stats_id).fadeToggle(function(){
                    $('#' + this.news_id).fadeToggle();
                });
                this.screen_view = 0;
                break;
            default:
                this.screen_view = 0;
                break;
        }
    } else {
        this.screen_view += 1;
        this.screen_view %= this.running_missions.length;
        this.current_mission = this.running_missions[this.screen_view];
    }
}

