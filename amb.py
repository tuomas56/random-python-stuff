import itertools as _itertools
 
class Amb(object):
    def __init__(self):
        self._names2values   = {}       # set of values for each global name
        self._func           = None     # Boolean constraint function
        self._valueiterator  = None     # itertools.product of names values
        self._funcargnames   = None     # Constraint parameter names
 
    def __call__(self, arg=None):
        if hasattr(arg, '__code__'):                
            ##
            ## Called with a constraint function. 
            ##
            globls = arg.__globals__ if hasattr(arg, '__globals__') else arg.func_globals
            # Names used in constraint
            argv = arg.__code__.co_varnames[:arg.__code__.co_argcount]
            for name in argv:
                if name not in self._names2values:
                    assert name in globls, \
                           "Global name %s not found in function globals" % name
                    self._names2values[name] = globls[name]
            # Gather the range of values of all names used in the constraint
            valuesets = [self._names2values[name] for name in argv]
            self._valueiterator = _itertools.product(*valuesets)
            self._func = arg
            self._funcargnames = argv
            return self
        elif arg is not None:
            ##
            ## Assume called with an iterable set of values
            ##
            arg = frozenset(arg)
            return arg
        else:
            ##
            ## blank call tries to return next solution
            ##
            return self._nextinsearch()
 
    def _nextinsearch(self):
        arg = self._func
        globls = arg.__globals__
        argv = self._funcargnames
        found = False
        for values in self._valueiterator:
            if arg(*values):
                # Set globals.
                found = True
                for n, v in zip(argv, values):
                    globls[n] = v
                break
        if not found: raise StopIteration
        return values
 
    def __iter__(self):
        return self
 
    def __next__(self):
        return self()
    next = __next__ # Python 2