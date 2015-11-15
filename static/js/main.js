// This function adds a comment to the target container
function createComment(targetContainer, commentId, userName, commentContent){
	commentHtml = 
	"<div class='row comment' id='comment{{commentid}}'><div class='row commentHeader'><div class='col-sm-8'>\
	<span id='username'>"+userName+"</span> - <span id='date'>"+date+"</span></div></div>\
	<div class='row'><div class='col-sm-12' id='comment-content'>"+commentContent+"</div>\
	</div><div class='comment-child'></div></div>";
	$(targetContainer).append(commentHtml);
}

//This function appends a post to the target container
function createPost(targetContainer, title, date, desc){
	postHtml =
	"<div class='row post' postid={{postid}}> \
		<div class='row postHeader'>\
		<div id='title' class='col-sm-8'>"+title+"\
		</div>\
		<div class='col-sm-1 openButton'>Open\
		</div>\
		<div class='col-sm-1 hideButton'>Hide\
		</div>\
		<div class='col-sm-2 dateInfo'>"+date+"</div></div><div class='row'>\
		<div class='col-sm-12 postDesc'>"+desc+"</div></div></div>";
		$(targetContainer).append(postHtml);
}

//Too add: Meshing of the sql database needed to add these to a page