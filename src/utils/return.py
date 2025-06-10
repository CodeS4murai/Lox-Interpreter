class Return(Exception): # Custom exception class for return statements
    def __init__(self, value):
        super().__init__()
        self.value = value
