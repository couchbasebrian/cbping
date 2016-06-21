# cbping
# Brian Williams
# June 21, 2016
# Connect to CB and do some basic tests
# Developed with Python 2.7.8

import json
import requests
import sys
import socket
import time


# This helpful function came from
# http://stackoverflow.com/questions/33489209/print-unique-json-keys-in-dot-notation-using-python
def walk_keys(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.iteritems():
            for r in walk_keys(v, path + "." + k if path else k):
                yield r
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            s = "[" + str(i) + "]"
            for r in walk_keys(v, path + s if path else s):
                yield r
    else:
        yield path


# Check the command line arguments given
argsgiven = len(sys.argv)

if argsgiven != 3:
    print 'Usage: cbping host port'
    exit(0)

host = sys.argv[1]
port = sys.argv[2]
httpstatuscode = 0
poolsdefaulturl = 'http://' + host + ':' + port + '/pools/default'

print 'I will connect to: ' + poolsdefaulturl + ' and run some tests.'

poolsdefault = requests.get(poolsdefaulturl)

httpstatuscode = poolsdefault.status_code

if (httpstatuscode == 200):

    print 'I was able to connect and get a response'

    responsejson = poolsdefault.json()

    # Useful for JSON reference
    #for s in sorted(walk_keys(responsejson)):
    #    print s

    responsetext = poolsdefault.text
    json_dict = json.loads(responsetext)

    name =  json_dict['name']

    print 'The name of the node I connected to is: ' + name

    nodes = json_dict['nodes']

    print 'This node says that there are ' + str(len(nodes)) + ' nodes in the cluster.'

    #print type(nodes)

    formattingstring = "%30s %15s %30s"

    print (formattingstring % ('hostname','status', 'version'))

    for eachnode in nodes:
        print (formattingstring % (eachnode['hostname'] , eachnode['status'], eachnode['version']))

    print 'I will now check each of these nodes:'

    for eachnode in nodes:
        eachHostname = eachnode['hostname']
        lhs, rhs = eachHostname.split(":", 1)
        print 'Working on host: ' + lhs

        allPorts = ( rhs, 11210, 11211, 8092, 8093, 80, 8080)

        formatString2 = "%10s %40s %20s"

        print (formatString2 % ( "port", "result", "elapsed time" ))

        for eachPort in allPorts:

            # print "Trying port " + str(eachPort)

            eachAddress = (lhs, int(eachPort))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)

            t1 = time.clock()
            t2 = 0
            elapsed = 0

            msg = "-"

            try:
                sock.connect(eachAddress)
                msg = "SUCCESS"
            except Exception as e:
                msg = str(e)
            finally:
                t2 = time.clock()
                elapsed = t2 - t1
                sock.close()

            print (formatString2 % ( eachPort, msg, str(elapsed) ) )

else:
    print 'Got http error code:' + str(httpstatuscode)


print 'Goodbye'

# EOF
