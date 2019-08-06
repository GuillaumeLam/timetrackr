from datetime import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen


class SettingsScreen(Screen):
    h_spin_values = list(map(lambda val: str(val) if val > 9 else '0' + str(val), range(24)))
    m_spin_values = list(map(lambda val: str(val) if val > 9 else '0' + str(val), range(60)))

    h_spin_default = '00'
    m_spin_default = '00'

    h_spin_last_pick = None
    m_spin_last_pick = None

    ts = None

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.ts = App.get_running_app().timerscreen
        print(self.ts.daily_target)
        self.set_default_spinner(self.ts.daily_target)

    def on_spinner_select(self):
        h_spin_text = self.ids.h_spin.text
        m_spin_text = self.ids.m_spin.text

        if h_spin_text == '00' and m_spin_text == '00':
            popup = ModalView(
                auto_dismiss=True,
                size_hint=(None, None),
                size=(200, 100)
            )
            popup.add_widget(Label(text="That's a pretty low goal!"))
            popup.open()
            self.ids.h_spin.text = self.h_spin_last_pick
            self.ids.m_spin.text = self.m_spin_last_pick
        else:
            self.ts.daily_target = time(int(h_spin_text), int(m_spin_text))
            self.ts.daily_target_label = self.ts.time_str(self.ts.daily_target, True, True, False, 'timer')

            self.h_spin_last_pick = h_spin_text
            self.m_spin_last_pick = m_spin_text

    def set_default_spinner(self, default_time):
        hour = default_time.hour
        print(hour)
        if hour < 10:
            self.ids.h_spin.text = '0' + str(hour)
            print(self.h_spin_default)
        else:
            self.ids.h_spin.text = str(hour)

        minute = default_time.minute
        if minute < 10:
            self.ids.m_spin.text = '0' + str(minute)
        else:
            self.ids.m_spin.text = str(minute)
