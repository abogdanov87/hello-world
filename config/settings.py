SERVER = 'DEVELOP'

if SERVER == 'TEST':
    from .test import *

if SERVER == 'DEVELOP':
    from .base import *