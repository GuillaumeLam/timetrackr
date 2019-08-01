from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import Screen


class MainScreen(Screen):
	pass


class StatsScreen(Screen):
	pass


class SettingsScreen(Screen):
	pass


class TimeTrackrApp(App):

	def build(self):
		carousel = Carousel(direction='right')
		carousel.add_widget(SettingsScreen(name='settings'))
		carousel.add_widget(MainScreen(name='main'))
		carousel.add_widget(StatsScreen(name='stats'))
		carousel.index = 1
		return carousel


TimeTrackrApp().run()
