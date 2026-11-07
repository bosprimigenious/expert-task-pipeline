# Open-source scope

## Included

- pipeline documentation and failure analysis;
- the synthetic POWER-PERF case;
- public input packs and model-visible prompts;
- reference answer, rubric, grader and preflight (as an author-side example);
- run evidence and preflight reports;
- MIT-licensed tooling.

## Excluded

- browser profiles, cookies, tokens, credentials;
- real customer/employer data;
- private platform exports or account data;
- raw DSH transcripts;
- any claim of platform acceptance.

## Why the answer is included

The case is synthetic and is published as a **worked failure case**, not as a
live contest task. The private answer is included so readers can reproduce the
grader and see why the runs failed. If you reuse the task as a live evaluation,
remove `03_private_review/` from the model-visible pack.

## Synthetic label

The company, records and documents are synthetic. Do not present them as a real
utility’s records. The platform’s real-work rule is not satisfied by this
example alone.
