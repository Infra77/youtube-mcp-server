"""Synthetic regression for private files in public release packages."""
import ast
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from package_policy import verify_archive_members

PRIVATE = ['reference/Project_1_YouTube_MCP.pdf', 'Handbook.PDF',
           'desktop-client.json', 'client_secret_demo.json', 'profile.DPAPI',
           '.env', '.env.live', 'tokens.json', 'source-text/original.txt']


class PackagePrivacyTest(unittest.TestCase):
    def test_packager_excludes_private_files_under_every_root(self):
        source = ROOT / 'scripts/package_release.py'
        values = {}
        for node in ast.parse(source.read_text(encoding='utf-8')).body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in {'roots', 'files'}:
                    values[node.targets[0].id] = ast.literal_eval(node.value)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in values['files']:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('SYNTHETIC TEST ONLY', encoding='utf-8')
            for directory in values['roots']:
                for name in PRIVATE + ['public.md', '.env.example']:
                    p = root / directory / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text('SYNTHETIC TEST ONLY', encoding='utf-8')
            evidence = root / 'target/evidence'
            evidence.mkdir(parents=True)
            (evidence / 'local-check.json').write_text(json.dumps({'overall': 'PASS'}))
            for name in ['package_release.py', 'package_policy.py']:
                shutil.copyfile(ROOT / 'scripts' / name, root / 'scripts' / name)
            result = subprocess.run([sys.executable, str(root / 'scripts/package_release.py')],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(next((root / 'release').glob('*.zip'))) as archive:
                names = {name.split('/', 1)[1] for name in archive.namelist()}
                for directory in values['roots']:
                    for name in PRIVATE:
                        self.assertNotIn(f'{directory}/{name}', names)
                    self.assertIn(f'{directory}/public.md', names)
                    self.assertIn(f'{directory}/.env.example', names)
                self.assertIn('target/curator.jar', names)
                verify_archive_members(archive)

    def test_verifier_rejects_contaminated_archives(self):
        for name in PRIVATE + ['../escape', 'C:/escape', 'docs\\desktop-client.json']:
            with self.subTest(path=name):
                data = io.BytesIO()
                with zipfile.ZipFile(data, 'w') as archive:
                    archive.writestr(name, 'SYNTHETIC TEST ONLY')
                data.seek(0)
                with zipfile.ZipFile(data) as archive:
                    with self.assertRaises(ValueError):
                        verify_archive_members(archive)


if __name__ == '__main__':
    unittest.main()
