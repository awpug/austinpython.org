""" Basic helpers for tests in AustinPython. """

class Mock(object):
    """ Serves as a sort of object literal for mocking. """
    def __init__(self, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

