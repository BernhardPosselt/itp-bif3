/**
 * This is the updater class which handles when something should be updated
 * 
 * @param screen: 0 for left screen, 1 for right screen
 * @param mission: 0 for peace, 1 for mission
 * @param last_change: an array with the last changed timestamp of all reloadable elements
 * @param nr_elements: an array with the count of all reloadable elements
 */
function Update(screen, mission) {
    // set true when you dont want to develope the design so the screen fade ins
    // wont happen. Developement only!!
    this._developement = false;


    this.screen = screen;
    this.mission = mission;
    
    // default values, do not change these
    this.screen_view_change_interval = -1;
    this.screen_view = -1;
    this.news_view = -1;
    this.current_mission = -1;
    this.current_news = -1;
    this.running_missions = [];
    this.running_news = [];
    
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
    this.url_update_map = '{% url screen:update_map %}';
    this.url_update_title_msg = '{% url screen:update_title_msg %}';
    
    // ids of each div field we need to load data into
    this.welcome_id = 'willkommen';
    this.news_id = 'news';
    this.utils_id = 'geraete';
    this.vehicles_id = 'fahrzeuge';
    this.vehicle_order_id = 'ausrueckeordnung';
    this.mission_data_id = 'einsatzdaten';
    this.dispos_id = 'dispos';
    this.util_stats_id = 'geraete';
    this.vehicle_stats_id = 'fahrzeuge';
    this.map_id = 'karte';
    this.running_missions_id = 'lauf_missionen';
    this.header_id = 'header';
    this.time_id = 'time';

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
    this.alarmnr_id = 'alarmstufe';
    this.notifier_id = 'notifier';
    
    
    // cache variables to check for reloading map
    this.cache_street = '';
    this.cache_housnr = '';
    this.cache_stairnr = '';
    this.cache_zip = '';
    this.cache_place = '';
    this.cache_object = '';
    
    // run initial reloads
    this.update();
    
    // set update interval in seconds
    var self = this;
    this.update_interval = 1;
    this.update_timer = setInterval(function(){
        self.update();
    }, this.update_interval*1000);
}

/**
 * Periodically checks the server for updates
 */
Update.prototype.update = function () {
    var self = this;
    // check for url params
    var getvar = window.location.search;
    var dat;
    if (getvar.length > 0){
        dat = {
            preview: 'true'
        }
    } else {
        dat = {};
    }
    $.getJSON(self.url_update, dat, function(data){

        // check if we have to change the context
        if(self.mission !== data.mission){
            self.change_context(self.screen, data.mission);
        }

        // update time
        self.update_time(data.time);
        
        // check if we have to change the update interval
        if(self.screen_view_change_interval !== data.update_interval ||
           self.screen_view_change_interval < 0){
            self.set_screen_view_change_interval(data.update_interval);
        }
        
        // currently running missions, if < 0 then we have the first load of 
        // the page, so set the current mission to the first one
        if(self.current_mission < 0 && self.mission){
            self.screen_view = 0;
            self.current_mission = data.running_missions[0];
        }
        // if the running missions array is not the same as we got we have to
        // reset the screenview to the first position to keep sync
        if(!self.running_missions.compareArrays(data.running_missions)){
            self.screen_view = 0;
            self.current_mission = data.running_missions[0];    
        }
        
        self.running_missions = data.running_missions;
        self.running_news = data.running_news;
        
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
        clearInterval(this.screen_timer);
    }
    var self = this;
    this.screen_timer = setInterval(function(){
        self.screen_view_change();
    }, self.screen_view_change_interval*1000);
}

/**
 * Redirects to the new context
 *
 * @param screen: 0 for left screen, 1 for right screen
 * @param mission: false for peace, true for mission
 */
Update.prototype.change_context = function (screen, mission) {
    if(this.screen === 0){
        if(mission === false){
            window.location = this.url_peace_left;
        } else {
            window.location = this.url_mission_left;
        }
    } else {
        if(mission === false){
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
        if(this.mission === false){
            this.screen_peace_left_update();
        } else {
            
            this.screen_mission_left_update();            
        }
    } else {
        if(this.mission === false){
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
 * @param mission: false for peace, true for mission
 */
Update.prototype.change_context = function (screen, mission) {
    if(this.screen === 0){
        if(mission === false){
            window.location = this.url_peace_left;
        } else {
            window.location = this.url_mission_left;
        }
    } else {
        if(mission === false){
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
    var self = this;
    this.update_title_msg();
    $.getJSON(this.url_update_welcome, function(data){
        $('#' + self.welcome_id).html(data.welcome_msg);
    });
}

/**
 * Reloads and sets all elements on the peace right screen
 */
Update.prototype.screen_peace_right_update = function(){
    this.update_title_msg();
    var data;
    if(this.news_view < 0 || this.running_news.length <= 0){
        data = { news_id: this.running_news[0] };
    } else {
        data = { news_id: this.current_news };
    }
    
    $('#' + this.news_id).load(this.url_update_news, data);
    $('#' + this.vehicles_id).load(this.url_update_vehicles);
    $('#' + this.utils_id).load(this.url_update_utils);
}

/**
 * Sets the title msg to the standard
 */
Update.prototype.update_title_msg = function(){
    var self = this;
    $.getJSON(this.url_update_title_msg, function(data){
        $('#' + self.classification_id).html(data.title_msg);
    });
}


/**
 * Reloads and sets all elements on the mission left screen
 */
Update.prototype.screen_mission_left_update = function(){
    var data = { mission_id: this.current_mission };
    var self = this;
    $.getJSON(this.url_update_mission, data, function(data){
        $('#' + self.street_id).html(data.street);
        $('#' + self.housenr_id).html(data.housenr);
        $('#' + self.stairnr_id).html(data.stairnr);
        $('#' + self.doornr_id).html(data.doornr);
        $('#' + self.zip_id).html(data.zip);
        $('#' + self.place_id).html(data.place);
        $('#' + self.notes_id).html(data.notes);
        $('#' + self.object_id).html(data.object);
        $('#' + self.classification_id).html(data.classification);
        $('#' + self.alarmnr_id).html(data.alarmnr);
        //$('#' + this.notifier_id).html(data.notifier);
        self.update_alarmnr_color(data.alarmnr);
    });
    $('#' + this.vehicle_order_id).load(this.url_update_vehicle_order, data);
}

/**
 * Reloads and sets all elements on the mission right screen
 */
Update.prototype.screen_mission_right_update = function(){
    var data = { mission_id: this.current_mission };
    var self = this;

    $('#' + this.dispos_id).load(this.url_update_dispos, data);
    $.getJSON(this.url_update_mission, data, function(data){
        
        $('#' + self.classification_id).html(data.classification);
        $('#' + self.alarmnr_id).html(data.alarmnr);        
        var iframe_url = self.url_update_map + "?mission_id=" + data.id;
        var $frame = $('#' + self.map_id + ' iframe');

        // set url for iframe only if the url or data has changed
        if($frame.attr('src') !== iframe_url ||
            self.cache_street !== data.street ||
            self.cache_housenr !== data.housenr ||
            self.cache_stairnr !== data.stairnr ||
            self.cache_zip !== data.zip ||
            self.cache_place !== data.place ||
            self.cache_object !== data.object)
        {    
            // set tmp values and map url for iframe
            $frame.attr('src', iframe_url);
            self.cache_street = data.street;
            self.cache_housenr = data.housenr;
            self.cache_stairnr = data.stairnr;
            self.cache_zip = data.zip;
            self.cache_place = data.place;
            self.cache_object = data.object;
        }
        self.update_running_missions();
        self.update_alarmnr_color(data.alarmnr);
    });
}


/**
 * Changes between different views on the page, either multiple missions or
 * the news screen
 */
Update.prototype.screen_view_change = function(){
    if(!this._developement){
        var self = this;
        if(this.mission === false){
        
            this.screen_view += 1;
            this.screen_view %= 3;
            
            switch(this.screen_view){
                case 0:
                    $('#' + this.news_id).fadeOut(function(){
                        $('#' + self.util_stats_id).fadeIn();
                    });
                    break;
                case 1:
                    $('#' + this.util_stats_id).fadeOut(function(){
                        $('#' + self.vehicle_stats_id).fadeIn();
                        if(self.running_news.length !== 0){
                            self.news_view += 1;
                            self.news_view %= self.running_news.length;
                            self.current_news = self.running_news[self.news_view];
                        }
                    });
                    break;
                default:
                    $('#' + this.vehicle_stats_id).fadeOut(function(){
                        $('#' + self.news_id).fadeIn();
                    });
                    break;
            }

        } else {
            this.screen_view += 1;
            this.screen_view %= this.running_missions.length;
            this.current_mission = this.running_missions[this.screen_view];
        }
    }
}


/**
 * Updates the running missions on the screen to inform the users how many missions
 * are running in paralell
 */
Update.prototype.update_running_missions = function(){
    $('#' + this.running_missions_id).html(this.running_missions.length);
}

/**
 * Updates the current time display
 *
 * @param time: The time we want to set, a string
 */
Update.prototype.update_time = function(time){
    $('#' + this.time_id).html(time);
}

/**
 * Updates the header background to the class for the according alarmnr
 *
 * @param alarmnr: The alarmnr 
 */
Update.prototype.update_alarmnr_color = function(alarmnr){
    switch(alarmnr.charAt(0).toLowerCase()){
        case 'b':
            $('#' + this.header_id).attr('class', 'brand');
            break;
        case 's':
            $('#' + this.header_id).attr('class', 'schadstoff');
            break;
        case 't':
            $('#' + this.header_id).attr('class', 'technisch');
            break;
        default:
            $('#' + this.header_id).attr('class', 'frieden');        
            break;
    }
}
