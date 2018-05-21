def funA(a):
    print 'funA'

def funB(b):
    print 'funB'

@funA
@funB
def funC():
    print 'funC'