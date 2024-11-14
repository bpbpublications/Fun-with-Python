import toga


class MyApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow()
        self.main_window.content = toga.Box(children=[toga.Label("Hello!")])
        self.main_window.show()


if __name__ == "__main__":
    app = MyApp("Realistic App", "org.python.example")
    app.main_loop()
