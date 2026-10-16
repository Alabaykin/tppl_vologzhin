import pytest
from src import postfix_module

class TestPostfix:
    def test_addition(self):
        s = "3 4 +"
        assert postfix_module.calculate(s) == 7

    def test_subtraction(self):
        s = "3 4 -"
        assert postfix_module.calculate(s) == -1

    def test_multiplication(self):
        s = "3 4 *"
        assert postfix_module.calculate(s) == 12

    def test_division(self):
        s = "3 4 /"
        assert postfix_module.calculate(s) == 0.75
    
    def test_tilda_without_zero(self):
        s = "3 4 ~"
        assert postfix_module.calculate(s) == 1

    def test_tilda_with_zero(self):
        s = "3 0 4 ~ +"
        assert postfix_module.calculate(s) == 52