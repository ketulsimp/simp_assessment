from datetime import datetime
import re

def analyze_logs(logs: list[str]):
    if not logs:
        return {
            "error_count": 0,
            "most_common_error_keyword": None,
            "time_span_seconds": 0,
            "levels": {}
        }
    error=0
    for log in logs:
        if "ERROR" in log:
            error+=1
        else:
            continue
    return {"error_count": error}

    
