import kivy

from kivy.app import App
from kivy.lang import Builder

kivy.require("1.9.0")

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config

Config.set("graphics", "resizable", 0)


class kivExampleApp(App):
    def build(self):
        return Builder.load_file("kivy_example.kv")


def main():
    calcApp = kivExampleApp()
    return calcApp.run()


main()
