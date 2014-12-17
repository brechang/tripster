import time
import urllib, urllib2
import cookielib
import contextlib

cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)
urllib2.install_opener(opener)

login_url = 'http://ec2-54-174-136-103.compute-1.amazonaws.com/'
opener.open(login_url)

try:
    token = [x.value for x in cookies.cookiejar if x.name=='csrftoken'][0]
except IndexError:
    print "no csrftoken"

params = dict(username='madoka', password='a', \
        csrfmiddlewaretoken=token,
        )
encoded_params = urllib.urlencode(params)

start = time.time()
with contextlib.closing(opener.open(login_url, encoded_params)) as f:
    html = f.read()
end = time.time()
print "Logging in took: ", end-start, "seconds"


view_trips_url = "http://ec2-54-174-136-103.compute-1.amazonaws.com/view_trips?csrfmiddlewaretoken=%s" % (token)

start = time.time()
with contextlib.closing(opener.open(view_trips_url, encoded_params)) as f:
    html = f.read()
    print html
end = time.time()

print "Getting madoka's trips took: ", end-start, "seconds"

start = time.time()
req = urllib2.Request(view_trips_url)
resp = urllib2.urlopen(req)
end = time.time()
print "Getting madoka's trips took: ", end - start, "seconds"


