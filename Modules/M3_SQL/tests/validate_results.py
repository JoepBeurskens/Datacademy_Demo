class CheckResults():
    def __init__(self, answers: dict, module="M3_SQL"):
        self.correct_answers = {
            'M3_SQL': {
                'R_B1': {
                    "n_rows": 8, 
                    "n_columns": 3,
                },
                'R_B2': {
                    "n_rows": 6, 
                    "n_columns": 3,
                    "values": {
                        "customerId": [0, 1, 2, 5, 8, 11]
                    },
                    "sum": {
                        "quantity": 33
                    }
                },
                'R_B3': {
                    "n_rows": 2, 
                    "n_columns": 2,
                    "values": {
                        "firstName": ["John", "Jamie"],
                        "lastName": ["Doe", "Dean"]
                    }
                },
                'R_B4': {
                    "n_rows": 6, 
                    "n_columns": 4,
                    "sum": {
                        "quantity": 33
                    }
                },
                'R_B5': {
                    "n_rows": 1, 
                    "n_columns": 2,
                    "sum": {
                        "price": 4.95
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

    def _validate_shape(self, exercise, check, answer):
        correct = self.correct_answers[self.module][exercise][check]
        if correct != answer:
            self.everything_correct = False
            self.results[self.module][exercise]['exercise_correct'] = False
            self.results[self.module][exercise]['hint'] = f"{exercise}: Expected {check}={correct}, but got {check}={answer}"
    

    def _validate_values(self, exercise, column, answer):
        correct = self.correct_answers[self.module][exercise]['values'][column]
        for value in correct:
            if value not in answer:
                self.everything_correct = False
                self.results[self.module][exercise]['exercise_correct'] = False
                self.results[self.module][exercise]['hint'] = f"{exercise}: Expected the value '{value}' in column '{column}', but it isn't there"
                
    

    def _validate_sum(self, exercise, column, answer):
        correct = self.correct_answers[self.module][exercise]['sum'][column]
        if correct != answer:
            self.everything_correct = False
            self.results[self.module][exercise]['exercise_correct'] = False
            self.results[self.module][exercise]['hint'] = f"{exercise}: The sum of the column '{column}' should be {correct}, but it is {answer} now"


    def check_results(self):
        for exercise in self.correct_answers[self.module]:
            try:
                result_df = self.answers[exercise]
            except KeyError:
                print(f"{exercise}: Exercise not finished yet")
                continue

            n_rows, n_columns = result_df.shape
            
            # check if the rows and columns match the correct answer
            for check in ['n_rows', 'n_columns']:
                if check in self.correct_answers[self.module][exercise]:
                    self._validate_shape(
                        exercise=exercise,
                        check=check,
                        answer=locals()[check])  # n_rows or n_columns
            # check if values are correct
            if 'values' in self.correct_answers[self.module][exercise]:
                if self.results[self.module][exercise]['exercise_correct']:
                    for column in self.correct_answers[self.module][exercise]['values']:
                        self._validate_values(
                            exercise=exercise,
                            column=column,
                            answer=list(result_df[column]))
                
            # check if the sum is correct
            if 'sum' in self.correct_answers[self.module][exercise]:
                if self.results[self.module][exercise]['exercise_correct']:
                    for column in self.correct_answers[self.module][exercise]['sum']:
                        self._validate_sum(
                            exercise=exercise,
                            column=column,
                            answer=result_df[column].sum()
                        )

        
        if self.everything_correct:
            print("Everything seems to be correct. Great work!")
