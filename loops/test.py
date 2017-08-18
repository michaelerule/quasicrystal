
# Make stuff behave like atomics but use equality operator instead of hash
class Pool():
    def __init__(self,dtype=None):
        self.storage = []
        self.dtype = dtype
    def __call__(self,*args):
        '''
        call returns hashable key
        '''
        if self.dtype != None and (len(args)!=1 or type(args[0])!=self.dtype):
            item = self.dtype(*args)
        else:
            assert len(args)==1
            item = args[0]
        if self.dtype != None:
            print (item,type(item),self.dtype)
            assert type(item)==self.dtype
        for i,thing in enumerate(self.storage):
            if thing==item:
                return i
        self.storage += [item]
        return len(self.storage)-1
    def __getitem__(self,i):
        '''
        getitem retrieves based on hashable key
        '''
        return self.storage[i]

def angle(z):
    return atan2(z.imag,z.real)

class Point(): 
    '''
    Reference conainer for a 2D point stored as complex
    '''
    def __init__(self,z):
        self.z = z
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
        assert (other.__class__) in (Point,complex)
        return abs(self.z-other.z)<MINSCALE
    def __add__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__add__(other))
    def __div__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__div__(other))
    def __divmod__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__divmod__(other))
    def __floordiv__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__floordiv__(other))
    def __mod__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__mod__(other))
    def __mul__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__mul__(other))
    def __neg__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__neg__(other))
    def __nonzero__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__nonzero__(other))
    def __pos__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__pos__(other))
    def __pow__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__pow__(other))
    def __radd__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__radd__(other))
    def __rdiv__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rdiv__(other))
    def __rdivmod__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rdivmod__(other))
    def __rfloordiv__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rfloordiv__(other))
    def __rmod__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rmod__(other))
    def __rmul__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rmul__(other))
    def __rpow__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rpow__(other))
    def __rsub__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rsub__(other))
    def __rtruediv__(self,other):
        assert (other.__class__) in (Point,complex)
        return Point(self.z.__rtruediv__(other))
    @property
    def conjugate(self):
        return Point(self.z.conjugate)
    @property
    def imag(self):
        return self.z.imag
    @property
    def real(self):
        return self.z.real
    def __abs__(self):
        print self.z
        return abs(self.z)
