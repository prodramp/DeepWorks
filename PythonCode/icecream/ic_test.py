from icecream import ic
from icecream import install
import time
import logging

install()
ic.disable()


def my_timestamp():
    return '%i |> ' % int(time.time())


def warn(s):
    logging.warning(s)


def toString(obj):
    if isinstance(obj, str):
        return '[!string %r with length %i!]' % (obj, len(obj))
    return repr(obj)


ic.configureOutput(prefix=my_timestamp)
ic.configureOutput(outputFunction=warn)
ic.configureOutput(argToStringFunction=toString)
ic.configureOutput(includeContext=True, contextAbsPath=False)



def first():
    return 'first'


def second():
    return 'second'


def third():
    return 'third'


def foo():
    print(0)
    a = third()
    if a == 'first':
        print(1)
        a = second()
    else:
        print(2)
        a = third()


def foo_ic():
    ic()
    a = third()
    if a == 'first':
        ic()
        a = second()
    else:
        ic()
        a = third()


#foo_ic()
