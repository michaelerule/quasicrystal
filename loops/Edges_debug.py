#!/usr/bin/env jython

from java.awt          import *
from java.awt.event    import *
from java.awt.image    import *
from java.awt.Color    import *
from java.awt.geom     import *
from jarray            import *
from javax.swing       import *
from javax.swing.event import *
from java.lang         import *
import random
from math              import *
from cmath             import *
from collections       import *

# Symmetry order
M = 7

# Unit vector length
R = 40

# Window size
SCREENSIZE = 800

# Fixed unit vectors for all diections (oriented)
units = [R*exp(1j*pi*i/M) for i in range(2*M)]

# Prepare image buffer for rendering scratch space
image = BufferedImage(SCREENSIZE,SCREENSIZE,BufferedImage.TYPE_INT_RGB)
GQ    = image.createGraphics()
GQ.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON)

def cleardrawing():
    GQ.color = Color.WHITE
    GQ.fillRect(0,0,SCREENSIZE,SCREENSIZE)

# Start with blank canvas
cleardrawing()
       
# Initialize window
class Screen(JPanel):
    def paint(self,g):
        g.drawImage(image,0,0,SCREENSIZE,SCREENSIZE,None) 
jp               = Screen(BorderLayout())
jp.preferredSize = Dimension(SCREENSIZE,SCREENSIZE)

jf                       = JFrame("Tiles")
#jf.defaultCloseOperation = JFrame.EXIT_ON_CLOSE
jf.contentPane           = jp
jf.pack()
jf.show()

# Tile color pallet, RGB format [0,1)
colors = [(1,1,1),
(1  ,0 , 0), (0 , 0, 0),
(0  ,1 , 1), (0 ,.2,.5),
(1  ,1 , 0), (0 , 1, 0),
(1  ,0 , 1), (.4, 0, 1),
(.8 ,.8,.8), (.2,.2,.2),
(1  ,.5, 0), (.2,.2, 0),
(0.5, 1, 0), (1.,.5,.5)]

# Convert pallet to awt Colors
colors = [Color(r*.999,g*.999,b*.999) for (r,g,b) in colors]

# Equality is very approximate
MINSCALE = 0.1

# Make stuff behave like atomics but use equality operator instead of hash
class Pool():
    def __init__(self,dtype=None):
        self.storage = []
        self.dtype = dtype
    def __call__(self,item):
        '''
        call returns hashable key
        '''
        '''
        if self.dtype != None and (len(args)!=1 or args[0].__class__!=self.dtype):
            item = self.dtype(*args)
        else:
            assert len(args)==1
            item = args[0]
        '''
        if self.dtype!=None:
            if item.__class__ != self.dtype:
                print 'Type mismatch',item.__class__,self.dtype
            assert item.__class__==self.dtype
        for i,thing in enumerate(self.storage):
            if thing==item:
                return i
        self.storage += [item]
        return len(self.storage)-1
    def __getitem__(self,i):
        '''
        getitem retrieves based on hashable key
        '''
        if type(i) is int:
            return self.storage[i]
        return [self[j] for j in i]
            

def angle(z):
    return atan2(z.imag,z.real)

class Point(): 
    '''
    Reference conainer for a 2D point stored as complex
    '''
    def __init__(self,z):
        if z.__class__ is Point:
            z = z.z
        if not z.__class__ == complex:
            print 'Type error',z
        z = complex(z)
        self.z = z
        #print self.z
        self.edgeset = set()
        self.tileset = set()
    @property
    def angle(self):
        return atan2(self.imag,self.real)
    @property
    def x(self):
        return self.real
    @property
    def y(self):
        return self.imag
    def __eq__(self,other):
        if not (other.__class__) in (Point,complex): return False
        return abs(self.z-other.z)<MINSCALE
    def __add__(self,other):
        assert (other.__class__) in (Point,complex)
        if other.__class__ is Point:
            other = other.z
        return Point(self.z+other)
    def __sub__(self,other):
        assert (other.__class__) in (Point,complex)
        if other.__class__ is Point:
            other = other.z
        return Point(self.z-other)
    def __div__(self,other):
        assert (other.__class__) in (Point,complex)
        if other.__class__ is Point:
            other = other.z
        return Point(self.z/other)
    def __mul__(self,other):
        assert (other.__class__) in (Point,complex)
        if other.__class__ is Point:
            other = other.z
        return Point(self.z*other)
    def __neg__(self):
        return Point(-self.z)
    @property
    def conjugate(self):
        return Point(self.z.conjugate)
    @property
    def imag(self):
        #print self.z
        return self.z.imag
    @property
    def real(self):
        #print self.z
        return self.z.real
    def __abs__(self):
        #print self.z
        return abs(self.z)

class Edge:
    '''
    Oriented graph edge between two points
    '''
    def __init__(self,a,b,color=None):
        self.color  = color
        self.ia = pointpool(Point(a)) if (a.__class__) in (Point,complex) else a
        self.ib = pointpool(Point(b)) if (b.__class__) in (Point,complex) else b
        #print '??',a,b,self.ia,self.ib
        self.pointset = set()
        self.tileset = set()
        pointpool[self.ia].edgeset.add(edgepool(self))
        pointpool[self.ib].edgeset.add(edgepool(self))
    @property
    def a(self):
        return pointpool[self.ia]
    @property
    def b(self):
        return pointpool[self.ib]
    def paint(self,G):
        if self.color: G.color = self.color
        a,b = self.a,self.b
        G.draw(Line2D.Float(a.x,a.y,b.x,b.y))
    @property
    def delta(self):
        return self.b-self.a
    @property
    def length(self):
        return self.delta.magnitude
    @property
    def angle(self):
        return self.delta.angle
    @property
    def unit(self):
        if self.length<1e-8:
            return Point(1+0j)
        return self.delta/self.length
    def __eq__(self,other):
        if not (other.__class__) in (Edge,Edge): return False
        if (self.ia==other.ia and self.ib==other.ib):
            return True
        if abs(self.a-other.a)<MINSCALE and abs(self.b-other.b)<MINSCALE:
            return True
        if abs(self.b-other.a)<MINSCALE and abs(self.a-other.b)<MINSCALE:
            return True
        return False

class Tile:
    """
    Pair of edges that define a rhomboid tile
    """
    def __init__(self,*p,**kwargs):
        assert len(p)==3
        self.pi = [pointpool(Point(q)) for q in p]
        #print self.pi,self.p
        color = colors[self.tiletype%len(colors)]
        if 'color' in kwargs:
            color = kwargs['color']
        self.color = color
        self.edgeset = set()
        self.pointset = set()
        self.tileset = set()
        for e in self.edges:
            e = edgepool[i]
            e.tileset.add(tilepool(self))
            
    @property 
    def edges(self):
        a,b,c,d = self.tile
        return [edgepool(Edge(p,q)) for p,q in [(a,b),(b,c),(c,d),(d,a)]]
    @property
    def p(self):
        return [pointpool[i] for i in self.pi]
    def draw(self,G):
        if not self.color is None: G.color = self.color
        p = self.tile
        G.drawPolygon([int(.5+z.x) for z in p],[int(.5+z.y) for z in p],4)
    def fill(self,G):
        if not self.color is None: G.color = self.color
        p = self.tile
        G.fillPolygon([int(.5+z.x) for z in p],[int(.5+z.y) for z in p],4)
    @property
    def tile(self):
        a,b,c = self.p
        return map(Point,[a,b,c,a+c-b])
    @property
    def tilei(self):
        a,b,c = self.p
        return [pointpool(Point(q)) for q in [a,b,c,a+c-b]]
    @property
    def e0(self):
        return Edge(self.p[0],self.p[1])
    @property
    def e1(self):
        return Edge(self.p[1],self.p[2])
    @property
    def angle(self):
        p0,p1,p2 = self.p
        return (angle(p0-p1)-angle(p2-p1) + 4*pi)%(2*pi)
    @property
    def tiletype(self):
        span = self.angle
        if span> pi  : span = 2*pi-span
        if span>=pi/2: span = pi-span
        return int(span/(pi/M)+0.5)
    @property
    def span(self):
        span = self.angle
        span = 2*pi-span
        if span>pi:
            span = 2*pi-span
        return int(span/(pi/M)+0.5)
    def __eq__(self,other):
        # Check if two tiles occupy same slot in space
        # Clockwise / andticlockwise tiles are not equivalent (TODO)
        tt = set(self.tilei)
        to = set(other.tilei)
        return len(tt-to)==0 and len(to-tt)==0

# TODO: datastructures are a mess!
pointpool = Pool(Point)
edgepool  = Pool(Edge)
tilepool  = Pool(Tile)

# Test point class and mutability
p = pointpool(Point(1+1j))
q = pointpool(Point(1+1j))
pointpool[p].real = 10
print "Point test:",pointpool[p].x,pointpool[p].y 

# Edge test
e1 = edgepool[edgepool(Edge(30+40j,100+22j))]
print 'Edge test',e1,edgepool[edgepool(Edge(e1.a,e1.b))]

def unitTile(c,u1,u2):
    u0   = units[u1%(2*M)]
    u1   = units[u2%(2*M)]
    tile = Tile(c,c+u0,c+u0+u1)
    return tile

# Test tile class
center = (1+1j)*SCREENSIZE/2
j = 0
for i in range(M//2):
    t = unitTile(center,j,j+1+i)
    t.fill(GQ)
    j+=1+i
    print t.tiletype,t.span
jp.repaint()

# Initialize seed
perimeter = [unitTile(center,i,i+1) for i in range(M*2)]
cleardrawing()
for t in perimeter:
    t.fill(GQ)
jp.repaint()

# Find all edges in seed
alledges = []
for t in perimeter:
    a,b,c,d = t.tile
    alledges += [Edge(p,q) for p,q in [(a,b),(b,c),(c,d),(d,a)]]

# Remove interior edges
edgekeys = map(edgepool,alledges)

# All edges
GQ.color = CYAN
for k in edgekeys:
    edgepool[k].paint(GQ)
jp.repaint()

# Exterior edges
counts = defaultdict(int)
for k in edgekeys: counts[k]+=1
exterior = [k for k in edgekeys if counts[k]==1]

GQ.color = BLACK
for k in exterior:
    edgepool[k].paint(GQ)
jp.repaint()

# Inspect, did we find nearby edges?
for p in pointpool.storage:
    print p.edgeset

