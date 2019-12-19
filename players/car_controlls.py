class CarControl:
    def __init__(self, controls=[0, 0, 0]):
        self.forward = (controls[0] == 1)
        self.backward = (controls[0] == -1)
        self.left = (controls[1] == -1)
        self.right = (controls[1] == 1)
