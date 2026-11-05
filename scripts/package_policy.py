"""Filename policy for public release artifacts; never rely on Git ignore rules."""
from pathlib import PurePosixPath

PRIVATE_PARTS = {'.local', '.tools', '.git', 'source-text', '__pycache__'}


def excluded_path(name):
    path = PurePosixPath(name.replace('\\', '/'))
    parts = [part.casefold() for part in path.parts]
    if path.is_absolute() or '..' in parts or any(':' in part for part in parts):
        return True
    if any(part in PRIVATE_PARTS for part in parts):
        return True
    for part in parts:
        if part in {'workspace.json', 'workspace-mobile.json', 'desktop-client.json'}:
            return True
        if part == '.env' or (part.startswith('.env.') and part != '.env.example'):
            return True
        if part.endswith(('.pdf', '.dpapi')) or part.startswith('tokens'):
            return True
        if part.startswith('client_secret') and part.endswith('.json'):
            return True
    return False


def verify_archive_members(archive):
    """Reject private paths even in archives produced by a different packager."""
    for member in archive.infolist():
        if excluded_path(member.filename):
            raise ValueError('Archive contains a forbidden private or unsafe path')
        # Do not extract Unix symlinks supplied by an archive producer.
        if (member.external_attr >> 16) & 0o170000 == 0o120000:
            raise ValueError('Archive contains a symbolic link')
