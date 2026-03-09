class CalorieCalculator:

    @staticmethod
    def progress(total,goal):

        if goal == 0:
            return 0

        return min((total/goal) * 100,100)
