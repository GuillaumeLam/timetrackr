# timetrackr
An app to track working time


---


Ever wondered how much time are you actually studying? Or maybe you're looking to optimize the time you are studying to 
be even more efficient? Well look no further! 

<div>
	<div class='inline-block'>
		<img src="https://github.com/GuillaumeLam/timetrackr/blob/master/assets/app-screenshots/timetracker-settings.png" height="33.3%" width="32%">
	</div>
	<div class='inline-block'>
		<img src="https://github.com/GuillaumeLam/timetrackr/blob/master/assets/app-screenshots/timetracker-main.png" height="33.3%" width="32%">
	</div>
	<div class='inline-block'>
		<img src="https://github.com/GuillaumeLam/timetrackr/blob/master/assets/app-screenshots/timetracker-stats.png" height="33.3%" width="32%">
	</div>
</div>

With this mobile/desktop app, you can solve those problems. Simply press **Start** when you start working and press 
**Stop** when taking a small break or you're done working. With a session based system, you track how long you worked in
the day and in how many periods rather than one simple cumulative value. Furthermore, you can take breaks of a certain 
length within the same session. 

Set a daily goal to achieve and the progress bar will show you how far away you are to obtaining that goal.

Finally on the main page, set a start and end to the semester to keep track of how far along in the semster you are!


On the settings side, you can delete the session data or set the daily goal.


Finally, on the statistics side, you will be able to see the session data of any day. The more you work, the more that 
day's color will change to help you see the days with more progress. Including the start, end and duration of the work 
session, you can check how efficient you were during that session.


## Technologies

This app runs using Kivy. As such, most of the codebase is python. To get some extra modules, kivy-garden was also of 
help. The virtualenv is created using pipenv. Finally, to generate the apk, buildozer is utilized.

To start the virtualenv, run the command:
```
pipenv install
```
Followed by this command to initialize the shell:
```
pipenv shell
```

To run the app, simply run this command from the root folder of the project:
```
python scr/main.py
```

Finally, to create the apk and create a gzip to pass around:
```
make all
```

The apk and the .gzip should be in the bin folder!


## Deployment

As the app is still quite unpolished, I would like to get to a certain level of finish before deploying this onto the 
app store. Perhaps, an alpha could be released in the next upcoming months and later a better version.


#### Want to contribute?

If you want to help to make the app better for you or to help others, this is github! Fork and code away!

Here is a list of features to add:
- fix issue where session data doesnt show up after data clear
- add selection for semester start & end
- add method of exporting data
- give the settings page some love
