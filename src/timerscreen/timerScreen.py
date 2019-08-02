from kivy.properties import NumericProperty, StringProperty, ColorProperty
from kivy.uix.screenmanager import Screen


class TimerScreen(Screen):
    button_text = StringProperty('START')
    button_color = ColorProperty((0, 1, 0, 1))
    pb_value = NumericProperty(0)

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.time_state = 'stopped'

    def toggle(self):
        if self.time_state == 'stopped':
            self.time_state = 'running'
            self.button_text = 'STOP'
            self.button_color = (1, 0, 0, 1)
            self.pb_value = self.pb_value + 5
        else:
            self.time_state = 'stopped'
            self.button_text = 'START'
            self.button_color = (0, 1, 0, 1)
