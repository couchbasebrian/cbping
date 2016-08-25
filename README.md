# cbping
Basic python script to help automate simple network sanity checking

Usage:

    pip install requests
    
    git clone https://github.com/couchbasebrian/cbping.git
    
    cd cbping
    
    python cbping.py -H <host> -P <port> -u <username> -p <password> [-c] [-s] [-rc]
    
    An example for a simgle node test would be:
    
        python cbping.py -H 172.23.99.170 -P 8091 -u Administrator -p password -s
    
    or for a cluster wide check:
    
        python cbping.py -H 172.23.99.170 -P 8091 -u Administrator -p password -c
        
    or for a cluster wide check and check if there is an XDCR cluster. If so, check conectivity to there too:
    
        python cbping.py -H 172.23.99.170 -P 8091 -u Administrator -p password -c -rc
    

Please specify the host and port of a node in an established cluster, not an uninitialized node showing the setup wizard.  Usually port will be 8091.

Sample output:
    
    I will connect to: http://172.23.99.170:8091/pools/default and run some tests.
    This node says that there are 2 nodes in the cluster.
    
    Cluster Node                   Node Status     Node CB version               
    ------------                   -----------     ---------------               
    172.23.99.170:8091             healthy         4.1.1-5914-enterprise         
    172.23.99.171:8091             healthy         4.1.1-5914-enterprise         
    
    Hostname             Port       Result                                   Elapsed Time*
    --------             ----       ------                                   ------------
    172.23.99.171        8091       SUCCESS                                  107.0
    172.23.99.171        8092       SUCCESS                                  111.0
    172.23.99.171        8093       SUCCESS                                  106.0
    172.23.99.171        8094       [Errno 61] Connection refused            162.0
    172.23.99.171        9100       SUCCESS                                  120.0
    172.23.99.171        9102       SUCCESS                                  120.0
    172.23.99.171        9103       [Errno 61] Connection refused            163.0
    172.23.99.171        9104       [Errno 61] Connection refused            167.0
    172.23.99.171        9105       [Errno 61] Connection refused            181.0
    172.23.99.171        9998       [Errno 61] Connection refused            169.0
    172.23.99.171        9999       SUCCESS                                  146.0
    172.23.99.171        11207      SUCCESS                                  106.0
    172.23.99.171        11209      SUCCESS                                  109.0
    172.23.99.171        11210      SUCCESS                                  103.0
    172.23.99.171        11211      SUCCESS                                  132.0
    172.23.99.171        11214      SUCCESS                                  107.0
    172.23.99.171        11215      [Errno 61] Connection refused            144.0
    172.23.99.171        18091      SUCCESS                                  182.0
    172.23.99.171        18092      SUCCESS                                  116.0
    172.23.99.171        18093      SUCCESS                                  111.0
    172.23.99.171        4369       SUCCESS                                  108.0
    172.23.99.171        21100      SUCCESS                                  118.0             
    *Elapsed time is in microseconds.
    
    ---------- Remote Clusters ----------
    
    I will get the info from: http://172.23.99.170:8091/pools/default/remoteClusters?uuid=12495008e3e9b644d42acbb90963688c
    
    deleted    hostname                  name                 uri                                               
    -------    --------                  ----                 ---                                               
    False      172.23.99.172:8091        XDCRReceiver411      /pools/default/remoteClusters/XDCRReceiver411     
    
    Hostname             Port       Result                                   Elapsed Time*        
    --------             ----       ------                                   ------------        
    172.23.99.172        8091       SUCCESS                                  145.0            
    172.23.99.172        8092       SUCCESS                                  133.0            
    172.23.99.172        8093       SUCCESS                                  135.0            
    172.23.99.172        11209      SUCCESS                                  13.0             
    172.23.99.172        11210      SUCCESS                                  128.0            
    172.23.99.172        11211      SUCCESS                                  143.0            
    172.23.99.172        80         [Errno 61] Connection refused            192.0            
    172.23.99.172        8080       [Errno 61] Connection refused            178.0            
    *Elapsed time is in microseconds.
    
    -------------- Buckets --------------
    
    I will get bucket info from: http://172.23.99.170:8091/pools/default/buckets
    
    Bucket Name          itemCount  Bucket Type    
    -----------          ---------  -----------    
    BUCKETNAME           1004       membase        
    
    Goodbye
    
