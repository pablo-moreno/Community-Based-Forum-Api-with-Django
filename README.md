# Community Based Forum Api with Django and DRF

NOTE: Use this at your own risk, I've made this only as a demo.

A community based backend api similar to Reddit built on DRF and DJANGO. It has comments, posts, communities and users.

## Users

  - Create an user
  
      > Providing username, email and password it creates an user and automatically logs its IP.
      
  - Get user profile
  
      > Returns the username and email of the user.
      
  
## Communities

  - Create a community
  
      > Create a community by only providing the name, username gets saved automatically.
  
  - "Delete" a community
  
      > "Delete" a community by deactivating it. Not permanently deleting the community.
  
  - Get communities administrated by user
  
      > Returns name and url to communities administrated by user.
  
  - Get communities moderated by user
  
      > Returns name and url to communities moderated by user.
  
  - Perform an admin update
  
      > Modify a community as admin. An admin can modify several options like requesting invitation to access the community,
      edit if it is an adult community, text color, background color, background image, banned users, invited users and       moderators of the community.
  
  - Perform a moderator update
  
      > Modify a community as moderator. A moderator can modify invited users and banned users only.
  
  - Retrieve a community
  
      > Returns name, if invitation is required, if it is an adult community or not, text color, background color and background image.
  
## Posts

  - Retrieve a post list
  
      > Returns title, votes, who posted it, comments_count and a post link. You can filter and search posts in this view as well.
  
  - Retrieve post
  
      > Retrieves title, description, votes, if it is locked, who posted it, url of media and comments_count of a post and if the user "deleted" the post then it returns deleted in the description, title and url.
  
  - Update a post
  
      > Updates title, description, votes, if it is locked and url of a post.
  
  - Create a post
  
      > Creates a post by providing a description, title and/or url.
  
  - "Delete" a post
  
      > "Delete" a post by deactivating it. Not permanently removing it.
  
## Comments

  - Create a comment
  
      > Create a comment by providing the text, if it is a sticky comment and/or a parent comment.
  
  - Retrieve a comment by post
  
      > Returns if comment is sticky, votes, creation date, text and who posted it.
  
  - Delete a comment
  
      > "Delete" a comment by deactivating it. Not permanently removing it.
  
  - Update a comment
  
      > Update body of a comment.
  
  - Retrieve child comments
  
      > Returns the same as when retrieving a comment. It checks the provided parent id.
  
