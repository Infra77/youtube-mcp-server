"""Current completion addendum plus byte-preserved source pages (text equality verified)."""
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pypdf import PdfReader,PdfWriter
R=Path(__file__).resolve().parents[1];T=R/'target/pdf';T.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet()
styles['Title'].fontSize=24;styles['Title'].leading=29;styles['Title'].textColor=colors.HexColor('#153650')
styles['BodyText'].fontSize=10;styles['BodyText'].leading=14;styles['BodyText'].spaceAfter=9
styles['Heading2'].fontSize=13;styles['Heading2'].leading=17;styles['Heading2'].spaceBefore=12
pages=[('Completion remediation edition',[
('Authority and status','3 November 2026. This updated copy replaces the earlier implementation addendum. All 53 original handbook pages follow unchanged. The client project and SDLC PDFs remain authoritative. This is a remediated local review candidate, not a claim that Google, human review or team delivery have already occurred.'),
('The product','Java 21, Spring Boot/Spring AI MCP over stdio, official YouTube API, PostgreSQL/Flyway and separate Windows OAuth/approval CLI. No custom frontend or public MCP HTTP service. Five Agent Skills and the Obsidian PARA vault remain required deliverables.'),
('Verified evidence versus pending evidence','Consult docs/test-results.md for current executed tests. Tests use synthetic data, WireMock, disposable PostgreSQL and a real packaged MCP client. Documentation/schema checks are not behavioral skill evaluations. Google consent, real-account demonstrations, independent machines, human review and GitHub evidence must be recorded separately.'),
('Portable source and execution plan','The three source PDFs are copied under docs/reference for member review. The external plan.md contains 16 steps for each of three members: 48 work packages with context, requirements, commands, reviews, evidence and final acceptance gates. Open brain/ as the Obsidian vault. Keep handbook step notes outside the project.'),
('Honest development history','The team starts from an existing AI-assisted implementation. Import it honestly, then create real review, testing, correction and acceptance commits. Do not fabricate prior reviews, contributor identities, stage dates or PR links. Human responsibility for every merged change remains mandatory.')]),
('Implementation amendments',[
('OAuth and disconnect - Steps 24, 37, 39','A running vault pins the encrypted credential-file generation. Replacing or deleting the credential invalidates cached access and requires restarting MCP. Logout attempts remote revocation but removes local credentials even on failure, reporting the two outcomes separately. An interactive channel-ID command removes orphan local records.'),
('Cache, pagination and quota - Steps 16, 22, 23, 28','Metadata cache: five-minute lifetime, 128 entries, account-keyed, in process; no personal collection responses cached. Cache hits incur no API charge. Full preflight conservatively reserves cache-miss costs. Personal collections use up to two pages within existing item bounds; repeated page tokens fail closed. Maximum personal reads are 21; recommendations reserve 22 reads plus one search.'),
('Drafts and truthful results - Steps 13, 31, 32','Schema-2 drafts persist exclusion reasons and canonical video URLs. Existing stored proposal bytes retain their hash checks. Commit results distinguish proposed and confirmed counts/runtime and expose each item status. Metadata language is not proof of spoken language; total duration is a documented upper bound.'),
('Safe partial repair - Step 32','A separate human CLI REPAIR grant may repair only PARTIAL with a known playlist ID. Read back, require the exact approved prefix, append only the missing suffix, then read back again. Unknown creates and active/crashed writers are not blindly replayed. RESOLVE records human inspection without claiming successful creation. Stop other writers before recovery.'),
('Retention - Steps 14, 43, 47','Startup/hourly and explicit cleanup remove expired uncommitted drafts and all draft metadata/grants/journals older than seven days. Old quota rows are pruned. Inspect unresolved writes before that deadline. An offline installation must clean before reuse. Remote playlists are never deleted by local cleanup.')]),
('Verification and final acceptance',[
('Security and dependency review - Step 40','Compatible dependency patches replace affected original versions; pom.xml and the generated BOM are authoritative. Gitleaks is checksum-verified. OSV checks exact runtime versions and retains findings. The HTTP-only MCP DNS-rebinding advisory has an explicit stdio-only applicability disposition requiring human review; a transport change reopens it.'),
('Quality gates - Steps 18, 36-41','Local-check performs clean package, tests, formatting, links, traceability, strict skill YAML/cases, Gitleaks and actual MCP startup/read. Additional OAuth/provider/recovery/retention tests and synthetic relevance/timing evidence complement the original suite. Actual skill-host runs are required at each stage; generated expected outcomes do not count as those runs.'),
('Three-member schedule and stage reviews','The shared plan revalidates Stage 1 by Day 3, Stage 2 by Day 6, Stage 3 by Day 11 and Stage 4 by Day 16. Every member has daily work and reciprocal peer review. Days 14-15 reserve time for closure and rehearsals. Day 16 has pre-release reviews, publication, then independent verification; no circular approval dependency.'),
('External gates cannot be fabricated','GitHub authentication does not authorize Google consent. The account owner signs in/consents and personally types real playlist approval. Another human reviews changes. Real independent-machine, live-host, scheduled-live and final tag evidence must exist. Missing prerequisites block completion; reaching Day 16 is not itself acceptance.'),
('Entry points','Read README.md, docs/remediation-status.md, docs/acceptance-status.md and docs/adr/0010.md. Follow docs/setup-windows.md. Run python scripts/release_gate.py --final only when linked evidence is complete. The original handbook begins on the next page with its original page numbering.')])]
story=[]
for index,(title,sections) in enumerate(pages):
 if index:story.append(PageBreak())
 story.append(Paragraph(title,styles['Title']))
 for heading,text in sections:
  story.append(Paragraph(heading,styles['Heading2']));story.append(Paragraph(text,styles['BodyText']))
def footer(c,d):
 c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#536579'));c.drawString(42,26,'Completion addendum | 3 November 2026');c.drawRightString(A4[0]-42,26,f'{d.page} / 3')
add=T/'completion-addendum.pdf'
SimpleDocTemplate(str(add),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=36,bottomMargin=48).build(story,onFirstPage=footer,onLaterPages=footer)
assert len(PdfReader(add).pages)==3,'Inspect pagination before delivery'
source=R/'docs/reference/YouTube_Intelligence_MCP_Server_Only_Handbook.pdf'
original=PdfReader(source);assert len(original.pages)==53
out=R/'docs/YouTube_Intelligence_MCP_Handbook_Updated.pdf'
writer=PdfWriter();writer.append(add);writer.append(source)
with out.open('wb') as f:writer.write(f)
result=PdfReader(out);assert len(result.pages)==56
assert all(a.extract_text()==result.pages[i+3].extract_text() for i,a in enumerate(original.pages))
print('56 pages; all original 53 page texts preserved. Render/view the three addendum pages.')
