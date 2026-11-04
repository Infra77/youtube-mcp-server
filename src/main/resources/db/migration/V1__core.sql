CREATE TABLE drafts (
 id UUID PRIMARY KEY, account VARCHAR(160) NOT NULL, proposal TEXT NOT NULL,
 fingerprint CHAR(64) NOT NULL, state VARCHAR(32) NOT NULL DEFAULT 'PROPOSED',
 expires_at TIMESTAMPTZ NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 remote_id VARCHAR(160), error_code VARCHAR(80),
 CHECK (state IN ('PROPOSED','APPROVED','CREATING','CREATED','PARTIAL','NEEDS_MANUAL_REVIEW','FAILED_BEFORE_WRITE'))
);
CREATE TABLE approvals (
 draft_id UUID PRIMARY KEY REFERENCES drafts(id) ON DELETE CASCADE,
 account VARCHAR(160) NOT NULL, fingerprint CHAR(64) NOT NULL,
 expires_at TIMESTAMPTZ NOT NULL, consumed_at TIMESTAMPTZ
);
CREATE TABLE write_journal (
 draft_id UUID NOT NULL REFERENCES drafts(id) ON DELETE CASCADE,
 step VARCHAR(80) NOT NULL, status VARCHAR(40) NOT NULL,
 remote_id VARCHAR(160), error_code VARCHAR(80), updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 PRIMARY KEY(draft_id,step)
);
CREATE TABLE quota_buckets (
 quota_date DATE NOT NULL, bucket VARCHAR(32) NOT NULL,
 configured_limit BIGINT NOT NULL CHECK(configured_limit>=0),
 consumed BIGINT NOT NULL DEFAULT 0 CHECK(consumed>=0),
 reserved BIGINT NOT NULL DEFAULT 0 CHECK(reserved>=0), PRIMARY KEY(quota_date,bucket)
);
CREATE TABLE quota_reservations (
 id UUID NOT NULL, quota_date DATE NOT NULL, bucket VARCHAR(32) NOT NULL,
 amount BIGINT NOT NULL CHECK(amount>=0), used BIGINT NOT NULL DEFAULT 0 CHECK(used>=0),
 settled BOOLEAN NOT NULL DEFAULT FALSE, created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 PRIMARY KEY(id,bucket), FOREIGN KEY(quota_date,bucket) REFERENCES quota_buckets(quota_date,bucket),
 CHECK(used<=amount)
);
CREATE INDEX drafts_account ON drafts(account);
