import pytest
from src.stack_machine import StackMachine


class TestStackMachine:
    def test_addition(self):
        s = "3 4 +"
        machine = StackMachine(s)
        assert machine.calculate() == 7

    def test_subtraction(self):
        s = "3 4 -"
        machine = StackMachine(s)
        assert machine.calculate() == -1

    def test_multiplication(self):
        s = "3 4 *"
        machine = StackMachine(s)
        assert machine.calculate() == 12

    def test_division(self):
        s = "3 4 /"
        machine = StackMachine(s)
        assert machine.calculate() == 0.75

    def test_division_integer_result(self):
        s = "8 2 /"
        machine = StackMachine(s)
        res = machine.calculate()
        assert res == 4
        assert isinstance(res, int)

    def test_tilda_without_zero(self):
        s = "3 4 ~"
        machine = StackMachine(s)
        assert machine.calculate() == 1

    def test_tilda_with_zero(self):
        s = "3 0 4 ~ 2 ~"
        machine = StackMachine(s)
        assert machine.calculate() == 47

    def test_float_operands(self):
        s = "2.5 1.5 +"
        machine = StackMachine(s)
        assert machine.calculate() == 4.0

    def test_negative_numbers(self):
        s = "-5 3 +"
        machine = StackMachine(s)
        assert machine.calculate() == -2

    def test_verbose_and_history(self, capsys):
        s = "3 4 +"
        machine = StackMachine(s)
        res = machine.calculate(verbose=True)
        assert res == 7
        assert len(machine.history) == 3
        captured = capsys.readouterr()
        assert "Шаг '+' -> стек: [7]" in captured.out

    def test_empty_expression(self):
        machine = StackMachine("   ")
        with pytest.raises(ValueError, match="Выражение пустое"):
            machine.calculate()

    def test_not_enough_operands(self):
        machine = StackMachine("3 +")
        with pytest.raises(ValueError, match="Не хватает операндов"):
            machine.calculate()

    def test_zero_division(self):
        machine = StackMachine("10 0 /")
        with pytest.raises(ZeroDivisionError):
            machine.calculate()

    def test_invalid_token(self):
        machine = StackMachine("3 4 @")
        with pytest.raises(ValueError, match="Неизвестный токен '@'"):
            machine.calculate()

    def test_leftover_operands(self):
        machine = StackMachine("3 4 5 +")
        with pytest.raises(ValueError, match="в стеке осталось 2 элементов"):
            machine.calculate()