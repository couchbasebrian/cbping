# cbping
Basic python script to help automate simple network sanity checking

Usage:

    pip install requests
    
    git clone https://github.com/couchbasebrian/cbping.git
    
    cd cbping
    
    python cbping.py <host> <port>

Usually <port> will be 8081

Sample output:
    
    I will connect to: http://172.23.99.170:8091/pools/default and run some tests.
    This node says that there are 2 nodes in the cluster.
    
    Cluster Node                   Node Status     Node CB version               
    ------------                   -----------     ---------------               
    172.23.99.170:8091             healthy         4.1.1-5914-enterprise         
    172.23.99.171:8091             healthy         4.1.1-5914-enterprise         
    
    hostname             port       result                                   elapsed time        
    --------             ----       ------                                   ------------        
    172.23.99.170        8091       SUCCESS                                  0.0001              
    172.23.99.170        8092       SUCCESS                                  0.000131            
    172.23.99.170        8093       SUCCESS                                  0.000137            
    172.23.99.170        11209      SUCCESS                                  0.000149            
    172.23.99.170        11210      SUCCESS                                  0.000169            
    172.23.99.170        11211      SUCCESS                                  0.000132            
    172.23.99.170        80         [Errno 61] Connection refused            0.000163            
    172.23.99.170        8080       [Errno 61] Connection refused            0.000174            
    
    hostname             port       result                                   elapsed time        
    --------             ----       ------                                   ------------        
    172.23.99.171        8091       SUCCESS                                  0.000156            
    172.23.99.171        8092       SUCCESS                                  0.000131            
    172.23.99.171        8093       SUCCESS                                  0.000134            
    172.23.99.171        11209      SUCCESS                                  0.00013             
    172.23.99.171        11210      SUCCESS                                  0.00013             
    172.23.99.171        11211      SUCCESS                                  0.000137            
    172.23.99.171        80         [Errno 61] Connection refused            0.000162            
    172.23.99.171        8080       [Errno 61] Connection refused            0.00022             
    
    ---------- Remote Clusters ----------
    
    I will get the info from: http://172.23.99.170:8091/pools/default/remoteClusters?uuid=12495008e3e9b644d42acbb90963688c
    
    deleted    hostname                  name                 uri                                               
    -------    --------                  ----                 ---                                               
    False      172.23.99.172:8091        XDCRReceiver411      /pools/default/remoteClusters/XDCRReceiver411     
    
    hostname             port       result                                   elapsed time        
    --------             ----       ------                                   ------------        
    172.23.99.172        8091       SUCCESS                                  0.000145            
    172.23.99.172        8092       SUCCESS                                  0.000133            
    172.23.99.172        8093       SUCCESS                                  0.000135            
    172.23.99.172        11209      SUCCESS                                  0.00013             
    172.23.99.172        11210      SUCCESS                                  0.000128            
    172.23.99.172        11211      SUCCESS                                  0.000143            
    172.23.99.172        80         [Errno 61] Connection refused            0.000192            
    172.23.99.172        8080       [Errno 61] Connection refused            0.000178            
    
    -------------- Buckets --------------
    
    I will get bucket info from: http://172.23.99.170:8091/pools/default/buckets
    
    Bucket Name          itemCount  Bucket Type    
    -----------          ---------  -----------    
    BUCKETNAME           1004       membase        
    
    Goodbye
    
