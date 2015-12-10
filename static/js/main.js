$(document).ready(function(){
    $('.comment-button').click(function(){
        $(this).parent().next('.comment-child').slideToggle();
         return false;
    });

    $('.hide-btn').click(function(){
        if ($(this).text() === "Hide Replies") {
            $(this).text("Show Replies");
			$(this).siblings('.media.collapse').slideToggle();
        } else if ($(this).text() === "Show Replies"){
            $(this).text("Hide Replies");
			$(this).siblings('.media.collapse').slideToggle();
        }
    });

    $('#commentModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget); // Button that triggered the modal
      var modal = $(this);
      var recipient = button.data('id'); // Extract info from data-* attributes
      modal.find(".modal-body input[name='parentCommentID']").val(recipient);
      // you can add more attributes here
  });
  
  $('#reportModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget); // Button that triggered the modal
      var modal = $(this);
      var recipient = button.data('id'); // Extract info from data-* attributes
      modal.find(".modal-body input[name='commentid']").val(recipient);
      // you can add more attributes here
  });
  
  $('#categoryDropDownPostCreate.dropdown-menu li').click(function() {

		var $target = $( this );
	 
		$target.closest( '.dropdown' )
		  .find( '[data-bind="label"]' ).text( $target.text() )
			 .end()
		  .children( '.dropdown-toggle' ).dropdown( 'toggle' );
		  
		$('#categoryDropdownValue').val($target.val());
		
	   return false;
	 
	});
});

