class UltimateManager():
    def __init__(self):
        
        self.ultimate_enabled = False

        self.disable_ultimate_function = lambda: None

    def do_ultimate(self, enable_function: lambda: None, disable_function: lambda: None) -> bool:
        if self.ultimate_enabled is not True:
            enable_function()
            self.disable_ultimate_function = disable_function
            self.ultimate_enabled = True

            return True
        
        return False


    def disable_ultimate(self):
        self.disable_ultimate_function()
        self.ultimate_enabled = False