from datetime import datetime
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.carousel import Carousel

from settingsscreen.settingsScreen import SettingsScreen
from statsscreen.statsScreen import StatsScreen
from timerscreen.timerScreen import TimerScreen


class TimeTrackrApp(App):

	screen_percentage_x = NumericProperty(0.975)
	screen_percentage_y = NumericProperty(0.99)
	button_x = NumericProperty(0.9)
	button_y = NumericProperty(0.55)
	button_percentage = NumericProperty(0.7)
	main_stats_y = NumericProperty(0.4)
	stats_subdivision_y = NumericProperty(0.33)

	def __init__(self):
		App.__init__(self)
		self.settingscreen = None
		self.timerscreen = None
		self.statscreen = None
		self.pause_time = None

	def build(self):
		carousel = Carousel(direction='right')
		self.timerscreen = TimerScreen(name='main')
		self.settingscreen = SettingsScreen(name='settings')
		self.statscreen = StatsScreen(name='stats')

		carousel.add_widget(self.settingscreen)
		carousel.add_widget(self.timerscreen)
		carousel.add_widget(self.statscreen)
		# carousel.index = 1
		return carousel

	def on_pause(self):
		self.pause_time = datetime.now()
		return True

	def on_resume(self):
		resume_time = datetime.now()
		pause_time = resume_time - self.pause_time

		if self.timerscreen.time_state == 'running':
			self.timerscreen.work_time = self.timerscreen.add_time(self.timerscreen.work_time, pause_time)
		elif self.timerscreen.time_state == 'stopped':
			self.timerscreen.down_time = self.timerscreen.add_time(self.timerscreen.down_time, pause_time)


TimeTrackrApp().run()
