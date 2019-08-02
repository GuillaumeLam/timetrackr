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

	def build(self):
		carousel = Carousel(direction='right')
		carousel.add_widget(SettingsScreen(name='settings'))
		carousel.add_widget(TimerScreen(name='main'))
		carousel.add_widget(StatsScreen(name='stats'))
		carousel.index = 1
		return carousel


TimeTrackrApp().run()
