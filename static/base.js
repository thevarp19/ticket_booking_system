$(document).ready(function(){

  $('.item').on('mouseenter', function() {
    $(this).find('.hover').addClass('hover-show');
  });
  $('.item').on('mouseleave', function() {
    $(this).find('.hover').removeClass('hover-show');
  });
  $('#datepicker').datepicker({
            uiLibrary: 'bootstrap5',
            minDate: '0',
            maxDate: '+15D',
            format: "yyyy-mm-dd"
  })
});


