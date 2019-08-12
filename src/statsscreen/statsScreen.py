import datetime
import os
import pickle
from kivy.app import App
from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen
from statsscreen.kivyCalendar import CalendarWidget


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

    def __init__(self, timerscreen, statsscreen, session_data={}, date=(), **kwargs):
        super(RV, self).__init__(**kwargs)
        self.session_data = session_data
        self.timerS = timerscreen
        self.statsS = statsscreen
        self.date = date
        self.update()

    def update(self):
        self.day = self.session_data[(self.date[0], self.date[1], self.date[2])] \
            if (self.date[0], self.date[1], self.date[2]) in self.session_data else {'session': [], 'work_time': 0}
        self.data = self.statsS.data_to_rv_format(self.day['session'])

        work_time = self.timerS.get_sec_time(self.day['work_time'])
        self.statsS.day_label.text = 'Day Total: ' + str(work_time.hour) + 'h' + str(work_time.minute) + 'min'

    def change_day(self, date):
        self.date = date
        self.update()


class StatsScreen(Screen):
    session_data_index_key = 'session_data'
    session_data_key = 'data'

    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.ts = App.get_running_app().timerscreen

        if os.path.exists(App.get_running_app().file_dir):
            with open(App.get_running_app().file_dir, 'rb') as file:
                self.data = pickle.load(file)
        else:
            self.data = {}

        today = (datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year)
        self.day_label = Label(
            text='Day Total: ' + str(0) + 'h' + str(0) + 'min',
            size_hint=(1, 0.15)
        )
        label_font = sp(12.5)
        self.table_header = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.15)
        )
        self.header_label1 = Label(
            text='Start Time',
            font_size=label_font
        )
        self.header_label2 = Label(
            text='End Time',
            font_size=label_font
        )
        self.header_label3 = Label(
            text='Session Total',
            font_size=label_font
        )
        self.header_label4 = Label(
            text='Session Efficiency',
            font_size=label_font
        )
        self.table_header.add_widget(self.header_label1)
        self.table_header.add_widget(self.header_label2)
        self.table_header.add_widget(self.header_label3)
        self.table_header.add_widget(self.header_label4)

        self.rv = RV(session_data=self.data, date=today, timerscreen=self.ts, statsscreen=self)
        self.calendar_data = {k: v['work_time'] for k, v in self.data.items()}
        self.calendar = CalendarWidget(study_times=self.calendar_data, button_callack=self.rv.change_day)

        self.ids.stats.add_widget(self.calendar)
        self.ids.stats.add_widget(self.day_label)
        self.ids.stats.add_widget(self.table_header)

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

        with open(App.get_running_app().file_dir, 'wb') as file:
            pickle.dump(self.data, file)

    def data_to_rv_format(self, session_list):
        return list(map(lambda data:
                        {'label1': {'text': self.ts.time_str(data[0], True, True, False, 'day_time')},
                         'label2': {'text': self.ts.time_str(data[1], True, True, False, 'day_time')},
                         'label3': {'text': self.ts.time_str(data[2], True, True, True, 'timer')},
                         'label4': {'text': str('%.3f'%(self.ts.get_time_sec(data[2]) * 100 / (
                                self.ts.get_time_sec(data[1]) - self.ts.get_time_sec(data[0])))) + "%"},
                         }, session_list))
