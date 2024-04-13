// Get the base country from the html
$.getScript(
  `https://maps.googleapis.com/maps/api/js?key=${google_api_key}&libraries=places`
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
/**
 * Function that is called when the place is changed in the autocomplete object.
 * It gets the place details from the autocomplete object and stores the address components in the form fields.
 * If the place has no geometry, it asks the user to enter the address.
 * If the place has a geometry, it stores the latitude and longitude in the form fields.
 */
function onPlaceChanged() {
  // Get the place details from the autocomplete object.
  let place = autocomplete.getPlace();

  let geocoder = new google.maps.Geocoder();
  let address = document.getElementById("id-google-address").value;

  // Get the latitude and longitude from the address
  geocoder.geocode({ address: address }, function (results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      let latitude = results[0].geometry.location.lat();
      let longitude = results[0].geometry.location.lng();

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
    let num, addy;
    for (let i = 0; i < place.address_components.length; i++) {
      for (let j = 0; j < place.address_components[i].types.length; j++) {
        if (place.address_components[i].types[j] === "street_number") {
          num = place.address_components[i].long_name;
        }
        if (place.address_components[i].types[j] === "route") {
          addy = place.address_components[i].long_name;
        }
        if (place.address_components[i].types[j] === "postal_town") {
          $("#id_town").val(place.address_components[i].long_name);
        }
        if (
          place.address_components[i].types[j] === "administrative_area_level_2"
        ) {
          $("#id_county").val(place.address_components[i].long_name);
        }
        if (place.address_components[i].types[j] === "country") {
          $("#id_country").val(place.address_components[i].long_name);
        }

        if (place.address_components[i].types[j] === "postal_code") {
          $("#id_post_code").val(place.address_components[i].long_name);
        }
      }
    }
    $("#id_address").val(num + " " + addy);

    // find all hidden inputs & ignore csrf token
    let hiddenInputs = $("input:hidden");
    hiddenInputs.each(function (index, element) {
      if ($(element).attr("name") !== "csrfmiddlewaretoken") {
        $(element).prop("type", "text");
        $(element).addClass("hidden-el");
      }
    });

    // fade in the completed form
    $(".hidden-el").fadeIn();
    $("#profile-btn").removeAttr("disabled");
  }
}
