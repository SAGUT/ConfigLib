import logging
from ..LibFrame import applicationDict
from pathlib import Path
import os
class FileHandler(object):

    def __init__(self):
        self.config=applicationDict['config']
        self.projectdir=Path(self.config['project']['projectdir'])
        self.checkDir()

    def checkDir(self):
        if not os.path.exists(self.projectdir):
            Path(self.projectdir).mkdir(parents=True, exist_ok=True)