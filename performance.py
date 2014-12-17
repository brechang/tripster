import time
from urllib2 import *


start = time.time()
req = Request('http://ec2-54-174-136-103.compute-1.amazonaws.com/view_trips?csrfmiddlewaretoken=SzIac0oc9mkROqaDCLxiEJezUI2LelDb')
resp = urlopen(req)
end = time.time()
print "Getting madoka's trips took: ", end - start, "seconds"

