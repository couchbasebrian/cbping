import json
import requests
import sys
import socket
import time
import pprint
from requests.auth import HTTPBasicAuth
import argparse
parser = argparse.ArgumentParser()

#set up the four arguments that can be passed into the script from the command line.
parser.add_argument('-P', '--port', help='Server port to test.', type=int, required=True)
parser.add_argument('-b', '--bucketname', dest='bucketname', help='The name of the bucket to insert into.', action='store_true')
parser.add_argument('-H', '--hostname', dest='hostname', required=True, help='Host name or IP Address of Couchbase cluster')
parser.add_argument('-u', '--username', dest='username', help='Administrative username.', required=True, default='Administrator')
parser.add_argument('-p', '--password', dest='password', help='Administrative password.', required=True, default='password')
parser.add_argument('-c', '--cluster', dest='clusterMode', help='Check the whole cluster?', default=False, action='store_true')
parser.add_argument('-s', '--single-node', dest='singleNodeMode', help='Only check a single node?', default=False, action='store_true')
parser.add_argument('-rc', '--rcluster', dest='rcluster', help='Check connectivity to XDCR clusters', default=False, action='store_true')

args = parser.parse_args()

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

    print (formatString3 % ("Hostname", "Port", "Result", "Elapsed Time*"))
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
            #get the elapsed time and convert to microseconds
            elapsed = (t2 - t1) * 1000000
            #elapsed = "%.6f" % (t2 - t1)
            sock2.close()

        print (formatString3 % (hostnamepart, eachPortToTest, msg, str(elapsed)))
    print "*Elapsed time is in microseconds."

#Test XDCR cluster if requested to
def checkRemoteCluster():
    print '---------- Remote Clusters (XDCR) ----------'

    remoteClusters = json_dict['remoteClusters']

    # Remote Clusters Requires Authentication otherwise you
    # get a 401 Unauthorized
    remoteClustersUriEnd = remoteClusters['uri']

    remoteClustersUri = 'http://' + args.hostname + ':' + str(args.port) + remoteClustersUriEnd

    print
    print 'I will get the info from: ' + remoteClustersUri

    remoteclusters = requests.get(remoteClustersUri,auth=HTTPBasicAuth(args.username, args.password))

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


#############################################

if (args.clusterMode == True):
    print 'I see that you want cluster mode'

if (args.singleNodeMode == True):
    print 'I see that you want single-node mode'

if ((args.clusterMode == False) and (args.singleNodeMode == False)):
    print 'I will assume that you meant cluster mode'

# Look at the command line arguments

httpstatuscode = 0
poolsdefaulturl = 'http://' + args.hostname + ':' + str(args.port) + '/pools/default'

# Okay lets get started

if (args.singleNodeMode == True):
    singleNodeDict = dict()
    singleNodeDict['hostname'] = args.hostname + ':' + str(args.port)
    testPortsOnNode(singleNodeDict)
    sys.exit(0)

# Cluster mode

print 'I will connect to: ' + poolsdefaulturl + ' and run some tests.'

poolsdefault = requests.get(poolsdefaulturl,auth=HTTPBasicAuth(args.username, args.password))

#httpstatuscode = poolsdefault.status_code

if (poolsdefault.status_code == 200):

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

    print 'This cluster says there are ' + str(len(nodes)) + ' nodes in the cluster.'

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

    #Do we check remote clusters or not?
    if (args.rcluster == True):
        checkRemoteCluster()


    # Move on to the next uri

    print '-------------- Bucket Information --------------'

    poolsdefaultbucketsurl = 'http://' + args.hostname + ':' + str(args.port) + '/pools/default/buckets'

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