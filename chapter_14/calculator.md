# init

```bash
$ briefcase new
```

# source

```python
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class calculator(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()


def main():
    return calculator()
```


# UI

## add button
use app name calculator

## udpate app

```bash
$ vim src/calulator/app.py
```

# layout

## buttons

```python
import toga

def build():
    c_box = toga.Box()
    box = toga.Box()

    input_field = toga.TextInput()
    button = toga.Button("Calculate")

    c_box.add(button)
    c_box.add(input_field)

    box.add(c_box)
    return box

class main_app(toga.App):
    def startup(self):
        main_ui= build()

        self.main_window = toga.MainWindow(title="test application")
        self.main_window.content = main_ui
        self.main_window.show()
```

## add colors

```python
from toga.style import Pack
from toga.style.pack import LEFT

button = toga.Button("Calculate", style=Pack(background_color="#eeeeff", text_align=LEFT))
```
## add action

```python
import ranodom
from toga.style import Pack
from toga.style.pack import LEFT


def calculate(widget):
    return random.randint(1, 500)

button = toga.Button("Calculate", style=Pack(background_color="#eeeeff"), on_press=calculate)
```

## action result

```python
import ranodom
from toga.style import Pack
from toga.style.pack import LEFT


def build():
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
```

## button with callback for calucalor

```python
result_input = toga.TextInput(readonly=True, style=Pack(background_color="#333333", flex=1))
storage = CalculatorMod(result_input)
button_7 = toga.Button("7", style=Pack(flex=1), on_press=storage.addValue)
```
