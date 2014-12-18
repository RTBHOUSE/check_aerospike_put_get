check_aerospike_put_get
=======================

Nagios plugin that gets and put data to aerospike to assess potential data loss after node failures.


<pre>
Usage: check_aerospike_put_get.py [options]

Options:
  -h, --help            show this help message and exit
  -H HOST, --host=HOST  Aerospike host. Use this option multiple time in
                        cluster. Default: 127.0.0.1
  -p PORT, --port=PORT  Aerospike port. Default: 3000
  -n NAMESPACE, --namespace=NAMESPACE
                        Aerospike namsepace. Default: test
  -i, --init            Init records to check -
  -r RECORD_NUMBERS, --record_numbers=RECORD_NUMBERS
                        Number of records to check. Default 30
</pre>


Prerequisites
--------------
Plugin require python aerospike library to work ( http://www.aerospike.com/docs/client/python/install/ ) 



Initializing
--------------
Command:

```shell
./check_aerospike_put_get.py  -H node1 -H node2 -r20 -n test -i
```

Will create "nagios-set" set in namsepace "test": and put 20 records witch value=0.


Check
--------------

```shell
./check_aerospike_put_get.py  -H node1.creativecdn.net -H node1.creativecdn.net -r20 -n test
```

Each time this command is executed it reads all 20 records from aerospike, checks them, increments by one and writes back. If some of the records are unavailable or value of some the records
is different from all values median plugin will return CRITICAL to nagios. Performance data can be used to assess how much data were affected.



How performacne data look like:
<pre>
./check_aerospike_put_get.py  -H node1 -H node2 -r20 -n test
OK: 
|record_gen_0=4302
record_gen_1=4302
record_gen_2=4302
record_gen_3=4302
record_gen_4=4302
record_gen_5=4302
record_gen_6=4302
record_gen_7=4302
record_gen_8=4302
record_gen_9=4302
record_gen_10=4302
record_gen_11=4302
record_gen_12=4302
record_gen_13=4302
record_gen_14=4302
record_gen_15=4302
record_gen_16=4302
record_gen_17=4302
record_gen_18=4302
record_gen_19=4302
record_avarage_deviation_0=0.000000
record_avarage_deviation_1=0.000000
record_avarage_deviation_2=0.000000
record_avarage_deviation_3=0.000000
record_avarage_deviation_4=0.000000
record_avarage_deviation_5=0.000000
record_avarage_deviation_6=0.000000
record_avarage_deviation_7=0.000000
record_avarage_deviation_8=0.000000
record_avarage_deviation_9=0.000000
record_avarage_deviation_10=0.000000
record_avarage_deviation_11=0.000000
record_avarage_deviation_12=0.000000
record_avarage_deviation_13=0.000000
record_avarage_deviation_14=0.000000
record_avarage_deviation_15=0.000000
record_avarage_deviation_16=0.000000
record_avarage_deviation_17=0.000000
record_avarage_deviation_18=0.000000
record_avarage_deviation_19=0.000000
</code>




