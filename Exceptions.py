class IncorrectBoardSizeException(Exception):
    def __init__(self, n, m):
        super().__init__("Board size {} x {} are Incorrect".format(n, m))


class IncorrectMineAmountException(Exception):
    def __init__(self, q):
        super().__init__("Amount {} of Mines is incorrect".format(q))


class AnotherDataValidationException(Exception):
    def __init__(self, text):
        super().__init__(text)
