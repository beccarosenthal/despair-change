"use strict";

console.log('in register.js')
function validateForm() {

    console.log("in validate form!");
    return true;
    let email = document.querySelector("#email").value;
    if (email === "") {
        alert("Email must be filled out.");
        return false;
    }

    let fname = document.querySelector("#fname").value;
    if (fname === "") {
        alert("First name must be filled out.");
        return false;
    }

    let lname = document.querySelector("#lname").value;
    if (lname === "") {
        alert("Last name must be filled out.");
        return false;
    }

    // todo make sure they need to have a password at all
    let password = document.querySelector("#password").value;
    if (password === "") {
        alert("You must enter a password");
        return false;
    }
    let password_validate = document.querySelector("#password_validate").value;
    if (password != password_validate) {
        alert("Passwords must match.");
        return false;
    }

    let state = document.querySelector("#state").value;
    if (state === "Select a State") {
        alert("Please select a state.");
        return false;
    }

    let phone = document.querySelector("#phone").value;
    //if no phone number submitted, totally fine
    //elif phone filled out in improper format,
    if (phone !== "") {
        if (phoneNumberCheck(phone) == false) {
        alert("Format your phone number as xxxxxxxxxx or leave the field blank.");
        return false;
    }
}

    let zipcode = document.querySelector("#zipcode").value;
    if (zipcode !== "") {
        if (zipcodeCheck(zipcode) == false) {
            alert("Zipcode should be 5 digits or left blank");
            return false;
    }
}
    return true;
}

  let phoneFormat = /^\d{10}$/
function phoneNumberCheck(inputtxt) {
  //XXXXXXXXXX
  if(inputtxt.match(phoneFormat)) {
    console.log("phone number good")
    return true;


  }
  else {
    console.log("phone number bad")
    return false;
  }
}

function zipcodeCheck(inputtxt) {
    // ddddd
  let zipcodeFormat = /^\d{5}$/;
  if(inputtxt.match(zipcodeFormat)) {
    return true;
  }
  else {
    return false;
  }
}

//validate the form when the register button is clicked
$("#submit-button").on('click', submitForm)

function submitForm(evt) {

    if (validateForm() == true) {
        $("#register").submit();
    }
    else {
        alert("please fill out the form correctly.")
    }
}
