import ast

class CheckResults():
    def __init__(self, answers: dict, module="M4_ML"):
        self.correct_answers = {
            'M4_ML': {
                'R_A1': {
                    "value" : {
                        "answer": 5 
                    } 
                },
                'R_A2': {
                    "value" : {
                        "answer": 30.57 
                    } 
                },
                'R_A3': {
                    "list" : {
                        "answer": ['petal length (cm)', 'petal width (cm)']
                    } 
                },
                'R_B2-1': {
                    "list" : {
                        "answer": [60.3, 20.0, 44.0, 41.0, 42.0]
                    } 
                },
                'R_B2-2': {
                    "value" : {
                        "answer": 60.3
                    } 
                },
                'R_B2-3': {
                    "n_rows": 150, 
                    "n_columns": 5,
                    "check": {
                        "name": 'sepal width (cm)',
                        "val1": 3.5
                    }
                },
                'R_B4-1': {
                    "n_rows": 150, 
                    "n_columns": 3,
                    "check": {
                        "name": 'sepal width (cm)',
                        "val1": 0.625
                    }
                },
                'R_C1': {
                    "n_rows": 150, 
                    "n_columns": 5,
                    "check": {
                        "name": 'state',
                        "val1": 'dry'
                    }
                },
                'R_C2': {
                    "value" : {
                        "answer": 0.9
                    } 
                },
                'R_D1': {
                    "value" : {
                        "answer": 3
                    } 
                }
            }
        }

        self.module = module
        self.answers = answers

        self.everything_correct = True

        # store results
        self.results = {self.module: {}}
        for exercise in self.correct_answers[self.module]:
            self.results[module][exercise] = {
                'exercise_correct': True,
                'hint': None}

        self.check_results()


    def _validate_value(self, exercise, answer):
        correct = self.correct_answers[self.module][exercise]['value']['answer']
        if correct != answer:
            self.everything_correct = False
            self.results[self.module][exercise]['exercise_correct'] = False
            self.results[self.module][exercise]['hint'] = f"{exercise}: Expected {correct}, but got {answer}"


    def _validate_list(self, exercise, answer):
        correct = self.correct_answers[self.module][exercise]['list']['answer']
        if set(correct) != set(answer):
            self.everything_correct = False
            self.results[self.module][exercise]['exercise_correct'] = False
            self.results[self.module][exercise]['hint'] = f"{exercise}: Expected {correct}, but got {answer}"


    def _validate_dataframe(self, exercise, check, answer, indx):
        if check != 'check':
            correct = self.correct_answers[self.module][exercise][check]
        else:
            correct = self.correct_answers[self.module][exercise][check]['val1']

        if correct != answer[indx]:
            self.everything_correct = False
            self.results[self.module][exercise]['exercise_correct'] = False
            self.results[self.module][exercise]['hint'] = f"{exercise}: Expected {check}={correct}, but got {check}={answer}"
    

    def check_results(self):
        for exercise in self.correct_answers[self.module]:
            try:
                result_df = self.answers[exercise]
            except KeyError:
                print(f"{exercise}: Exercise not finished yet")
                continue

            # check if values are correct
            if "value" in self.correct_answers[self.module][exercise]:
                self._validate_value(
                            exercise=exercise,
                            answer=result_df['answer'][0])

            # check if list have similar content
            if "list" in self.correct_answers[self.module][exercise]:
                self._validate_list(
                            exercise=exercise,
                            answer=ast.literal_eval(result_df['answer'][0]))

            # check dataframe values and shape
            if 'n_rows' in self.correct_answers[self.module][exercise]:
                n_rows, n_columns = result_df.shape
                column_name = self.correct_answers[self.module][exercise]['check']['name']
                corresponding_val = result_df[column_name][0]

                answers = [n_rows, n_columns, corresponding_val]

                # check if the rows and columns match the correct answer
                # additional check if first values are similar
                for idx, check in enumerate(['n_rows', 'n_columns', 'check']):
                    if check in self.correct_answers[self.module][exercise]:
                        self._validate_dataframe(
                            exercise=exercise,
                            check=check,
                            answer=answers,
                            indx=idx)

        if self.everything_correct:
            print("Everything seems to be correct. Great work!")