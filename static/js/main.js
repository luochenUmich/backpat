$(document).ready(function(){
    $('.comment-button').click(function(){
        $(this).parent().next('.comment-child').slideToggle();
         return false;
    });
});