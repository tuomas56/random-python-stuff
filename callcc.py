import greenlet


class ContinuationError(Exception): pass


def callcc(f):

    saved = [greenlet.getcurrent()]


    def cont(val):

        if saved[0] == None:

            raise ContinuationError("one shot continuation called twice")

        else:

            return saved[0].switch(val)


    def new_cr():

        v = f(cont)

        return cont(v)


    value_cr = greenlet.greenlet(new_cr)

    value = value_cr.switch()

    saved[0] = None

    return value
