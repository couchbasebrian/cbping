# cbping
Basic python script to help automate simple network sanity checking
    
    
    $ python cbping.py 172.23.99.170 8091
    I will connect to: http://172.23.99.170:8091/pools/default and run some tests.
    I was able to connect and get a response
    The name of the node I connected to is: default
    This node says that there are 2 nodes in the cluster.
                          hostname          status                        version
                172.23.99.170:8091         healthy          4.1.1-5914-enterprise
                172.23.99.171:8091         healthy          4.1.1-5914-enterprise
    I will now check each of these nodes:
    Working on host: 172.23.99.170
          port                                   result         elapsed time
          8091                                  SUCCESS             0.000104
         11210                                  SUCCESS              0.00014
         11211                                  SUCCESS             0.000139
          8092                                  SUCCESS             0.000138
          8093                                  SUCCESS             0.000138
            80            [Errno 61] Connection refused             0.000167
          8080            [Errno 61] Connection refused             0.000166
    Working on host: 172.23.99.171
          port                                   result         elapsed time
          8091                                  SUCCESS             0.000147
         11210                                  SUCCESS             0.000143
         11211                                  SUCCESS             0.000161
          8092                                  SUCCESS              0.00014
          8093                                  SUCCESS              0.00014
            80            [Errno 61] Connection refused             0.000214
          8080            [Errno 61] Connection refused             0.000179
    Goodbye
    
    
