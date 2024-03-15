// Example JavaScript to capture form submissions and send them to the Google Sheet

document.addEventListener("DOMContentLoaded", function () {
  var origin = window.location.origin;
  var form = document.getElementById("aiipe-send-email");
  var emailInput = document.getElementById("email");
  var submitButton = document.getElementById("submit-button");
  var url =
    "https://script.google.com/macros/s/AKfycbzCBIItAIBevM-IhnTIUEyltdSFowjTd7Cd3ONdtl63i_JfoK-vzO8s2qvJXLSJ9AS4/exec";

  if (form && emailInput && submitButton) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      // Change the button text to show loading dots
      submitButton.innerHTML = "Joining...";

      // Construct the json form data
      var formData = new FormData(form);
      var object = {};
      formData.forEach(function (value, key) {
        object[key] = value;
      });

      // json data
      var json = JSON.stringify(object);
      object.origin = origin;

      // google analytics
      gtag("set", "user_data", {
        email: object.email,
      });

      // Disable the input and the button
      emailInput.disabled = true;
      submitButton.disabled = true;

      // Post the data to the Google Apps Script endpoint
      // Check if the browser supports Fetch API
      if (window.fetch) {
        // Fetch request options
        var requestOptions = {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `email=${object.email}&origin=${origin}`, // Assuming 'json' is defined elsewhere
        };

        console.log("requestOptions", requestOptions);

        // Perform the fetch request
        fetch(url, requestOptions)
          .then(function (response) {
            console.log("response", response);
            // Check if the request was successful
            if (response.ok) {
              // Redirect to the thank-you page
              window.location.href = "thank-you";
            } else {
              // Handle errors
              throw new Error("Network response was not ok.");
            }
          })
          .catch(function (error) {
            // Handle errors
            alert(
              "There was a problem with your submission. Please try again."
            );
            console.error("Error:", error);
          });
      } else {
        // Fallback for browsers that do not support Fetch API
        // Use XMLHttpRequest or other fallback method here
        // Create a new XMLHttpRequest object
        var xhr = new XMLHttpRequest();

        // Define the request method, URL, and async flag
        xhr.open("POST", url, true);

        // Set the request header
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("Aii-Origin", origin); // Include origin in a custom header

        // Define the onload event handler
        xhr.onload = function () {
          // Check if the request was successful (status code 200)
          if (xhr.status === 200) {
            // Redirect to the thank-you page
            window.location.href = "thank-you";
          } else {
            // Handle errors
            alert(
              "There was a problem with your submission. Please try again."
            );
            console.error("Error:", xhr.statusText);
          }
        };

        // Define the onerror event handler
        xhr.onerror = function () {
          // Handle errors
          alert("There was a problem with your submission. Please try again.");
          console.error("Error:", xhr.statusText);
        };

        // Send the JSON data in the request body
        xhr.send(json); // Assuming 'json' is defined elsewhere
      }
    });
  }
});
