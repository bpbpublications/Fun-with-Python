"""
Calculator application
"""
import toga
import random
from toga.style import Pack
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW, Pack


def build():
    c_box = toga.Box()
    f_box = toga.Box()
    box = toga.Box()

    c_input = toga.TextInput(readonly=True)
    f_input = toga.TextInput()

    c_label = toga.Label("Celsius", style=Pack(text_align=LEFT))
    f_label = toga.Label("Fahrenheit", style=Pack(text_align=LEFT))
    join_label = toga.Label("is equivalent to", style=Pack(text_align=RIGHT))

    def calculate(widget):
        try:
            c_input.value = (float(f_input.value) - 32.0) * 5.0 / 9.0
        except ValueError:
            c_input.value = "???"

    button = toga.Button("Calculate", on_press=calculate)

    f_box.add(f_input)
    f_box.add(f_label)

    c_box.add(join_label)
    c_box.add(c_input)
    c_box.add(c_label)

    box.add(f_box)
    box.add(c_box)
    box.add(button)

    box.style.update(direction=COLUMN, padding=10)
    f_box.style.update(direction=ROW, padding=5)
    c_box.style.update(direction=ROW, padding=5)

    c_input.style.update(flex=1)
    f_input.style.update(flex=1, padding_left=210)
    c_label.style.update(width=100, padding_left=10)
    f_label.style.update(width=100, padding_left=10)
    join_label.style.update(width=200, padding_right=10)

    button.style.update(padding=15)

    return box


class CalculatorMod:
    def __init__(self, result_widget):
        self.storage_1 = []
        self.storage_2 = []
        self.operator = None
        self.result_widget = result_widget

    def addValue(self, widget):
        if not self.operator and not self.result_widget.value:
            self.storage_1.append(int(widget.text))
        else:
            self.storage_2.append(int(widget.text))

    def click_operator(self, widget):
        if not self.operator:
            self.operator = widget.text

    def calculate(self, widget):
        result = None
        number_1 = int("".join([str(x) for x in self.storage_1]))
        number_2 = int("".join([str(x) for x in self.storage_2]))
        if self.operator == "+":
            result = number_1 + number_2
        elif self.operator == "-":
            result = number_1 - number_2
        elif self.operator == "x":
            result = number_1 * number_2
        elif self.operator == "÷":
            result = number_1 / number_2
        self.show_result(result)

    def show_result(self, result):
        if not result:
            return
        self.result_widget.value = result
        self.storage_1 = [*str(result)]
        self.storage_2 = []
        self.operator = None


def calculator_ui():
    c_box = toga.Box()
    row1_box = toga.Box()
    row2_box = toga.Box()
    row3_box = toga.Box()
    row4_box = toga.Box()
    box = toga.Box()

    result_input = toga.TextInput(readonly=True, style=Pack(background_color="#333333", flex=1))
    storage = CalculatorMod(result_input)
    f_input = toga.TextInput()
    result_label = toga.Label("Result", style=Pack(text_align=RIGHT, flex=1))

    button_7 = toga.Button("7", style=Pack(flex=1), on_press=storage.addValue)
    button_8 = toga.Button("8", style=Pack(flex=1), on_press=storage.addValue)
    button_9 = toga.Button("9", style=Pack(flex=1), on_press=storage.addValue)
    button_x = toga.Button("x", style=Pack(flex=1), on_press=storage.click_operator)

    button_4 = toga.Button("4", style=Pack(flex=1), on_press=storage.addValue)
    button_5 = toga.Button("5", style=Pack(flex=1), on_press=storage.addValue)
    button_6 = toga.Button("6", style=Pack(flex=1), on_press=storage.addValue)
    button__ = toga.Button("-", style=Pack(flex=1), on_press=storage.click_operator)

    button_3 = toga.Button("3", style=Pack(flex=1), on_press=storage.addValue)
    button_2 = toga.Button("2", style=Pack(flex=1), on_press=storage.addValue)
    button_1 = toga.Button("1", style=Pack(flex=1), on_press=storage.addValue)
    button_plus = toga.Button("+", style=Pack(flex=1), on_press=storage.click_operator)

    button_0 = toga.Button("0", style=Pack(flex=1), on_press=storage.addValue)
    button_div = toga.Button("÷", style=Pack(flex=1), on_press=storage.click_operator)
    button_equal = toga.Button("=", style=Pack(flex=1), on_press=storage.calculate)

    c_box.add(result_label)
    c_box.add(result_input)

    row1_box.add(button_7)
    row1_box.add(button_8)
    row1_box.add(button_9)
    row1_box.add(button_x)
    row1_box.style.update(padding=5)

    row2_box.add(button_4)
    row2_box.add(button_5)
    row2_box.add(button_6)
    row2_box.add(button__)
    row2_box.style.update(padding=5)

    row3_box.add(button_1)
    row3_box.add(button_2)
    row3_box.add(button_3)
    row3_box.add(button_plus)
    row3_box.style.update(padding=5)

    row4_box.add(button_0)
    row4_box.add(button_div)
    row4_box.add(button_equal)
    row4_box.style.update(padding=5)

    box.add(c_box)
    box.add(row1_box)
    box.add(row2_box)
    box.add(row3_box)
    box.add(row4_box)

    box.style.update(direction=COLUMN, padding=10)
    return box


def build2():
    c_box = toga.Box()
    box = toga.Box()

    input_field = toga.TextInput()

    def calculate(widget):
        input_field.value = random.randint(1, 500)

    button = toga.Button("Calculate", style=Pack(background_color="#eeeeff"), on_press=calculate)

    c_box.add(button)
    c_box.add(input_field)

    box.add(c_box)
    return box


class calculator(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = calculator_ui()
        self.main_window.show()


def main():
    return calculator()
