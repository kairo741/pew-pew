class Ultimate:
    def __init__(self, enable_function=lambda: None, disable_function=lambda: None, duration=5):
        self.enable_function = enable_function
        self.disable_function = disable_function
        self.duration = duration