class Event:
    class Move:
        pass

    class Reproduce:
        def __init__(self, child):
            self.child = child

    class Die:
        pass

    class Stay:
        pass
