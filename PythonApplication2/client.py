#!/usr/bin/env python

import sys
sys.path.append('./gen-py')

from helloworld import HelloWorld

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
  transport = TSocket.TSocket('localhost', 9090)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = HelloWorld.Client(protocol)
  transport.open()

  print "client - ping"
  print "server - " + client.ping()

  print "client - say"
  msg = client.say("Hello!")
  print "server - " + msg

  transport.close()

except Thrift.TException, ex:
  print "%s" % (ex.message)