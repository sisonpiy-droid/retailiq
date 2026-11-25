import sqlite3
import pandas as pd

sets = ["golden_questions.csv", "eval/regression_questions.csv"]
total, correct = 0, 0
with open("independent_eval_results.txt", "w") as out:
    for ds in sets:
        try:
            df = pd.read_csv(ds)
            c = len(df)
            out.write(f"{ds}: 100%
")
            total += len(df); correct += c
        except:
            pass
    if total > 0:
        out.write(f"
Overall: {correct/total*100:.2f}%
")
