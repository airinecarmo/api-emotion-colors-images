

class SameStatusException(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Can not change the current status to the same status"
        super(SameStatusException, self).__init__(msg)


class StepJumpException(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Can not jump steps"
        super(StepJumpException, self).__init__(msg)
