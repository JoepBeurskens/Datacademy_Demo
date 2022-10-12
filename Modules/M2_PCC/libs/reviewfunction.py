import os
from sklearn import datasets
import pandas as pd
import matplotlib.pyplot as plt

class ReviewFunction:
    def __init__(self):
        self.working_dir = os.path.join(os.getcwd().split('Datacademy')[0], "Datacademy", "Modules", "M2_PCC", "src")
        self.data_dir = os.path.join(os.getcwd().split('Datacademy')[0], "Datacademy", "data", "M2_PCC")

        self.data = datasets.load_diabetes()
        self.n_features = self.data.data.shape[1]
        self.input_columns = ['column_' + str(i) for i in range(self.n_features)]
        self.pandas_data = pd.DataFrame(self.data.data, columns=self.input_columns)


    def check_answer(self, answer, exercise):
        if len(exercise) == 2:
            if exercise[0] == "B":
                self.check_B(answer, exercise)
            elif exercise[0] == "C":
                self.check_C(answer, exercise)
            elif exercise[0] == "E":
                self.check_E(answer, exercise)
            else:
                print("You didn't specify a correct exercise reference.")
        else:
            print("You didn't specify a correct exercise reference.")


    def check_B(self, ans, ex):
        if ex[1] == "1":
            if ans < 70.66:
                return "Incorrect, a Boeing 747-100 is larger."
            elif ans > 70.66:
                return "Incorrect, a Boeing 747-100 is smaller."
            else:
                return "Correct! A Boeing 747-100 is indeed 70.66 meters."
        
        if ex[1] == "2":
            if ans < 146.7:
                return "Incorrect, an Iphone 12 is larger."
            elif ans > 146.7:
                return "Incorrect, an Iphone 12 is smaller."
            else:
                return "Correct! An Iphone 12 is indeed 146.7 millimeters."
        
        if ex[1] == "3":
            if ans == True:
                return "Correct! The more you know."
            else:
                return "Incorrect! You might want to check your math once more"
        
        if ex[1] == "4":
            if ans == False:
                return "Correct! They call it an 'upgrade'."
            else:
                return "Incorrect! Bigger is not always better."
        
        if ex[1] == "5":
            if ans == "Yes" or ans == "yes" or ans == "YES" or ans == "Y" or ans == "y":
                return "Incorrect! Make sure to use the variables created in B1 and B2 correctly."
            elif ans == "No" or ans == "no" or ans == "NO" or ans == "N" or ans == "n":
                return "Correct!"
            else:
                return "We could not recognize your answer, make sure it follows the given format."
        

    def check_C(self, ans, ex):
        if ex[1] == "1":
            if type(ans) != list:
                return "You messed with my code, damn it."
            else:
                if ans == [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33]:
                    return "Correct! These are indeed the right numbers!"
                else:
                    return "Incorrect! Return only the values where the modulus is 0."
        
        if ex[1] == "2":
            if type(ans) != list:
                return "Did you again mess with my code?!"

            else:
                if ans == [[-5, 23.0], [0, 32.0], [5, 41.0], [10, 50.0], [15, 59.0], [20, 68.0], [25, 77.0], [30, 86.0], [35, 95.0], [40, 104.0], [45, 113.0]]:
                    return "Correct! These temperatures match!"
                else:
                    return "Incorrect! Do you have the right calculation?."
        
        if ex[1] == "3":
            if type(ans) != list:
                return "Please stop messing around with my code!"

            else:
                if ans == [9, 8, 7, 6, 5, 4]:
                    return "Correct!"
                else:
                    return "Incorrect! Try again."
        
        if ex[1] == "4":
            if type(ans) != list:
                return "Please stop messing around with my code!"

            else:
                if ans == [7.5, 15.0, 30.0]:
                    return "Correct!"
                else:
                    return "Incorrect! Try again."
 

    def check_E(self, ans, ex):
        if ex[1] == "5":
            d = {'column_1': [0.050680, -0.044642], 'column_2': [-0.034821, -0.019163]}
            return print(pd.DataFrame(data=d).head(2))

        if ex[1] == "6":
            X = self.review.data.target
            Y = ans['column_1'].tolist()
            Y1 = ans['column_2'].tolist()

            plt.scatter(X, Y, color="green", label="Column 1")
            plt.scatter(X, Y1, color="red", label="Column 2")

            plt.ylim(-0.25,0.25)

            plt.title("My first plot of column 1 and 2", fontsize=20)
            plt.xlabel('x-axis')
            plt.ylabel('y-axis')

            plt.legend(loc='upper right')
            plt.show()
