// This function toggles the directions table on the map page
function DirectionsToggle() {
  const el = $("#dir-toggle");
  const dir_table = $("#dir-table");
  if (dir_table.attr("hidden") == "hidden") {
    dir_table.fadeIn();
    dir_table.removeAttr("hidden");
    el.html(
      'hide <a href="javascript:void(0)" onclick="DirectionsToggle()">here'
    );
  } else {
    dir_table.fadeOut();
    dir_table.attr("hidden", "hidden");
    el.html(
      'click <a href="javascript:void(0)" onclick="DirectionsToggle()">here'
    );
  }
}

// This function is used to show the alert message
function ShowAlert(title, message, type, redirect) {
  if (redirect) {
    toastr[type](message, title, {
      positionClass: "toast-bottom-right",
      closeButton: true,
      progressBar: true,
      newestOnTop: true,
      rtl: $("body").attr("dir") === "rtl" || $("html").attr("dir") === "rtl",
      timeOut: 7500,
      onHidden: function () {
        window.location.assign(redirect);
      },
    });
  } else {
    toastr[type](message, title, {
      positionClass: "toast-bottom-right",
      closeButton: true,
      progressBar: true,
      newestOnTop: true,
      rtl: $("body").attr("dir") === "rtl" || $("html").attr("dir") === "rtl",
      timeOut: 7500,
    });
  }
}

// Function to show the password on the login and signup pages
function showPword() {
  const x = document.getElementsByClassName("password");
  for (let i = 0; i < x.length; i++) {
    if (x[i].type === "password") {
      x[i].type = "text";
    } else {
      x[i].type = "password";
    }
  }
}

let temp_button_text;

// Custom function to show a loading spinner on the submit button
function CustomFormSubmitPost(e) {
  const el = $(e);
  temp_button_text = el.text();
  el.attr("disabled", "disabled")
    .text("")
    .append(
      '<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...'
    );
}

function CustomFormSubmitResponse(e) {
  const el = $(e);
  el.removeAttr("disabled").text(temp_button_text);
}

// This function is used to submit the signup form data and return the response to the user
("use strict");

/**
 * FormControls module handles form submissions and AJAX requests for signup, signin, and user profile forms.
 * @module FormControls
 */
const FormControls = (() => {
  const usersignup = () => {
    const form = $("#signupform");
    form.submit((event) => {
      event.preventDefault();
      CustomFormSubmitPost($("#signupform button[type=submit]"));
      grecaptcha.ready(() => {
        grecaptcha
          .execute(recaptcha_site_key, { action: "/" })
          .then((token) => {
            document.getElementById("id_token").value = token;
            const formdata = form.serialize();
            $.ajax({
              url: form.attr("action"),
              method: form.attr("method"),
              data: formdata,
              success: (json) => {
                CustomFormSubmitResponse($("#signupform button[type=submit]"));
                const redirect = json["result"] === "Success" ? "/" : false;
                ShowAlert(
                  json["result"],
                  json["message"],
                  json["result"].toLowerCase(),
                  redirect
                );
              },
              error: (xhr) => {
                CustomFormSubmitResponse($("#signupform button[type=submit]"));
                ShowAlert(
                  "Error",
                  "There was an error, please try again",
                  "error",
                  false
                );
                console.log(xhr.status + ": " + xhr.responseText);
              },
            });
          });
      });
    });
  };

  const usersignin = () => {
    const form = $("#signinform");
    form.submit((event) => {
      event.preventDefault();
      CustomFormSubmitPost($("#signinform button[type=submit]"));
      const formdata = form.serialize();
      $.ajax({
        url: form.attr("action"),
        method: form.attr("method"),
        data: formdata,
        success: (json) => {
          CustomFormSubmitResponse($("#signinform button[type=submit]"));
          const redirect = json["result"] === "Success" ? "/" : false;
          ShowAlert(
            json["result"],
            json["message"],
            json["result"].toLowerCase(),
            redirect
          );
        },
        error: (xhr) => {
          CustomFormSubmitResponse($("#signinform button[type=submit]"));
          ShowAlert(
            "Error",
            "There was an error, please try again",
            "error",
            false
          );
          console.log(xhr.status + ": " + xhr.responseText);
        },
      });
    });
  };

  const userprofile = () => {
    const form = $("#profileform");
    form.submit((event) => {
      event.preventDefault();
      CustomFormSubmitPost($("#profileform button[type=submit]"));
      const formdata = form.serialize();
      $.ajax({
        url: form.attr("action"),
        method: form.attr("method"),
        data: formdata,
        success: (json) => {
          CustomFormSubmitResponse($("#profileform button[type=submit]"));
          const redirect = json["result"] === "Success" ? "/" : false;
          ShowAlert(
            json["result"],
            json["message"],
            json["result"].toLowerCase(),
            redirect
          );
        },
        error: (xhr) => {
          CustomFormSubmitResponse($("#profileform button[type=submit]"));
          ShowAlert(
            "Error",
            "There was an error, please try again",
            "error",
            false
          );
          console.log(xhr.status + ": " + xhr.responseText);
        },
      });
    });
  };

  return {
    init: () => {
      usersignup();
      usersignin();
      userprofile();
    },
  };
})();

jQuery(document).ready(() => {
  FormControls.init();
});

$(() => {
  // This function gets cookie with a given name
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");
  function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
  function sameOrigin(url) {
    const host = document.location.host;
    const protocol = document.location.protocol;
    const sr_origin = "//" + host;
    const origin = protocol + sr_origin;
    return (
      url == origin ||
      url.slice(0, origin.length + 1) == origin + "/" ||
      url == sr_origin ||
      url.slice(0, sr_origin.length + 1) == sr_origin + "/" ||
      !/^(\/\/|http:|https:).*/.test(url)
    );
  }
  $.ajaxSetup({
    beforeSend: (xhr, settings) => {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });
});
