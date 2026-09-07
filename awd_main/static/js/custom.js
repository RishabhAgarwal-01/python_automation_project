
$(document).ready(function(){
    // Wait 5 seconds, then fade out anything with the 'alert' class
    setTimeout(function(){
        $('.alert').fadeOut('slow');
    }, 5000);
});