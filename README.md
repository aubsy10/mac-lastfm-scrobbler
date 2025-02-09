# mac-lastfm-scrobbler

Created using python 3.12.5

Application allowing user's to scrobble albums in their entirety manually as well as individual tracks.
Note that I will continue to be debugging and pushing patches as I work on it and use it over the next
couple of months but for now, the basic functionality works.

Future plans include mkaing it easier for users to download an executable version of this code

I would also like to make it easier for users to input the API keys since I'm not going to
post my own API key. For now, if you'd like to use it create your own API key using Last.fm's
API key system, and at the root of the file create a .env file with parameters API_KEY and
API_SECRET with their respective values.

Finally, note that when you sign in, you'll have 5 seconds to actually click the sign in button
in the open window otherwise it will time out, I plan to fix this in a future patch.
