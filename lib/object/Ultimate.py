from copy import deepcopy
from pygame import Surface

from lib.utils.Utils import Utils


class Ultimate:
    def __init__(self, enable_function=lambda parent: None, disable_function=lambda parent: None, duration=5):
        self.enable_function = enable_function
        self.disable_function = disable_function
        self.duration = duration

    
    def copy(self, parent):
        copyobj = type(self)()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                if type(attr) is Surface:
                    copyobj.__dict__[name] = Surface.copy(attr)

                elif callable(attr):
                    copyobj.__dict__[name] = Utils.copy_function(attr, parent_class=parent)
                    
                else:
                    copyobj.__dict__[name] = deepcopy(attr)
        return copyobj