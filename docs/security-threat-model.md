# Threat model
Assets: refresh credentials, private metadata, account integrity, approval grants and quota.
AI tool input and all video metadata are untrusted. No model argument selects account or grants consent.
URL parsing checks exact host/path, rejects userinfo/ports/fragments ambiguity and never fetches user URLs.
Provider origins are fixed in production; loopback override is test-only. SQL uses bound parameters.
CLI requires a real console, previews exact account/privacy/items/digest, and verifies the typed phrase.
Fingerprint, expiry and account are checked again in the database claim. Same-OS-user code/DB access
is a trusted local boundary, not a defense against arbitrary malicious local administrators.
Write intent persists before network send; ambiguous response fails closed for manual reconciliation.
No raw provider bodies or exception text are returned to the model. Logs must omit private collections.
DPAPI credentials are scoped to CurrentUser and live outside source; .env is ignored. Logout revokes
and removes credentials; data deletion removes local account drafts/grants/journals.
Scope youtube.force-ssl supports required operations. No partner scope, password collection or OOB flow.
Live acceptance is pending the user's Google setup. Production retention must be checked against
current YouTube developer policy before deployment beyond coursework.
