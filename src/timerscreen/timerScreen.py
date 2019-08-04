import kivy
from datetime import datetime, time, timedelta
from functools import partial
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, ColorProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


class TimerScreen(Screen):
    @staticmethod
    def time_str(time, hour, min, sec, format):
        time_str = ''
        if hour:
            if format == 'day_time':
                time_str = time_str + str(time.hour % 24)
            elif format == 'timer':
                time_str = time_str + str(time.hour % 24) + 'h'
        if min:
            if format == 'day_time':
                time_str = time_str + ':' + str(time.minute % 60)
            elif format == 'timer':
                time_str = time_str + ' ' + str(time.minute % 60) + 'min'
        if sec:
            if format == 'day_time':
                time_str = time_str + ':' + str(time.second % 60)
            elif format == 'timer':
                time_str = time_str + ' ' + str(time.second % 60) + 's'

        return time_str

    button_text = StringProperty('START')
    button_color = ColorProperty((0, 1, 0, 1))

    work_time = time(0, 0, 0)
    work_time_label = StringProperty(time_str.__func__(work_time, True, True, True, 'timer'))

    down_time = time(0, 0, 0)

    start_time = datetime.now()
    start_time_label = StringProperty(time_str.__func__(start_time, True, True, False, 'day_time'))

    pb_value = NumericProperty(0)

    daily_target = time(8, 0, 0)
    daily_target_label = StringProperty(time_str.__func__(daily_target, True, True, False, 'timer'))

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        self.time_state = 'stopped'
        self.work_clock = Clock
        self.down_clock = Clock

        self.cpb = self.ids.cpb
        self.cpb.update()

    def toggle(self):
        if self.time_state == 'stopped':
            self.time_state = 'running'
            self.button_text = 'STOP'
            self.button_color = (1, 0, 0, 1)

            if self.get_time_sec(self.down_time) >= self.get_time_sec(time(0, 15, 0)):
                self.work_time = time(0, 0, 0)
                self.work_time_label = self.time_str(self.work_time, True, True, True, 'timer')
                self.start_session_start()
            elif self.get_time_sec(self.down_time) == self.get_time_sec(time(0, 0, 0)):
                self.start_session_start()

            self.down_time = time(0, 0, 0)

            if type(self.down_clock) is kivy._clock.ClockEvent:
                self.down_clock.cancel()

            self.work_clock = Clock.schedule_interval(partial(self.update_clock, 'work'), 1)

        elif self.time_state == 'running':
            self.time_state = 'stopped'
            self.button_text = 'START'
            self.button_color = (0, 1, 0, 1)

            self.work_clock.cancel()

            self.down_clock = Clock.schedule_interval(partial(self.update_clock, 'down'), 1)

    def update_clock(self, work_or_down, *args):
        if work_or_down == 'work':
            self.work_time = (datetime(1, 1, 1, self.work_time.hour, self.work_time.minute, self.work_time.second)
                              + timedelta(seconds=1)).time()
            self.work_time_label = self.time_str(self.work_time, True, True, True, 'timer')
            self.update_pb()
        elif work_or_down == 'down':
            self.down_time = (datetime(1, 1, 1, self.down_time.hour, self.down_time.minute, self.down_time.second)
                              + timedelta(seconds=1)).time()

        self.cpb.update()

    def update_pb(self):
        self.pb_value = self.pb_value + self.get_time_sec(time(0, 0, 1)) / self.get_time_sec(self.daily_target) * 100

    def get_time_sec(self, time_to_sec):
        return time_to_sec.hour * 3600 + time_to_sec.minute * 60 + time_to_sec.second

    def start_session_start(self):
        self.start_time = datetime.now()
        self.start_time_label = self.time_str(self.start_time, True, True, False, 'day_time')


class CircularProgressBar(Widget):
    thickness = 20
    value_normalized = NumericProperty(0)
    label_text = StringProperty("%")
    max = 100

    semester_start = datetime(2019, 5, 1, 0, 0, 0)
    semester_end = datetime(2019, 9, 11, 0, 0, 0)

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)
        self.label_text = str('%.3f'%(self.value_normalized * 100)) + "%"

    def set_value(self, value):
        self.value_normalized = value

        if self.value_normalized > 1:
            self.value_normalized = 1

        self.label_text = str('%.3f'%(self.value_normalized * 100)) + "%"

    def add_value(self, value):
        self.value_normalized = value + self.value_normalized

        if self.value_normalized > 1:
            self.value_normalized = 1

        self.label_text = str('%.3f'%(self.value_normalized * 100)) + "%"

    def update(self):
        semester_days = (self.semester_end - self.semester_start).days
        semester_prog = (datetime.now() - self.semester_start).days

        self.set_value(semester_prog / semester_days)
