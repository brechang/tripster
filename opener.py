import urllib, urllib2
import cookielib

password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
top_level_url = "http://ec2-54-174-136-103.compute-1.amazonaws.com/"
password_mgr.add_password(None, top_level_url, 'madoka', 'a')

handler = urllib2.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib2.build_opener(handler)

# use the opener to fetch a URL
opener.open("http://ec2-54-174-136-103.compute-1.amazonaws.com/feed")

# Install the opener.
# Now all calls to urllib2.urlopen use our opener.
urllib2.install_opener(opener)

