import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.stack_machine import StackMachine


def main():
    if len(sys.argv) < 2:
        print("Похоже, вы не передали выражение для вычисления.")
        sys.exit(1)

    expression = " ".join(sys.argv[1:])

    print(f"Вычисляем выражение: '{expression}'")
    print("Состояние стека на каждом шаге:")

    machine = StackMachine(expression)
    try:
        result = machine.calculate(verbose=True)
        print(f"\n{expression} = {result}")
    except ZeroDivisionError as e:
        print(f"\nВозникла ошибка вычислений: {e}")
        print("Убедитесь, что в операции деления делитель не равен нулю.")
        sys.exit(1)
    except ValueError as e:
        print(f"\nЗамечена неточность в выражении: {e}")
        print("Перепроверьте операнды и операторы.")
        sys.exit(1)
    except Exception as e:
        print(f"\nПроизошла неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
