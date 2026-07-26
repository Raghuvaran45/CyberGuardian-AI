import pandas as pd

from engine.root_cause import analyze_root_cause


sample = pd.DataFrame({

    "night_login":[1],

    "office_hours":[0],

    "failed_login_attempts":[8],

    "long_session":[1],

    "short_session":[0],

    "login_status":[0],

    "device_fingerprint":[0],

    "command_sequence":[22],

    "geo_location":[8]

})


reasons = analyze_root_cause(sample)


print("="*60)

print("ROOT CAUSE ANALYSIS")

print("="*60)


for reason in reasons:

    print("✓", reason)