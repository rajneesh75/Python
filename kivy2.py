from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class MyApp(App):
    def build(self):
        self.label = Label(text="Welcome to Kivy!", font_size=20)

        btn = Button(
            text="Click Me 👆",
            font_size=18,
            size_hint=(1, 0.3)
        )
        btn.bind(on_press=self.on_button_click)

        layout = BoxLayout(orientation='vertical', padding=20)
        layout.add_widget(self.label)
        layout.add_widget(btn)

        return layout

    def on_button_click(self, instance):
        self.label.text = "Button clicked! 🚀"


# Run the app
if __name__ == "__main__":
    MyApp().run()
