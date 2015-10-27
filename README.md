Desk.com - Digitization Automation
==================================
At ITS we digitize a lot of media and generating streaming tickets can be a hassle. This integration will check the Digitization Group in Desk to see if there is any media that has been digitized, but not yet been resolved. It will make a call to the [Rohan-Search](https://github.com/sdsu-its/rohan-search) server to generate a streaming ticket and send an email to the faculty member who requested the movie.

## Desk Config
This app looks for a group called ```Digitization``` with a filter setup that has all the cases that belong to the ```Digitization``` group.

A custom filed, called ```streaming_url``` is also used to track the public url of the file that has been digitized for them.

## Sample Params
Params are loaded from an environment variable named ```Params```, the contents of which should look something like this:

```
{
  "Desk.com": {
    "site_name": "yoursite",
    "auth_method": "password",
    "username": "john@example.com",
    "password": "this password",
    "client_key": "keys",
    "client_secret": "ReallyLongKey",
    "resource_owner_key": "AlsoAKey",
    "resource_owner_secret": "AlsoAReallyLongKey"
  },
  "Rohan_Search": {
    "url": "https://my-app.herokuapp.com/"
  }
}
```
