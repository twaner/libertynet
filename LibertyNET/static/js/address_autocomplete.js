
// Uses address form, using the autocomplete feature
// of the Google Places API to help users fill in the information.
var placeSearch, autocomplete;
var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'long_name',
    postal_code: 'short_name'
};
var myAddress = ["id_address", "id_state", "id_zip_code", "id_city_name"];
function initialize() {
// Create the autocomplete object, restricting the search
// to geographical location types.
autocomplete = new google.maps.places.Autocomplete(
/** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
{ types: ['geocode'] });
// When the user selects an address from the dropdown,
// populate the address fields in the form.
google.maps.event.addListener(autocomplete, 'place_changed', function() {
    fillInAddress();
    });
}
// The START and END in square brackets define a snippet for our documentation:
// [START region_fillform]
function fillInAddress() {
// Get the place details from the autocomplete object.
var place = autocomplete.getPlace();
// Get each component of the address from the place details
// and fill the corresponding field on the form.
var g_Addy = new Array()
var q = 0;
for (var i = 0; i < place.address_components.length; i++) {
    var addressType = place.address_components[i].types[0];
    if (componentForm[addressType]) {
        var val = place.address_components[i][componentForm[addressType]];
        g_Addy[q] = val;
        q++;
    }
}
document.getElementById("id_address").value = g_Addy[0] + ' ' + g_Addy[1];
document.getElementById("id_zip_code").value = g_Addy[4];

if (document.getElementById("id_city_name")){
    document.getElementById("id_city_name").value = g_Addy[2];
} else {
    document.getElementById("id_city").value = g_Addy[2];
}

// Handle State <select> options
var state_worker = document.getElementById("id_state");
for (var i = 0; i < state_worker.options.length; i++) {
    if (state_worker.options[i].value == g_Addy[3]) {
        state_worker.selectedIndex = i;
        state_worker.onChange();
        window.alert(state_worker.selectedIndex);
        }
    }
}

// [END region_fillform]
// [START region_geolocation]
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
        var geolocation = new google.maps.LatLng(
        position.coords.latitude, position.coords.longitude);
        autocomplete.setBounds(new google.maps.LatLngBounds(geolocation,
        geolocation));
        });
    }
}
// [END region_geolocation]
