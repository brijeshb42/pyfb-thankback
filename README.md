# Facebook Birthday wish thankback

This script requires python 'requests' module to be installed.

After installation of requests module:-

* Create an application on [facebook](https://developers.facebook.com/apps)
* Copy and paste the APP ID and APP SECRET from the app page into the script.
* Then from console run `python index.py`
* At first, the script will open a browser window requesting your permission.
* After authorization, copy the access_token variable from the url into the console as asked.
* After entering a valid code, the script will ask you the number pf posts to retrieve.
* Enter the desired number of posts to retrieve.
* After retrieving the posts, you will be asked to enter keywords to match the post messages.
* After you enter the keywords, a list of matches will be displayed and the process of commenting on and liking the posts will start.

The script is very slow as it does individual request for liking and commenting on the posts.