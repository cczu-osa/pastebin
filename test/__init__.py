import os
import shutil

if os.path.isdir('data'):
    shutil.rmtree('data')