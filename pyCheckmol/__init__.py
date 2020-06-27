from .pyCheckmol import CheckMol

import os
home = os.getenv("HOME")
if os.path.isdir('{}/.pycheckmoltmp'.format(home)):
    pass
else:
    os.mkdir(home+'/.pycheckmoltmp')