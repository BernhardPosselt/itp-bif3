$(document).ready(function() {
    initMap();
});

$(window).onload(function() {
    GUnload();
});

function initMap() {
    var gml, mmap;
    var gxmlopts = {}
    mmap=new GMap2(document.getElementById("map")); 
    geocoder = new GClientGeocoder();
    var adresse = "3161, St. Veit/Gölsen";
    showAddress(adresse);
    gxmlopts["nozoom"]=true;
    gml = new GeoXml("gml", mmap, "{{ STATIC_URL }}kml/Hydranten.kml",gxmlopts);
    gml.parse();
}


function showAddress(address) {
    if (geocoder) {
        geocoder.getLatLng
        (
            address,
            function(point) {
                if (!point) {
                    alert(address + " not found");
                } else {
                    mmap.setCenter(point, 16);
                    var marker = new GMarker(point);
                    mmap.addOverlay(marker);
                }
            }
        );
    }
}