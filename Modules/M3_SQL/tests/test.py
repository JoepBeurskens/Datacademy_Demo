from Modules.M3_SQL.tests.validate_results import CheckResults
import os
import pandas as pd

answers_dir = "./Modules/M3_SQL/answers"

exercises = [f for f in os.listdir(answers_dir) if ".csv" in f]
exercises.sort()

answers_dict = {}

for exercise in exercises:
    exercise_df = pd.read_csv(os.path.join(answers_dir, exercise), sep=";")
    exercise_name = f"R_{exercise.split('.')[0]}"
    answers_dict[exercise_name] = exercise_df



results = CheckResults(answers=answers_dict, module="M3_SQL")


def test_results():
    for module in results.results:
        for exercise in results.results[module]:
            assert results.results[module][exercise]['exercise_correct'], results.results[module][exercise]['hint']