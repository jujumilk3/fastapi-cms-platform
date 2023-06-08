# fastapi-cms-platform

## Description

Basic CMS platform built with FastAPI.
No time zone. Every thing handled as UTC.

## Feature list

### alarm

- [ ] CRUD Alarm

### Board

- [x] CRUD Board by admin
- [x] Get board list by admin (all)
- [x] Get board list by user (only published)

### Bookmark

- [ ] CRUD Bookmark
- [ ] Get Bookmarked Contents(Posts, Comments, Replies)

### Comment

- [x] CRUD Comment
- [ ] CRUD Reply: WIP
- [ ] Soft delete
- [ ] Comment list of post: WIP
- [ ] Reply list of comment
- [ ] Soft delete if there is concerned contents like comment, reply, reaction
- [ ] Hard delete if there is no concerned contents

### Follow

- [ ] CRUD Follow
- [ ] Get Followed Users
- [ ] Get Following Users
- [ ] Get Following Boards

### Post

- [x] CRUD Post
- [ ] Soft delete if there is concerned contents like comment, reply, reaction
- [ ] Hard delete if there is no concerned contents

### Reaction

- [x] CRUD Reaction
- [ ] Get Reacted Contents(Posts, Comments, Replies)

### Tag

- [ ] CRUD Tag

### User

- [x] signup
- [ ] ~~nickname duplication check~~
- [x] signin
- [x] change password
- [x] change profile
- [x] issue refresh token and refresh access token
