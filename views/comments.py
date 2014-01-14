def create_comment(response):
	current_user = get_logged_in(response)
	if current_user:
		comment = response.get_field("comment")
		if comment:
			image_id = response.get_field("image_id")
			#try:
			db.create_comment(image_id, current_user.username, comment)
			response.write("Comment successful!")
			#except:
	else:
		response.write("You are not logged in.")

def get_comment(response):
	comment_list = []
	image_id = response.get_field("image_id")
	for comment_id in db.get_image_comments(image_id):
		comment_list.append(get_comment(comment_id))