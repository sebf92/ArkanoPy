# http://web.archive.org/web/20100523132518/http://code.activestate.com/recipes/65207-constants-in-python/?in=user-97991

class _const:
    '''
    Example:\n\n
    import const\n
    # bind an attribute ONCE:\n
    const.magic = 23\n
    # but NOT re-bind it:\n
    const.magic = 88\n      
    # raises const.ConstError\n    
    '''
    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value
import sys
sys.modules[__name__]=_const()