// This is the API key for the Google Maps API
$.getScript("https://maps.googleapis.com/maps/api/js?key=" + google_api_key + "&libraries=places")
    .done(function (script, textStatus) {
        google.maps.event.addDomListener(window, "load", initMap)

    })

// This function is used to initialize the map
function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var map = new google.maps.Map(document.getElementById('map-route'), {
        zoom: 7,
        center: { lat: lat_a, lng: long_a }
    });
    directionsDisplay.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsDisplay);

}

// waypoints for the route 
const waypts = [
    {
        location: { lat: lat_c, lng: long_c },
        stopover: true
    },
    {
        location: { lat: lat_d, lng: long_d },
        stopover: true
    }
];

// This function is used to calculate the route and display it on the map 
/**
 * Calculates and displays the route between the origin and destination using the provided directions service and display.
 *
 * @param {google.maps.DirectionsService} directionsService - The directions service to use for calculating the route.
 * @param {google.maps.DirectionsRenderer} directionsDisplay - The directions renderer to use for displaying the route.
 */
function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: origin,
        destination: destination,
        waypoints: waypts,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING,
    }, function (response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);


        } else {

            alert('Directions request failed due to ' + status);
            window.location.assign("/route")
        }
    });
}