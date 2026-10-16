

class StackMachine:
    OPERATORS = {"+", "-", "/", "*", "~"}

    def __init__(self, expression: str):
        self.expression = expression
        self.stack: list[int | float] = []
        self.history: list[str] = []

    def calculate(self, verbose: bool = False) -> int | float:
        tokens = self.expression.strip().split()
        if not tokens:
            raise ValueError("Выражение пустое. Пожалуйста, передайте корректное выражение.")

        self.stack.clear()
        self.history.clear()

        for token in tokens:
            if token in self.OPERATORS:
                if len(self.stack) < 2:
                    raise ValueError(
                        f"Не хватает операндов для операции '{token}', "
                        f"найдено {len(self.stack)} ( стек: {self.stack})."
                    )

                r = self.stack.pop()
                l = self.stack.pop()

                match token:
                    case "+":
                        self.stack.append(l + r)
                    case "-":
                        self.stack.append(l - r)
                    case "*":
                        self.stack.append(l * r)
                    case "/":
                        if r == 0:
                            raise ZeroDivisionError("Попытка деления на ноль, проверьте делитель.")
                        div_res = l / r
                        self.stack.append(int(div_res) if div_res.is_integer() else div_res)
                    case "~":
                        if l != 0 and r != 0:
                            self.stack.append(abs(l - r))
                        else:
                            total = sum(self.stack) + l + r
                            self.stack.clear()
                            self.stack.append(total ** 2)
            else:
                try:
                    if "." in token:
                        self.stack.append(float(token))
                    else:
                        self.stack.append(int(token))
                except ValueError:
                    raise ValueError(
                        f"Неизвестный токен '{token}'. Поддерживаются только числа и операторы: {', '.join(sorted(self.OPERATORS))}."
                    )

            step_str = f"Шаг '{token}' -> стек: {self.stack}"
            self.history.append(step_str)
            if verbose:
                print(step_str)

        if len(self.stack) != 1:
            raise ValueError(
                f"Некорректное выражение: после завершения вычислений в стеке осталось {len(self.stack)} элементов: {self.stack}. "
            )

        return self.stack[-1]
