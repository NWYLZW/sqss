#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class ValAssignedSetException(BaseException):
    """ Common base class for all exceptions """
    def __init__(self):
        super(ValAssignedSetException, self).__init__()
        self.message = 'It should be assigned, but there is no assignment.'
