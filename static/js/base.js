"use strict";

$(document).ready(function() {

// To make the modal window pop up

$('#donationModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget); // Button that triggered the modal
  var recipient = button.data('whatever'); // Extract info from data-* attributes
  console.log(recipient);
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this);
  // console.log("i'm here...");
});

$.getJSON("https://bootswatch.com/api/3.json", function (data) {
  var themes = data.themes;
  var select = $("select");
  select.show();
  $(".alert").toggleClass("alert-info alert-success");
  $(".alert h4").text("Success!");

  themes.forEach(function(value, index){
    select.append($("<option />")
          .val(index)
          .text(value.name));
  });

  select.change(function(){
    var theme = themes[$(this).val()];
    $("link").attr("href", theme.css);
    $("h1").text(theme.name);
  }).change();

}, "json").fail(function(){
    $(".alert").toggleClass("alert-info alert-danger");
    $(".alert h4").text("Failure!");
});

//version from before to copy referral link to clipboard
function copyReferralLink() {
  var copyText = document.getElementById("referralLink");
  console.log("Referral link: " + copyText )
  copyText.select();
  document.execCommand("Copy");
alert("URL Copied! Send your friend the link to amplify your impact." + copyText.value);
}

$('.glyphicon-chevron-left, .glyphicon-chevron-right').click(function () {
  console.log('clicked a button...maybe')
})

});
// copy referral link to clipboard - my tinkering with it and adding print statements
// function copyReferralLink() {
//   var copyText = document.getElementById("referralLink");
//   copyText.select();
//   console.log(copyText + " before .value")
//   copyText = copyText.value
//   console.log(copyText + " after .value")
//   console.log(copyText.value)
//   document.execCommand("Copy", false, copyText.value);
//   alert("Send the link on your clipboard to a friend so they can give a dollar to amplify your impact. " + copyText.value);
// }

// check this out https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand

