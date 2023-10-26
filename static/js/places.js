// Get the base country from the html
$.getScript(
    "https://maps.googleapis.com/maps/api/js?key=" +
    google_api_key +
    "&libraries=places"
).done(function (script, textStatus) {
    google.maps.event.addDomListener(window, "load", initAutoComplete);
});

// Initialize the autocomplete
let autocomplete;

// Function to initialize the autocomplete
function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("id-google-address"),
        {
            types: ["address"],
            componentRestrictions: { country: [base_country.toLowerCase()] },
        }
    );

    autocomplete.addListener("place_changed", onPlaceChanged);
}

// Function to get the place details from the autocomplete
function onPlaceChanged() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();

    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById("id-google-address").value;

    // Get the latitude and longitude from the address
    geocoder.geocode({ address: address }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            $("#id_longitude").val(longitude);
            $("#id_latitude").val(latitude);
        }
    });

    // If the place has no geometry, ask the user to enter the address
    if (!place.geometry) {
        document.getElementById("id-google-address").placeholder =
            "*Begin typing address";
    }

    // If the place has a geometry, store the address components in the form fields
    else {
        for (var i = 0; i < place.address_components.length; i++) {
            for (var j = 0; j < place.address_components[i].types.length; j++) {
                if (place.address_components[i].types[j] == "street_number") {
                    var num = place.address_components[i].long_name;
                }
                if (place.address_components[i].types[j] == "route") {
                    var addy = place.address_components[i].long_name;
                }
                if (place.address_components[i].types[j] == "postal_town") {
                    $("#id_town").val(place.address_components[i].long_name);
                }
                if (
                    place.address_components[i].types[j] == "administrative_area_level_2"
                ) {
                    $("#id_county").val(place.address_components[i].long_name);
                }
                if (place.address_components[i].types[j] == "country") {
                    $("#id_country").val(place.address_components[i].long_name);
                }

                if (place.address_components[i].types[j] == "postal_code") {
                    $("#id_post_code").val(place.address_components[i].long_name);
                }
            }
        }
        $("#id_address").val(num + " " + addy);

        // find all hidden inputs & ignore csrf token
        var x = $("input:hidden");
        for (let i = 0; i < x.length; i++) {
            if (x[i].name != "csrfmiddlewaretoken") x[i].type = "text";
            x.eq(x).attr("class", "hidden-el");
        }

        // fade in the completed form
        $(".hidden-el").fadeIn();
        $("#profile-btn").removeAttr("disabled");
    }
}
