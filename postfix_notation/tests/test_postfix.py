import os
import sys
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src import StackMachine
import main


class TestOperations:
    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("2 3 +", 5),
            ("2.5 3.5 +", 6),
            ("-5 3 +", -2),
            ("10 4 -", 6),
            ("4 10 -", -6),
            ("5.5 0.5 -", 5),
            ("3 4 *", 12),
            ("2.5 2 *", 5),
            ("-2 3 *", -6),
            ("10 2 /", 5),
            ("7 2 /", 3.5),
            ("8 2 /", 4),
        ],
        ids=[
            "sum_ints",
            "sum_floats",
            "sum_negatives",
            "sub_positive",
            "sub_negative",
            "sub_floats",
            "mul_positive",
            "mul_floats",
            "mul_negative",
            "div_exact",
            "div_float_result",
            "div_int_result",
        ],
    )
    def test_binary_operations(self, expression, expected):
        machine = StackMachine(expression)
        assert machine.calculate() == expected

    def test_division_by_zero(self):
        machine = StackMachine("5 0 /")
        with pytest.raises(ZeroDivisionError, match="деления на ноль"):
            machine.calculate()

    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("3 8 ~", 5),
            ("2 5 ~", 3),
            ("3 0 4 ~", 49),
            ("0 4 ~", 16),
            ("4 0 ~", 16),
            ("2 1 5 0 ~", 64),
            ("0 0 ~", 0),
        ],
        ids=[
            "diff_positive",
            "diff_order_abs",
            "zero_operand_including_stack_and_operands",
            "zero_first_operand_sum_squared",
            "zero_second_operand_sum_squared",
            "zero_with_multi_element_stack",
            "both_zeros",
        ],
    )
    def test_calc_tilde_valid(self, expression, expected):
        machine = StackMachine(expression)
        assert machine.calculate() == expected

    @pytest.mark.parametrize(
        "expression",
        ["~", "1 ~"],
        ids=["empty_stack", "single_element"],
    )
    def test_calc_tilde_insufficient_operands(self, expression):
        machine = StackMachine(expression)
        with pytest.raises(ValueError, match="Не хватает операндов"):
            machine.calculate()


class TestEvaluation:
    @pytest.mark.parametrize(
        "expression, expected",
        [
            ("3 0 4 ~ 2 ~", 47),
            ("2 2 + 4 - 4 ~ 2 3 * +", 22),
            ("5 1 2 + 4 * + 3 -", 14),
            ("15 3 / 2 +", 7),
            ("4 2 / 2 /", 1),
            ("10 2 - 3 -", 5),
            ("2.5 1.5 +", 4),
            ("-5 3 +", -2),
        ],
        ids=[
            "task_case_1",
            "task_case_2",
            "combined_arithmetic",
            "div_and_add",
            "chained_division",
            "chained_subtraction",
            "float_conversion_to_int",
            "negative_arithmetic",
        ],
    )
    def test_evaluate_expression_valid(self, expression, expected):
        machine = StackMachine(expression)
        assert machine.calculate(verbose=False) == expected

    @pytest.mark.parametrize(
        "expression, exc_type, match",
        [
            ("   ", ValueError, "Выражение пустое"),
            ("2 3 & +", ValueError, "Неизвестный токен"),
            ("2 +", ValueError, "Не хватает операндов"),
            ("~", ValueError, "Не хватает операндов"),
            ("1 2 3 +", ValueError, "осталось 2 элементов"),
            ("10 0 /", ZeroDivisionError, "деления на ноль"),
            ("/home/user 2 +", ValueError, "похож на путь"),
            (r"C:\Users\user 2 +", ValueError, "похож на путь"),
            ("main.py 2 +", ValueError, "похож на имя файла"),
        ],
        ids=[
            "empty",
            "unknown_op",
            "missing_operands_binary",
            "missing_operands_tilde",
            "stack_too_large_at_end",
            "div_zero",
            "expanded_tilde_path_unix",
            "expanded_tilde_path_windows",
            "expanded_file_token",
        ],
    )
    def test_evaluate_expression_errors(self, expression, exc_type, match):
        machine = StackMachine(expression)
        with pytest.raises(exc_type, match=match):
            machine.calculate(verbose=False)

    def test_verbose_output(self, capsys):
        machine = StackMachine("2 3 +")
        res = machine.calculate(verbose=True)
        assert res == 5
        assert len(machine.history) == 3
        captured = capsys.readouterr()
        assert "Шаг '2' -> стек: [2]" in captured.out
        assert "Шаг '3' -> стек: [2, 3]" in captured.out
        assert "Шаг '+' -> стек: [5]" in captured.out


class TestCLI:
    @pytest.mark.parametrize(
        "args, expected_code, expected_output",
        [
            ([], 1, "вы не передали выражение"),
            (["3", "0", "4", "~", "2", "~"], 1, "передайте выражение в кавычках"),
            (["3"], 1, "передайте выражение в кавычках"),
            (["3 0 4 ~ 2 ~"], 0, "3 0 4 ~ 2 ~ = 47"),
            (["2 2 + 4 - 4 ~ 2 3 * +"], 0, "2 2 + 4 - 4 ~ 2 3 * + = 22"),
            (["10 0 /"], 1, "Ошибка вычислений"),
            (["invalid_token 2 +"], 1, "Неизвестный токен"),
            (["/home/user 2 +"], 1, "похож на путь"),
            (["main.py 2 +"], 1, "похож на имя файла"),
        ],
        ids=[
            "no_args",
            "unquoted_multi_tokens",
            "unquoted_single_token",
            "task_ex1",
            "task_ex2",
            "div_by_zero",
            "invalid_tok",
            "path_expansion",
            "file_expansion",
        ],
    )
    def test_main_cli_args(self, args, expected_code, expected_output, capsys):
        code = main.main(["main.py"] + args)
        assert code == expected_code
        captured = capsys.readouterr()
        assert expected_output in captured.out

    def test_main_default_sys_argv(self, capsys):
        sys.argv = ["main.py", "2 3 +"]
        code = main.main()
        assert code == 0
        captured = capsys.readouterr()
        assert "2 3 + = 5" in captured.out