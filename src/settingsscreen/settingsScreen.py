from datetime import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class SettingsScreen(Screen):
    h_spin_values = list(map(lambda val: str(val) if val > 9 else '0' + str(val), range(24)))
    m_spin_values = list(map(lambda val: str(val) if val > 9 else '0' + str(val), range(60)))

    h_spin_default = '00'
    m_spin_default = '00'

    h_spin_last_pick = None
    m_spin_last_pick = None

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.ts = self.app.timerscreen
        self.set_default_spinner(self.ts.daily_target)

    def on_spinner_select(self):
        h_spin_text = self.ids.h_spin.text
        m_spin_text = self.ids.m_spin.text

        if h_spin_text == '00' and m_spin_text == '00':
            popup = Popup(
                title='Get better goals',
                content=Label(text="That's a pretty low goal!"),
                auto_dismiss=True,
                size_hint=(None, None),
                size=(200, 100)
            )
            popup.open()
            self.ids.h_spin.text = self.h_spin_last_pick
            self.ids.m_spin.text = self.m_spin_last_pick
        else:
            if int(h_spin_text) >= 20:
                text = 'Studying is important, but did you know that the bare minimum of sleep needed to live, ' \
                       'not just thrive, is 4 hours per day'
                popup = Popup(
                    title='Get some rest',
                    content=Label(text=text),
                    auto_dismiss=True,
                    size_hint=(None, None),
                    size=(200, 100)
                )
                popup.open()
            self.ts.daily_target = time(int(h_spin_text), int(m_spin_text))
            self.ts.store_daily_target(int(h_spin_text), int(m_spin_text))
            self.ts.daily_target_label = self.ts.time_str(self.ts.daily_target, True, True, False, 'timer')

            self.h_spin_last_pick = h_spin_text
            self.m_spin_last_pick = m_spin_text

    def set_default_spinner(self, default_time):
        hour = default_time.hour
        if hour < 10:
            self.ids.h_spin.text = '0' + str(hour)
        else:
            self.ids.h_spin.text = str(hour)

        minute = default_time.minute
        if minute < 10:
            self.ids.m_spin.text = '0' + str(minute)
        else:
            self.ids.m_spin.text = str(minute)
