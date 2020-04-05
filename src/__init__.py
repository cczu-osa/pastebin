import os

if not os.path.isdir('data'):
    os.mkdir('data')

from src.app import app as application
import src.api
import src.database
import src.tasks
import src.settings
import src.router
