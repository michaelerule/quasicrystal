#!/usr/bin/env jython
import traceback
try:
    execfile('Edges_debug.py')
except Exception, e:
    traceback.printexc(e)
    print e
