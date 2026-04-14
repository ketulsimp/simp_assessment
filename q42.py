import datetime 
import re
from collections import defaultdict,Counter


logs = ["2026-04-10 14:32:01 ERROR Database connection timeout",

"2026-04-10 14:32:05 WARNING Memory usage at 85%",

"2026-04-10 14:33:12 ERROR Disk write failure",

"2026-04-10 14:33:45 INFO Server restarted",

"2026-04-10 14:34:00 ERROR Connection refused"]

def analyze_logs(logs: list[str]) -> dict:
    if len(logs)==0:
        return "No logs to analyze"
    pattern = r'^\d{4}-\d{2}-\d{2} (\d{2}:\d{2}:\d{2}) (\w+) ([\w\s]+)'
    extraction = re.findall(pattern,"2026-04-10 14:32:01 ERROR Database connection timeout")
    log_levels = defaultdict(int)
    keywords = defaultdict(int)
    min_time = None
    max_time = None
    for log in logs:
        time,type_of_error,msg = re.findall(pattern,log)[0]
        log_levels[type_of_error] += 1
        if type_of_error == "ERROR":
            for word in msg.split():
                keywords[word.lower()] += 1
        true_time = datetime.datetime.strptime(time,"%H:%M:%S")
        if min_time is None:
            min_time = true_time
        else:
            min_time = min(min_time,true_time)
        if max_time is None:
            max_time = true_time
        else:
            max_time = max(max_time,true_time)
        
    result = {
        'error_count': log_levels['ERROR'],
        'most_common_error_keyword': sorted(keywords)[0],
        "timespan_seconds": (max_time-min_time).seconds,
        "levels": dict(log_levels.items())
    }
    return result
        
print(analyze_logs([]))
print(analyze_logs(logs))
