/**
 * Execute at start
 */
$(document).ready(function() { 
    
    // toggle classes on hover
    $("#content").hover( function(){
        $("#header").removeClass("peace");
        $("#footer").removeClass("peace");
        $("#header").addClass("alarm");
        $("#footer").addClass("alarm");
    });
    
    // toggle classes on hover
    $("#header").hover( function(){
        $("#header").removeClass("alarm");
        $("#footer").removeClass("alarm");
        $("#header").addClass("peace");
        $("#footer").addClass("peace");
    });
    
});
