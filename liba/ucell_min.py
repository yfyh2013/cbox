from draw_gl import drawgl

from ucell import UCell
from reper import Reper

import reper_coord
import vec_z2o

def to_min( self ):
    rep = self.rep  ## alias
    near = {}

    ext = self * 1  ## extend in all directions by 1

    mps = min( self.pnts.values(), key = lambda l: len( l ) )  ## "minimal points"
                                                               ## this is minimal group of points
    mps = list( mps )  ## convert set() to ordered list()

    #print "minimal points = ", mps

    eqv_dr = set()  ## all possible translations wich translate each point of
                    ## this ucell (self) to extended ucell (ext)

    ## for each pair from mps...
    for i in xrange( len(mps) ):
        for j in xrange( i+1, len(mps) ):
            dr = mps[i] - mps[j]  ## vec to translate
            uct = self + dr       ## translated ucell

            eqv = True  ## translate equiv or not
            for k,vs in uct.pnts.iteritems():
                if not vs.issubset( ext.pnts[ k ] ):  ## some points not intersected with others
                    eqv = False
                    break
            if eqv:
                eqv_dr.add( dr )

    eqv_dr.update( list( rep ) )  ## add vectors from original reper

    #print "possible translations = ", eqv_dr

    ## sort vectors by its lengs
    eqv_dr = list( eqv_dr )
    eqv_dr.sort( key = lambda v: v.vlen() )

    #DEBUG DRAW
    #for v in eqv_dr:
    #    drawgl( v, style="line", color=(1,0,0) )

    ## take first shortest
    v1 = eqv_dr[ 0 ]

    ## take second shorterst wich is not lie on one line with v1
    v1n = v1.norm()
    for v in eqv_dr:
        if not v1n == v.norm():
            #print v1n, v.norm()
            break
    v2 = v

    ## take third shortest wich is not complanar with v1 and v2
    vc = v1.vcross( v2 )
    for v in eqv_dr:
        if vc * v > 0.001:
            break
    v3 = v

    nrep = Reper( v1,v2,v3 ) ## new reper

    #DEBUG DRAW
    #for v in nrep:
    #    drawgl( v, style="line", color=(0,1,0) )

    uc   = UCell( nrep )

    for k,vs in self.pnts.iteritems():
        vsn = set()  ## new basis
        vs_sorted = list( vs )
        vs_sorted.sort( key = lambda v: v.vlen() )  ## nearest to coordinate origin - better
        for v in vs_sorted:
            fbasis = True  ## this is point from basis
            for vv in vsn: ## test with each point in new basis
                dr = vv - v
                #print dr
                dr = nrep.dec2frac( dr )  ## transform vector from point v to vv to fractional coordinates
                dr = dr.z2o()             ## cut all coordinates to range [0,1)
                if dr.vlen2() < 0.001:    ## dr != Vec( 0.0, 0.0, 0.0 )
                    fbasis = False        ## point v is not in basis
                    break

            if fbasis:
                v = nrep.dec2frac( v ).z2o()    ## cut basis vector by new unit cell
                vsn.add( nrep.frac2dec( v ) )   ## transform it back to decart and add to basis

        #print k, "--->", vsn
        uc.add( k, vsn )


    return uc
    #for v in ext.pnts['K']:
    #    drawgl( v, r = 0.06, color=(1,0,0) )



import ucell
ucell.UCell.to_min = to_min