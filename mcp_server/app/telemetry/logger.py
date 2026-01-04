import json
import logging
from datetime import datetime
from typing import Any, Dict


logger = logging.getLogger("telemetry")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)


def log_event(event: Dict[str, Any]):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        **event,
    }
    logger.info(json.dumps(payload))
