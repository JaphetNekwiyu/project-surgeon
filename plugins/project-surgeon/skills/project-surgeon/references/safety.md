# Safety policy

Do not change production-sensitive code without explicit scoped permission: money, taxes, invoices, ledgers, reconciliation, payments, auth/MFA, permissions, RLS, database migrations, storage, environment, deployment, scheduled jobs, legal or regulatory evidence. Never delete historical migrations or audit events.

Never read secret files solely for an audit, leak credential contents, access production services, overwrite a dirty worktree, run destructive Git commands or make unrequested external calls. An apparent dead-code result is not proof. Audit and performance modes remain read-only.

Preserve contracts, runtime behavior, error handling, logging, tenant isolation and idempotency. Verify each change against an established test baseline.
