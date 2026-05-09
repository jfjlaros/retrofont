from sys import modules
from types import ModuleType

mock = ModuleType('fontforge')
mock.font = object
mock.open = object
modules['fontforge'] = mock
mock = ModuleType('psMat')
mock.scale = object
modules['psMat'] = mock

from retrofont.meta import _author, _copyright, _project, _version


author = _author
copyright = _copyright
project = _project
release = _version

autoclass_content = 'both'
extensions = [
    'sphinx.ext.autodoc', 'sphinx_autodoc_typehints', 'sphinxarg.ext']
