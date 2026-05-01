from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from uuid import uuid4

DATA_DIR = Path('.runtime')
DATA_DIR.mkdir(exist_ok=True)

_RETRIEVAL_LOG = DATA_DIR / 'retrieval_logs.jsonl'
_ANSWER_AUDIT = DATA_DIR / 'answer_audits.jsonl'
_NOTICE_AUDIT = DATA_DIR / 'notice_audits.jsonl'
_LOCK = Lock()


def _append(path: Path, payload: dict) -> None:
    with _LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(payload, ensure_ascii=False) + '\n')


def write_retrieval_log(payload: dict) -> str:
    log_id = str(uuid4())
    entry = {"log_id": log_id, **payload}
    _append(_RETRIEVAL_LOG, entry)
    return log_id


def write_answer_audit(payload: dict) -> str:
    audit_id = str(uuid4())
    entry = {"audit_id": audit_id, **payload}
    _append(_ANSWER_AUDIT, entry)
    return audit_id


def write_notice_audit(payload: dict) -> str:
    notice_audit_id = str(uuid4())
    entry = {"notice_audit_id": notice_audit_id, **payload}
    _append(_NOTICE_AUDIT, entry)
    return notice_audit_id
