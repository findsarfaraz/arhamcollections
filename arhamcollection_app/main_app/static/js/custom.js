$('.dropdown-trigger').dropdown(
  {
    alignment:'right',
    hover: true,
    inDuration:300,
    coverTrigger: false
  });

$('select').formSelect();


  $('.carousel.carousel-slider').carousel({
    fullWidth: true,
    indicators: true
  });

autoplay();
function autoplay() {
    $('.carousel.carousel-slider#mainpage').carousel('next');
    setTimeout(autoplay, 4000);
}

function hoverplay() {
    $('.carousel.carousel-slider#photoslide').carousel('next');
    setTimeout(hoverplay, 4000);
}



 $('.sidenav#mobile-demo').sidenav(
 {
 	edge:'right',
 	
 });

  $('.sidenav#mobile-demo1').sidenav(
 {
 	edge:'left',
 	
 });




$('.parallax').parallax();

$("#photoslide").mouseenter(function(event){
  hoverplay() ;
  event.preventDefault();
});


$('.datepicker').pickadate({
format: 'yyyy-mm-dd',
selectMonths: true, // Creates a dropdown to control month
selectYears: 100, // Creates a dropdown of 15 years to control year,
today: 'Today',
clear: 'Clear',
close: 'Ok',
closeOnSelect: false // Close upon selecting a date,
});	








$('.slider').slider();


   

function ShowMessage(data)
  {

  
  if(data.success)
          {
          $('#success').show();
          $('#error').hide();
          $(".success-msg").text("");
          $(".success-msg").append(' <i class="fa fa-check"></i>  ');
          $(".success-msg").append(data.success);
          $(".success-msg").append('<span class="right"><i class="fa fa-times" id="successmsg" onclick="hidemsg(this.id)"></i></span>');
          if (data.redirect)
                {
                
                window.location.href = data.redirect;

                }
          }
  else if (data.error)
          {

          $('#error').show();
          $('#success').hide();
          $(".error-msg").text("");
          $(".error-msg").append(' <i class="fa fa-times-circle"></i> ');
          $(".error-msg").append(data.error);
          $(".error-msg").append('<span class="right"><i class="fa fa-times" id="errormsg" onclick="hidemsg(this.id)"></i></span>');
          }
  }


