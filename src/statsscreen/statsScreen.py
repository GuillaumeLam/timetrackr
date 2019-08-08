from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from statsscreen.kivyCalendar import CalendarWidget

import datetime


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.display_data = [{'text': str(x)} for x in range(10)]


class StatsScreen(Screen):

    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.ts = App.get_running_app().timerscreen
        self.data = {}                                      # TODO load from storage
        self.calendar_data = {k: v['work_time'] for k, v in self.data.items()}
        self.calendar = CalendarWidget(study_times=self.calendar_data)
        self.ids.stats.add_widget(self.calendar)
        self.day_label = Label(
            text='Day Total: Xh',
            size_hint=(1, 0.15)
        )
        self.ids.stats.add_widget(self.day_label)
        self.rv = RV()
        self.ids.stats.add_widget(self.rv)

    def add_data(self, work_time, start_time, end_time):
        if (start_time.day, start_time.month, start_time.year) in self.data:
            self.data[(start_time.day, start_time.month, start_time.year)]['session'] \
                .append((start_time.time(), end_time.time(), work_time))
            self.data[(start_time.day, start_time.month, start_time.year)]['work_time'] = \
                self.data[(start_time.day, start_time.month, start_time.year)]['work_time'] +\
                self.ts.get_time_sec(work_time)
        else:
            self.data[(start_time.day, start_time.month, start_time.year)] = {}
            self.data[(start_time.day, start_time.month, start_time.year)]['session'] = []
            self.data[(start_time.day, start_time.month, start_time.year)]['session']\
                .append((start_time.time(), end_time.time(), work_time))
            self.data[(start_time.day, start_time.month, start_time.year)]['work_time'] = \
                self.ts.get_time_sec(work_time)
        print(self.data[(start_time.day, start_time.month, start_time.year)])
