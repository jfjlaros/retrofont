from hatchling.metadata.plugin.interface import MetadataHookInterface


_author = 'Jeroen F.J. Laros'
_email = 'jlaros@fixedpoint.nl'
_description = 'TrueType retro fonts.'
_keywords = ['retro', 'font', 'TrueType']
_license = 'MIT'
_project = 'RetroFont'
_url = 'https://github.com/jfjlaros/retrofont'
_version = '0.0.1'
_year = '2025'

_classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    f'License :: OSI Approved :: {_license} License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules']
_copyright = f'Copyright (c) {_year} by {_author} <{_email}>'
_info = f'{_project} version {_version}\n\n{_copyright}\nHomepage: {_url}'


class JSONMetaDataHook(MetadataHookInterface):
    def update(self, metadata):
        package_metadata = {
            'authors': [{'name': _author, 'email': _email}],
            'classifiers': _classifiers,
            'description': _description,
            'keywords': _keywords,
            'license': _license,
            'license-files': ['LICENSE.md'],
            'readme': 'README.rst',
            'version': _version}
        metadata.update(package_metadata)
