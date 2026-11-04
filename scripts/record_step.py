"""Append factual, detailed handbook evidence to the user's external notes folder."""
from pathlib import Path
import argparse
ROOT = Path(__file__).resolve().parents[1]
def record(number, title, status, actions, files, checks, cumulative, limitations='None identified for this local step.'):
    folder = ROOT.parent / 'notes'
    folder.mkdir(exist_ok=True)
    text = f'''# Step {number}: {title}

Date: 2026-10-31 (Asia/Calcutta). Contributor: Codex, working for the user.
Status: {status}. Numbering is the handbook's explicit Step number, not its chapter number.

## What this step requires and what I did
{actions}

## Files and how to inspect the work
{files}

All project-relative paths above are inside `../youtube-intelligence-mcp/` from this notes folder.
The client PDFs remain at the parent SE folder. Extracted text in docs/source-text retains page
markers for auditing. No original client PDF was overwritten.

## Verification and interpretation
{checks}

## What is implemented up to this point
{cumulative}

## Remaining evidence and limitations
{limitations}

## Learning explanation
Requirements describe observable behavior, design establishes invariants, implementation enforces
them, and tests provide evidence. A file's existence alone does not establish runtime correctness.
This note distinguishes those stages. A fixture is synthetic input for a reproducible test, not a
record of an actual user's account or proof of a real YouTube operation. Human review and GitHub
work are separate obligations; the user deferred GitHub and we do not manufacture those records.
'''
    (folder/f'step {number}.md').write_text(text,encoding='utf-8')
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('number',type=int); parser.add_argument('title'); parser.add_argument('detail')
    args=parser.parse_args()
    record(args.number,args.title,'Implemented locally',args.detail,'See the paths described above.','See docs/test-results.md for executed checks.','Previous step artifacts remain in the project.')
