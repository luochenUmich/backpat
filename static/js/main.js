$(document).ready(function(){
    $('.comment-button').click(function(){
        $(this).parent().next('.comment-child').slideToggle();
         return false;
    });

    $('.hide-btn').click(function(){
        if ($(this).text() === "Hide") {
            $(this).text("Show");
        } else if ($(this).text() === "Show"){
            $(this).text("Hide");
        }
    });

    $('#commentModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget); // Button that triggered the modal
      var modal = $(this);
      var recipient = button.data('id'); // Extract info from data-* attributes
      console.log(recipient);
      modal.find(".modal-body input[name='parentCommentID']").val(recipient);
      // you can add more attributes here
  })
});

