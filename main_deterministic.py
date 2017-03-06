"""To prevent against security attacks, dictionary and set traversal are
not deterministic since Python 3.3.
This is controlled by the value of the environment variable `PYTHONHASHSEED`,
but it has to be done before the interpreter launches. Hence the following code.

Details: https://docs.python.org/3.3/using/cmdline.html#envvar-PYTHONHASHSEED
"""

import os
import subprocess

os.environ['PYTHONHASHSEED'] = '0'
proc = subprocess.call(['python', 'main.py'])
