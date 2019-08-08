from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from statsscreen.kivyCalendar import CalendarWidget

import datetime


class MultiLabel(RecycleDataViewBehavior, GridLayout):
    index = None
    cols = 4

    def refresh_view_attrs(self, rv, index, data):
        self.label1_text = data['label1']['text']
        self.label2_text = data['label2']['text']
        self.label3_text = data['label3']['text']
        self.label4_text = data['label4']['text']
        return super(MultiLabel, self).refresh_view_attrs(
            rv, index, data
        )


class RV(RecycleView):
    day = {'session': [], 'work_time': 0}

    def __init__(self, timerScreen, statsScreen, session_data={}, date=(), **kwargs):
        super(RV, self).__init__(**kwargs)
        self.session_data = session_data
        self.timerS = timerScreen
        self.statsS = statsScreen
        self.date = date
        self.update()

    def update(self):
        self.day = self.session_data[(self.date[0], self.date[1], self.date[2])] \
            if (self.date[0], self.date[1], self.date[2]) in \
               self.session_data else {'session': [], 'work_time': 0}
        self.data = self.statsS.data_to_rv_format(self.day['session'])

        work_time = self.timerS.get_sec_time(self.day['work_time'])
        print(work_time)
        self.statsS.day_label.text = 'Day Total: ' + str(work_time.hour) + 'h' + str(work_time.minute) + 'min'

    def change_day(self, date):
        self.date = date
        self.update()


class StatsScreen(Screen):

    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.ts = App.get_running_app().timerscreen
        self.data = {(7,8,2019):{'session': [(datetime.time(20, 25, 38), datetime.time(22, 25, 39), datetime.time(2, 0, 1))], 'work_time': 7201}}      # TODO load from storage
        self.calendar_data = {k: v['work_time'] for k, v in self.data.items()}
        self.calendar = CalendarWidget(study_times=self.calendar_data)
        self.ids.stats.add_widget(self.calendar)

        self.day_label = Label(
            text='Day Total: ' + str(0) + 'h' + str(0) + 'min',
            size_hint=(1, 0.15)
        )
        self.rb_header_label = Label(
            text='Insert table headers',
            size_hint=(1, 0.15)
        )
        self.ids.stats.add_widget(self.day_label)
        self.ids.stats.add_widget(self.rb_header_label)

        self.rv = RV(session_data=self.data, date=self.calendar.active_date, timerScreen=self.ts, statsScreen=self)
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

        self.rv.update()

        # day = self.data[(start_time.day, start_time.month, start_time.year)]
        #
        # self.rv.data = self.data_to_rv_format(day['session'])
        # work_time = self.ts.get_sec_time(day['work_time'])
        #
        # #
        # self.day_label.text = 'Day Total: ' + str(work_time.hour) + 'h' + str(work_time.minute) + 'min'
        # #

    def data_to_rv_format(self, session_list):
        return list(map(lambda data:
                        {'label1': {'text': self.ts.time_str(data[0], True, True, False, 'day_time')},
                        'label2': {'text': self.ts.time_str(data[1], True, True, False, 'day_time')},
                        'label3': {'text': self.ts.time_str(data[2], True, True, True, 'timer')},
                        'label4': {'text': str(self.ts.get_time_sec(data[2]) * 100 / (
                                self.ts.get_time_sec(data[1]) - self.ts.get_time_sec(data[0]))) + "%"},
                         }, session_list))

    # def update_session_data(self):
