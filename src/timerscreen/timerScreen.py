from datetime import datetime, timedelta
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ColorProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


class TimerScreen(Screen):
    button_text = StringProperty('START')
    button_color = ColorProperty((0, 1, 0, 1))
    pb_value = NumericProperty(0)
    start_time = datetime.now()
    start_time_label = StringProperty(start_time.strftime('%H:%M'))
    time = datetime(1, 1, 1, 0, 0, 0)
    time_label = StringProperty(time.strftime('%Hh %Mmin %Ss'))

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.time_state = 'stopped'
        self.work_clock = Clock

        self.cpb = CircularProgressBar(
            size_hint=(None, None),
            size=(100, 100)
        )

        self.ids.semester_prog.add_widget(self.cpb)

    def toggle(self):
        if self.time_state == 'stopped':
            self.cpb.set_value(0.4)
            self.time_state = 'running'
            self.button_text = 'STOP'
            self.button_color = (1, 0, 0, 1)

            self.start_time = datetime.now()
            self.start_time_label = self.start_time.strftime('%H:%M')

            self.work_clock = Clock.schedule_interval(self.update_clock, 1)

        else:
            self.time_state = 'stopped'
            self.button_text = 'START'
            self.button_color = (0, 1, 0, 1)
            self.work_clock.cancel()

    def update_clock(self, *args):
        self.time = self.time + timedelta(seconds=1)
        self.time_label = self.time.strftime('%Hh %Mmin %Ss')


class CircularProgressBar(Widget):
    thickness = 30
    value_normalized = NumericProperty(0.2)
    label_text = StringProperty("%")
    max = 100

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        self.label_text = str(int(self.value_normalized * 100)) + "%"

    def set_value(self, value):
        self.value_normalized = value

        self.label_text = str(int(self.value_normalized * 100)) + "%"
