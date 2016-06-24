# cbping
# Brian Williams
# June 21, 2016
# Connect to CB and do some basic tests

import json
import requests
import sys
import socket
import time
import pprint
from requests.auth import HTTPBasicAuth

username = 'Administrator'
password = 'couchbase'

pprinter = pprint.PrettyPrinter(indent=4)

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



def testPortsOnNode(nodeWithAHostname):
    currentHostname = nodeWithAHostname['hostname']
    hostnamepart, justThePort = currentHostname.split(":", 1)

    # For reference please see http://developer.couchbase.com/documentation/server/current/install/install-ports.html
    allThePorts = (justThePort, 8092, 8093, 8094, 9100, 9102, 9103, 9104, 9105, 9998, 9999, 11207, 11209, 11210, 11211, 11214, 11215, 18091, 18092, 18093, 4369, 21100)

    formatString3 = "%-20s %-10s %-40s %-20s"

    print (formatString3 % ("hostname", "port", "result", "elapsed time"))
    print (formatString3 % ("--------", "----", "------", "------------"))

    for eachPortToTest in allThePorts:

        eachaddress2 = (hostnamepart, int(eachPortToTest))
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock2.settimeout(10)

        t1 = time.clock()
        t2 = 0
        elapsed = 0
        msg = "-"

        try:
            sock2.connect(eachaddress2)
            msg = "SUCCESS"
        except Exception as e:
            msg = str(e)
        finally:
            t2 = time.clock()
            elapsed = t2 - t1
            sock2.close()

        print (formatString3 % (hostnamepart, eachPortToTest, msg, str(elapsed)))

#############################################

# Check the command line arguments given
argsgiven = len(sys.argv)

clusterMode = False
singleNodeMode = False

for eachArg in sys.argv:
    if (eachArg == '--cluster'):
        clusterMode = True
    if (eachArg == '--single-node'):
        singleNodeMode = True

if argsgiven < 3:
    print 'Usage: cbping.py host port <mode>'
    print 'Where <mode> is either:'
    print '       --cluster     :  Use REST to enumerate all the nodes.  This is the default.'
    print '       --single-node :  Just do tests on this one node specified'
    exit(0)

if (clusterMode == True):
    print 'I see that you want cluster mode'

if (singleNodeMode == True):
    print 'I see that you want single-node mode'

if ((clusterMode == False) and (singleNodeMode == False)):
    print 'I will assume that you meant cluster mode'

# Look at the command line arguments

host = sys.argv[1]
port = sys.argv[2]
httpstatuscode = 0
poolsdefaulturl = 'http://' + host + ':' + port + '/pools/default'

# Okay lets get started

if (singleNodeMode == True):
    singleNodeDict = dict()
    singleNodeDict['hostname'] = host + ':' + port
    testPortsOnNode(singleNodeDict)
    sys.exit(0)

# Cluster mode

print 'I will connect to: ' + poolsdefaulturl + ' and run some tests.'

poolsdefault = requests.get(poolsdefaulturl,auth=HTTPBasicAuth(username, password))

httpstatuscode = poolsdefault.status_code

if (httpstatuscode == 200):

    # print 'I was able to connect and get a response'

    responsejson = poolsdefault.json()

    # Useful for JSON reference
    #for s in sorted(walk_keys(responsejson)):
    #    print s

    responsetext = poolsdefault.text
    json_dict = json.loads(responsetext)

    name =  json_dict['name']

    #print
    #print 'The name of the node I connected to is: ' + name

    nodes = json_dict['nodes']

    print 'This node says that there are ' + str(len(nodes)) + ' nodes in the cluster.'

    #print type(nodes)

    formattingstring = "%-30s %-15s %-30s"

    print
    print (formattingstring % ('Cluster Node','Node Status', 'Node CB version'))
    print (formattingstring % ('------------','-----------', '---------------'))

    for eachNode in nodes:
        print (formattingstring % (eachNode['hostname'] , eachNode['status'], eachNode['version']))

    print
    # print 'I will now check each of these nodes:'

    for eachNode in nodes:
        eachHostname = eachNode['hostname']
        testPortsOnNode(eachNode)

        print

    # Done iterating over the nodes in the first http get

    # Move on to the next uri

    print '---------- Remote Clusters ----------'

    remoteClusters = json_dict['remoteClusters']

    # Remote Clusters Requires Authentication otherwise you
    # get a 401 Unauthorized
    remoteClustersUriEnd = remoteClusters['uri']

    remoteClustersUri = 'http://' + host + ':' + port + remoteClustersUriEnd

    print
    print 'I will get the info from: ' + remoteClustersUri

    remoteclusters = requests.get(remoteClustersUri,auth=HTTPBasicAuth(username, password))

    rchttpstatuscode = remoteclusters.status_code

    if (rchttpstatuscode == 200):
        print

        rcResponsejson = remoteclusters.json()
        # Useful for JSON reference
        #for s in sorted(walk_keys(rcResponsejson)):
        #    print s

        rcformatstring = "%-10s %-25s %-20s %-50s"
        print (rcformatstring % ('deleted', 'hostname', 'name', 'uri'))
        print (rcformatstring % ('-------', '--------', '----', '---'))

        # rcformatstring = "%-10s %-25s %-20s %-50s %-20s %-35s %-20s"
        # print (rcformatstring % ('deleted', 'hostname', 'name', 'uri', 'username', 'uuid', 'validateURI'))
        # print (rcformatstring % ('-------', '--------', '----', '---', '--------', '----', '-----------'))

        rcresponsetext = remoteclusters.text
        rcjson_dict = json.loads(rcresponsetext)

        for eachrc in rcjson_dict:
            # print (rcformatstring % (str(eachrc['deleted']), eachrc['hostname'], eachrc['name'], eachrc['uri'], eachrc['username'], eachrc['uuid'], eachrc['validateURI']))
            print (rcformatstring % (str(eachrc['deleted']), eachrc['hostname'], eachrc['name'], eachrc['uri']))

        print

        for eachrc in rcjson_dict:
            # print 'Working on Remote Cluster host: ' + eachrc['hostname']
            testPortsOnNode(eachrc)
            print

    else:
        print 'RC: Got http error code:' + str(rchttpstatuscode)


    # Move on to the next uri

    print '-------------- Buckets --------------'

    poolsdefaultbucketsurl = 'http://' + host + ':' + port + '/pools/default/buckets'

    print
    print 'I will get bucket info from: ' + poolsdefaultbucketsurl

    poolsdefaultbuckets = requests.get(poolsdefaultbucketsurl)

    pdbhttpstatuscode = poolsdefaultbuckets.status_code

    if (pdbhttpstatuscode == 200):
        # print 'PDB: It worked'

        pdbresponsejson = poolsdefaultbuckets.json()

        # Useful for JSON reference
        #for s in sorted(walk_keys(pdbresponsejson)):
        #    print s

        pdbresponsetext = poolsdefaultbuckets.text
        pdbjson_dict = json.loads(pdbresponsetext)

        print
        rcformatstring = "%-20s %-10s %-15s"
        print (rcformatstring % ('Bucket Name', 'itemCount', 'Bucket Type'))
        print (rcformatstring % ('-----------', '---------', '-----------'))

        for bucket in pdbjson_dict:
            bucketnodes = bucket['nodes']
            basicStats = bucket['basicStats']
            itemCount = basicStats['itemCount']
            bucketType = bucket['bucketType']

            if (bucketType == 'membase'):
                bucketType = 'Couchbase'

            print (rcformatstring % (bucket['name'], itemCount, bucketType))

            for bucketNode in bucketnodes:
                hostname = bucketNode['hostname']
                # print hostname
                replication = bucketNode['replication']
                # print replication


    else:
        print 'PDB: Got http error code:' + str(httpstatuscode)

    # end of section where first http get was successful



else:
    print 'PD: Got http error code:' + str(httpstatuscode)

print
print 'Goodbye'

# EOF