# Parking_system

POST : sign-up/

Any user can sign up to our parking management system.

POST: login/
{
    "username": "abc",
    "password":"abc@123",
    "email":"sk@yopmail.com"
}

sign up users can login to use the parking system.

GET: park/

To view all parking

POST: park/

To add a new parking space.


POST: search-parking-spots/

To search nearby parking spaces by giving radius, lat and long

POST: park/<park_pk>/parkingtickets/

To check the parking fee.
