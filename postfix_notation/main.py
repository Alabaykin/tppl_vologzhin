import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.stack_machine import StackMachine


def main(argv: list[str] | None = None) -> int:
    args = sys.argv if argv is None else argv
    if len(args) < 2:
        print("Похоже, вы не передали выражение для вычисления.")
        print('Пример: python main.py "3 0 4 ~ 2 ~"')
        return 1

    if len(args) > 2 or " " not in args[1].strip():
        print("Пожалуйста, передайте выражение в кавычках.")
        print('Пример: python main.py "3 0 4 ~ 2 ~"')
        return 1

    expression = args[1]

    print(f"Вычисляем выражение: '{expression}'")
    print("Состояние стека на каждом шаге:")

    machine = StackMachine(expression)
    try:
        result = machine.calculate(verbose=True)
        print(f"\n{expression} = {result}")
        return 0
    except ZeroDivisionError as e:
        print(f"\nОшибка вычислений: {e}")
        return 1
    except ValueError as e:
        print(f"\nОшибка в выражении: {e}")
        return 1
    except Exception as e:  # pragma: no cover
        print(f"\nНеожиданная ошибка: {e}")
        return 1


if __name__ == "__main__": # pragma: no cover
    exit_code = main()
    if exit_code != 0:
        sys.exit(exit_code)
