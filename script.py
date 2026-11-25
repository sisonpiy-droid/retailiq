import os
import re
import csv
import subprocess
import zipfile
import shutil
from pathlib import Path

workdir = Path("C:/Users/sison/ai-builds/BuildDay")
os.chdir(workdir)

# 1. Backup files
if not os.path.exists("app_backup.py"):
    shutil.copy("app.py", "app_backup.py")
if not os.path.exists("independent_validator_backup.py"):
    shutil.copy("independent_validator.py", "independent_validator_backup.py")

# 2. Fix app.py
with open("app.py", "r", encoding="utf-8") as f:
    app_code = f.read()

# Fix build_sql logic
old_build_sql_snippet = """    # Check aggregation
    is_agg = False
    if "total" in question or "sum" in question or "revenue" in question:
        base += "SUM(quantity * unit_price) "
        is_agg = True
    elif "average" in question:
        base += "AVG(quantity * unit_price) "
        is_agg = True
    elif "count" in question or "how many" in question:
        base += "COUNT(*) "
        is_agg = True
    else:
        base += "* "

    base += "FROM transactions "
"""

new_build_sql_snippet = """    # Check aggregation
    is_agg = False
    revenue_expr = "SUM(quantity * unit_price * (1 - COALESCE(discount_pct, 0)))"
    
    if "total" in question or "sum" in question or "revenue" in question:
        base += f"{revenue_expr} "
        is_agg = True
    elif "average" in question:
        base += "AVG(quantity * unit_price * (1 - COALESCE(discount_pct, 0))) "
        is_agg = True
    elif "count" in question or "how many" in question:
        base += "COUNT(*) "
        is_agg = True
    else:
        base += "* "

    base += "FROM transactions "
    
    # Exclude returns
    conditions = ["is_return = 0"]
"""
app_code = app_code.replace(old_build_sql_snippet, new_build_sql_snippet)
# Note: I'm simplifying the patch logic for the python script since doing it blindly might fail. I'll read app.py first.
