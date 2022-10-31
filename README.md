# Django-React for weather history

This web app contains user registration and login using JSON Web Token while for services it is using an API call on Open Weather Map that retrieve data which is given to user to observe current weather parameters or past 24 hours. CRUD operations to endpoints were tested with Postman as below displayed; roadmap was assigned on Jira (Kanban process), then committed on new GitHub branch, reviewed and approved to merge main branch.

#

## Endpoints tested in POSTMAN

![POST addLocation](./screenshots/DR-31-POST-addLocation.png)

![POST addLocation location already exists](./screenshots/DR-31-POST-addLocation-location-already-exists.png)

![POST addLocation strings with interger not accepted](./screenshots/DR-31-POST-addLocation-strings-with-interger-not-accepted.png)

![POST addLocation wrong unit](./screenshots/DR-31-POST-addLocation-wrong-unit.png)

![GET getLocations](./screenshots/DR-31-GET-getLocations.png)

![GET getLocationById](./screenshots/DR-31-GET-getLocationById.png)

![GET getLocationById-string-id](./screenshots/DR-31-GET-getLocationById-string-id.png)

![GET getLocationById with wrong id](./screenshots/DR-31-GET-getLocationById-wrong-id.png)

![PATCH updateLocation user1](./screenshots/DR-31-PATCH-updateLocation-user1.png)

![PATCH user2 denied partial update to user1](./screenshots/DR-31-PATCH-user2-denied-partial-update-user1.png)

![DELETE-id](./screenshots/DR-31-DELETE-id.png)

![FORECAST-NOW](./screenshots/DR-32-service-to-user_location.png)
