# Privacy and evidence hygiene

The public repository intentionally excludes raw browser captures.

Removed before publication:

- screenshots of the Doubao UI;
- page text dumps containing the account sidebar and unrelated chat titles;
- browser profiles, cookies and tokens;
- raw session metadata that could identify the account.

What remains:

- sanitized run reports;
- model output packages for the synthetic case;
- preflight and grader JSON;
- synthetic data and reference answer.

Before adding new evidence:

1. strip account names, avatars, unrelated conversation titles and URLs with
   query tokens;
2. keep timestamps and model/output hashes;
3. store screenshots outside the public repository unless redacted;
4. never commit `browser/`, cookies, `.env` or API keys.
