// Example JavaScript to capture form submissions and send them to the Google Sheet

document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("aiipe-send-email"); // Adjust the ID to match your form
  const emailInput = document.getElementById("email");
  const submitButton = document.getElementById("submit-button");
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // Change the button text to show loading dots
    submitButton.innerText = "Joining...";

    // Construct the form data
    var formData = new FormData(form);
    var object = {};
    formData.forEach(function (value, key) {
      object[key] = value;
    });
    var json = JSON.stringify(object);

    // Disable the input and the button
    emailInput.disabled = true;
    submitButton.disabled = true;

    // Post the data to the Google Apps Script endpoint
    fetch(
      "https://script.google.com/macros/s/AKfycbxg9FQ51NwOz5NIgh6497L-wyByuPmfs6qbR58mu4OX29mQpaR0h5adx3p7FTotwsaO/exec",
      {
        method: "POST",
        // Important: Google Apps Script doPost() expects 'application/x-www-form-urlencoded' content type
        // If using JSON, ensure your GAS code is properly parsing JSON from the request body
        headers: {
          "Content-Type": "application/json", // or 'application/x-www-form-urlencoded' if your GAS is set up for it
        },
        body: json, // Send JSON data
        redirect: "follow", // Optional: Follow redirects
        mode: "no-cors", // This prevents CORS errors
      }
    )
      .then((response) => {
        console.log("response", response);
        // Redirect or show a success message
        window.location.href = "thank-you.html"; // Redirect to a thank-you page
      })
      .catch((error) => {
        alert("There was a problem with your submission. Please try again.");
        console.error("Error:", error);
      });
  });
});
