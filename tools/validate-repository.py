#!/usr/bin/env python3
"""Validate a curated, unsigned PixInsight GenerateMasters feed without executing it."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import xml.etree.ElementTree as ET
import zipfile

PREFIX = 'src/scripts/GenerateMasters/'

def validate(directory):
    directory = Path(directory)
    root = ET.fromstring((directory/'updates.xri').read_bytes())
    assert root.tag == 'xri' and root.attrib == {'version':'1.0'}
    platforms = root.findall('platform')
    assert len(platforms) == 2
    assert {p.get('os') for p in platforms} == {'macosx', 'linux'}
    packages = []
    for platform in platforms:
        assert platform.get('arch') == 'noarch' and platform.get('version') == '1.9.4:*'
        assert len(platform.findall('package')) == 1
        packages.append(platform.find('package'))
    package = packages[0]
    assert packages[1].attrib == package.attrib
    name = package.get('fileName')
    assert re.fullmatch(r'GenerateMasters-\d+\.\d+\.\d+-\d{14}\.zip', name)
    assert package.get('type') == 'script' and package.get('releaseDate') == name[-18:-4]
    data = (directory/name).read_bytes()
    assert hashlib.sha1(data).hexdigest() == package.get('sha1'), 'ZIP SHA-1 mismatch'
    sums = dict(line.split('  ',1)[::-1] for line in (directory/'SHA256SUMS').read_text().splitlines())
    for filename in [name, 'updates.xri']:
        assert hashlib.sha256((directory/filename).read_bytes()).hexdigest() == sums[filename], 'SHA-256 mismatch'
    with zipfile.ZipFile(directory/name) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) and len(names) < 2000
        assert sum(i.file_size for i in archive.infolist()) < 100_000_000
        manifest = json.loads(archive.read(PREFIX+'release-manifest.json'))
        assert manifest['name'] == 'GenerateMasters' and manifest['schemaVersion'] == 1
        entries = manifest['files']
        assert set(names) == {PREFIX+e['path'] for e in entries} | {PREFIX+'release-manifest.json'}
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            assert info.filename.startswith(PREFIX) and '..' not in path.parts and '\\' not in info.filename
            assert not stat.S_ISLNK(info.external_attr >> 16) and info.file_size < 20_000_000
            assert not re.search(r'(?:ProcessMasters|DanAstroPhoto\.js|native/|/src/|\.git/|\.map$|\.ts$)',info.filename[len(PREFIX):],re.I), info.filename
            content = archive.read(info)
            assert not re.search(rb'/Users/[^/]+/|/Developer/AstroImaging|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY',content), info.filename
            if info.filename.endswith(('.js','.jsh')) and b'#feature-id' in content:
                assert info.filename == PREFIX+'pixinsight/GenerateMasters.js', 'Unexpected registered script'
        for entry in entries:
            content = archive.read(PREFIX+entry['path'])
            assert len(content) == entry['size'] and hashlib.sha256(content).hexdigest() == entry['sha256']
        for required in ['pixinsight/GenerateMasters.js','pixinsight/GenerateMasters.svg','pixinsight/includes/open-blink.scp','scripts/one-run.mjs','config.yaml']:
            assert PREFIX+required in names
    print('Validated GenerateMasters feed, archive boundaries and all hashes:', name)

if __name__ == '__main__':
    validate(sys.argv[1] if len(sys.argv)>1 else 'updates')
