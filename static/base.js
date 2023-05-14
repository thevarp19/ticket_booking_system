$(document).ready(function(){
<<<<<<< HEAD
  $('.item').on('mouseenter', function() {
    $(this).find('.hover').addClass('hover-show');
  });
  $('.item').on('mouseleave', function() {
    $(this).find('.hover').removeClass('hover-show');
  });
  $('#datepicker').datepicker({
            uiLibrary: 'bootstrap5',
            minDate: "today"
        });
});
=======
<<<<<<< HEAD
     $('item').hover(function() {
=======
     $('.item').hover(function() {
>>>>>>> 47576b2c1c44cf0590225f53546feb0b4c6b85ab
         $(".hover").animate({
             opacity: '1',
           }, "slow");
       });
<<<<<<< HEAD
       $('item').mouseout(function() {
=======
       $('.item').mouseout(function() {
>>>>>>> 47576b2c1c44cf0590225f53546feb0b4c6b85ab
         $(".hover").animate({
             opacity: '0',
           });
       });
   });
>>>>>>> origin/kuralay_temp
