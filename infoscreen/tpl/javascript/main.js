$(document).ready(function(){
    // initialize the loader with the default values for the corresponding screen
    // and load the default values into the html elements
    var update = new Update({{ screen }}, {{ mission|lower }});
});

// extend array object with a compare method
Array.prototype.compareArrays = function(arr) {
    if (this.length != arr.length) return false;
    for (var i = 0; i < arr.length; i++) {
        if (this[i].compareArrays) { //likely nested array
            if (!this[i].compareArrays(arr[i])) return false;
            else continue;
        }
        if (this[i] != arr[i]) return false;
    }
    return true;
}
