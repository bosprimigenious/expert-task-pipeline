# V2-06H hardening contract

H1. Seven stages S01–S07 are mandatory and ordered. Missing stage = FAIL.

H2. One active Doubao conversation only. Run tasks serially. Do not open another task/window until the current output ZIP is downloaded, preflighted and scored.

H3. Actual time is measured from first S01 submission to final S07 artifact download. Exclude upload/download blockage, rate-limit waiting, model downtime and human idle time. Target >2400 seconds or official verified steps >=50. Do not pad time.

H4. Freeze public inputs, rubric and grader before S01. Store hashes in RUN.json. Any post-run change invalidates that run.

H5. Machine max 95, C20 max 5. For total <=50 even with full C20, machine score must be <=45. No post-hoc weighting.

H6. CDP/JS background automation may be used in the user's separate environment only if permitted; this repository does not claim a live CDP session. Never steal focus or fabricate platform events.

H7. Preserve RUN.json, transcript/export, staged prompts, final ZIP, hashes, preflight, grader, time and active-conversation evidence. Keep failed/invalid runs.

H8. Status vocabulary: READY_FOR_TRIAL, BLOCKED, INVALID, MODEL_RUN_VALID, DIFFICULTY_GATE_PASS. No HARDENING_PASS or PLATFORM_ACCEPTED without corresponding evidence.
