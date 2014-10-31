
# Previously this file was used for the WSGIScriptAlias, the functionality has
# been moved to wsgi.py in the rekishi root
#
from warnings import warn
import os

warn("deprecated wsgi configuration file \"%s\", look into using wsgi.py instead." % __file__, DeprecationWarning)

rekishi_path = os.path.dirname(__file__)
exec open(rekishi_path + "/../wsgi.py", "r")


