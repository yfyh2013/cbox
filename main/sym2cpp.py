#!/usr/bin/env python2
import sys
from struct import pack
sys.path.extend( [ '../lib', '../liba', '../libc' ] )

from spgrp import *
import spgrp_gens


if len( sys.argv ) < 2:
    print "Usage: sym2cpp.py [fname]"
    exit( 1 )

f = open( sys.argv[ 1 ], 'w' )

N = sum( map( lambda n: len( SpGrp.subs( n ) ), xrange( 1, 231 ) ) )
f.write( pack( 'i', N ) )
#f.close()
#exit( 0 )

for n in xrange( 1, 231 ):
    for ns in SpGrp.subs( n ):
        s = SpGrp( n, ns )
        ops = s.full()
        print 'saving -->', s, len( ops )

        symb = s.mydata['symb'].strip()

        ## ????  why i can't use 'i30si' ????
        f.write( pack( 'i'  , n * 100 + ns ) )   ## write seed, symbol, count of ops
        f.write( pack( '30s', symb         ) )
        f.write( pack( 'i'  , len( ops )   ) )
        for m,v in ops:
            f.write( pack( 'ddddddddd', m[ 0 ][ 0 ], m[ 0 ][ 1 ], m[ 0 ][ 2 ], m[ 1 ][ 0 ], m[ 1 ][ 1 ], m[ 1 ][ 2 ], m[ 2 ][ 0 ], m[ 2 ][ 1 ], m[ 2 ][ 2 ] ) )
            f.write( pack( 'ddd', v.x, v.y, v.z ) )

f.close()
