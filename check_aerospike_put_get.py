#!/usr/bin/python

import aerospike
import sys
import time
from optparse import OptionParser


set       = 'nagios-set'



# CONSTANTS FOR RETURN CODES UNDERSTOOD BY NAGIOS
# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

status=OK
performance_data=''
out_str=''

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]



# TEMPLATE FOR READING PARAMETERS FROM COMMANDLINE
parser = OptionParser()
parser.add_option("-H", "--host", dest="host", action="append" , default=[], help="Aerospike host. Use this option multiple time in cluster. Default: 127.0.0.1 ")
parser.add_option("-p", "--port", dest="port", type="int" , default=3000, help="Aerospike port. Default: 3000  ")
parser.add_option("-n", "--namespace", dest="namespace", default="test", help="Aerospike namsepace. Default: test  ")
parser.add_option("-i", "--init", dest="init",  action="store_true" , help="Init records to check - ")
parser.add_option("-r", "--record_numbers", dest="record_numbers",  type="int" , default=30 , help="Number of records to check. Default 30 ")

(options, args) = parser.parse_args()



host_list=[]
if not options.host:
  host_list=[ ( '127.0.0.1', options.port ) ] 
else:
  for h in options.host:
    host_list.append( (h , options.port) )
  

config = {
  "hosts": host_list,
  "policies": {    "timeout": 1000   }
}


# print config 
try:
    client = aerospike.client(config).connect()


    if options.init:
      print "Initializing values for keys: nagios<record_numeber> in nagios-bin bin"
      for i in range(0, options.record_numbers):
         key = ( options.namespace , set , "nagios" + str(i) )
         client.put( key , { 'nagios-bin': 0 } )
         sys.stdout.write(".")
         sys.stdout.flush()
      sys.stdout.write("\n")
      sys.stdout.flush()
    else:

      record=[]
      performance_data=''

      ###
      #  get all records to "record" list
      ### 
      for i in range(0, options.record_numbers):
        key1 = ( options.namespace , set , "nagios" + str(i) )
        (key, metadata) = client.exists(key1)
        if metadata == None:
          out_str=out_str +  "Uknown record, namespace:%s, set:%s, key:%s" % key1
          status=CRITICAL
        else:
          (key, metadata, r) = client.select( key1 , ( 'nagios-bin', )  )
          record.insert(i,r['nagios-bin'])
          time.sleep(0.01)   # delay to not overheat aereospike
          performance_data = performance_data + "record_gen_%i=%i" % ( i , metadata['gen'] )  + "\n"
    #    sys.stdout.write(".")
    #    sys.stdout.flush()
    #  sys.stdout.write("\n")
    #  sys.stdout.flush()

      if status != CRITICAL: # check reckords olny if all of them exist
        ###
        #  calculate avarage
        ### 
        record_median_value=median(record)
        
        for i in range(0, options.record_numbers):
          if record[i] != record_median_value:
            status=CRITICAL
          performance_data = performance_data + "record_avarage_deviation_%i=%f" % ( i , record_median_value - record[i] )  + "\n"


        ###
        #  increment and put back all records
        ### 
        for i in range(0, options.record_numbers):
           key = ( options.namespace , set , "nagios" + str(i) )
           time.sleep(0.01)   # delay to not overheat aereospike
           client.put( key , { 'nagios-bin': record[i] + 1 } )
      # END if all record exist
      if status == OK:
        out_str="OK: " + out_str
      else:
        out_str="CRITICAL: " + out_str

except Exception, eargs:
  out_str = out_str + "UNKNOWN error: {0} ".format(eargs) 
  status=UNKNOWN

if not options.init:
  print out_str
  print '|' + performance_data ,

client.close()
sys.exit(status)


