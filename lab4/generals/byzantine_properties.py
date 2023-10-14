class ByzantineProperties:
    def __init__(self, on_tie, no_loyal, no_total):
        self.on_tie: object = False
        self.no_loyal: int = no_loyal
        self.no_total: int = no_total