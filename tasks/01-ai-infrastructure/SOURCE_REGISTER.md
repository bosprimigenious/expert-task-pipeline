# Task 01 — Source register

Capture date: 2026-11-11. Source discovery only; not a dataset lock.

| ID | Source | Facts verified | License / reuse | Decision |
|---|---|---|---|---|
| S01 | Microsoft Research, https://github.com/msr-fiddle/philly-traces | Sanitized first-party DNN training trace; 117,325 jobs; 2017-08-07 to 2017-12-22; five data files; job attempts, GPU/CPU/memory utilization and machine inventory | GitHub repository metadata reports CC-BY-4.0. Attribute Jeon et al., ATC 2019 and source repo; mark modifications | License confirmed; data not acquired |
| S02 | Alibaba Cluster Trace Program, https://github.com/alibaba/clusterdata/tree/master/cluster-trace-v2026-maas | Six-month anonymized production LLM inference trace; daily 145,083,117 rows / 61 shards; weekly 140,906,827 rows / 21 shards; app metrics 7,401 rows | Repository metadata has no license identifier. Dataset-specific terms and platform permission require review | Public source; authorization conditional |
| S03 | Alibaba schema, https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2026-maas/docs/schema.md | Daily/weekly/app fields, time windows, null semantics, joins and metric definitions | Documentation citation and attribution; do not infer data redistribution rights | Schema reference accepted |
| S04 | Alibaba download guide, https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2026-maas/docs/data_download.md | Daily archive 10,528,173,427 bytes; weekly archive 4,812,189,789 bytes; app metrics archive 99,947 bytes | Archive redistribution terms conditional | Acquisition spec accepted |
| S05 | Jeon et al., https://www.usenix.org/conference/atc19/presentation/jeon | Philly workload context: gang scheduling, locality constraints, queuing, GPU utilization and training failures | Research context only, not raw trace data | Background accepted |

## Schema and analysis constraints
- Philly and Alibaba are independent populations; no cross-dataset row joins.
- Philly jobs may have no attempts; attempt start/end times may be missing; a null final end time may mean still running.
- Philly NA utilization means offline, not zero.
- Alibaba daily records may contain multiple instance segments per day; GPU-hours are additive.
- Alibaba gpu_count is allocated GPU equivalents and may be fractional.
- Alibaba gpu_hours is segment allocated GPU time, not instantaneous utilization.
- Alibaba sm_util is normalized by allocated GPU equivalents.
- Alibaba weekly records are five-minute windows [time_s, time_s+300).
- Alibaba series_id is a monitoring-series ID, not an instance ID.
- Alibaba qps_norm is normalized; absolute QPS is not released.
- Daily/weekly association requires a deduplicated (instance_id, day, workload) mapping. App metrics associate by app_id and gpu_type, not series_id to instance.

## Provenance fields still required
For each acquired file: canonical URL, UTC retrieval timestamp, final URL, HTTP status, byte size, ETag/Last-Modified if supplied, archive CRC, SHA-256, extracted path, row count, schema fingerprint, null profile and license notice.