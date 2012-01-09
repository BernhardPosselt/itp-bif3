var gml, mmap;
//var gxmlopts = {}
    
window.onload = function() {
    if (GBrowserIsCompatible()) 
    {
        mmap=new GMap2(document.getElementById("map")); 
        geocoder = new GClientGeocoder();
        ort = '{{ ort }}';
        plz = '{{ plz }}';
        strasse = '{{ strasse }}';
        hausnummer = '{{ hausnummer }}';
        if (!ort)
        {
            plz = "3161";
            ort = "St. Veit/Gölsen";
        }
        var adresse = hausnummer + "," + strasse + ", " + plz + "," + ort;
        showAddress(adresse);
       // gxmlopts["nozoom"]=true;
        gml = new GeoXml("gml", mmap, '{{ kml_url }}');
        gml.parse();
    }
}

window.unload = function(){
    GUnload();
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


