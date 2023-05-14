$(document).ready(function(){
     $('item').hover(function() {
         $(".hover").animate({
             opacity: '1',
           }, "slow");
       });
       $('item').mouseout(function() {
         $(".hover").animate({
             opacity: '0',
           });
       });
   });
