#!/usr/bin/env python3
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

validator_path=Path(__file__).with_name('validate.py')
if not validator_path.exists():validator_path=Path(__file__).with_name('validate-repository.py')
spec=importlib.util.spec_from_file_location('validator',validator_path)
validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)

class ReleaseValidation(unittest.TestCase):
    def fixture(self, directory, extra=None):
        name='GenerateMasters-0.4.7-20261115150003.zip'
        payload={p:b'' for p in ['pixinsight/GenerateMasters.js','pixinsight/GenerateMasters.svg','pixinsight/includes/open-blink.scp','scripts/one-run.mjs','config.yaml']}
        if extra:payload.update(extra)
        entries=[{'path':p,'size':len(d),'sha256':hashlib.sha256(d).hexdigest()} for p,d in payload.items()]
        payload['release-manifest.json']=json.dumps({'name':'GenerateMasters','schemaVersion':1,'files':entries}).encode()
        with zipfile.ZipFile(directory/name,'w') as z:
            for p,d in payload.items():z.writestr(validator.PREFIX+p,d)
        sha=hashlib.sha1((directory/name).read_bytes()).hexdigest()
        root=ET.Element('xri',version='1.0')
        for os in ['macosx','linux']:
            p=ET.SubElement(root,'platform',os=os,arch='noarch',version='1.9.4:*')
            ET.SubElement(p,'package',fileName=name,sha1=sha,type='script',releaseDate='20261115150003')
        (directory/'updates.xri').write_bytes(ET.tostring(root))
        (directory/'SHA256SUMS').write_text(''.join(hashlib.sha256((directory/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in [name,'updates.xri']))
        return name
    def test_valid(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.fixture(p);validator.validate(p)
    def test_rejects_corrupt_zip(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);name=self.fixture(p);(p/name).write_bytes(b'corrupt')
            with self.assertRaises(AssertionError):validator.validate(p)
    def test_rejects_private_script_and_traversal(self):
        for path in ['pixinsight/ProcessMasters.js','../escape','node_modules/a/index.js.map','pixinsight/DanAstroPhoto.js']:
            with self.subTest(path=path),tempfile.TemporaryDirectory() as d:
                p=Path(d);self.fixture(p,{path:b''})
                with self.assertRaises(AssertionError):validator.validate(p)
    def test_rejects_other_menu_entry(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);self.fixture(p,{'pixinsight/bridge/bridge.js':b'#feature-id Utilities > Bridge'})
            with self.assertRaises(AssertionError):validator.validate(p)

if __name__=='__main__':unittest.main()
