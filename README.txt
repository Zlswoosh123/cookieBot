Plays the web game cookie clicker. This project started as a silly selenium practice script and evolved into (near) full cookieclicker playing bot fueled by raw nostalgia from playing as a child.

Setup:
1. Initial game file must be created by doing the following:
	a) Navigate to the game: https://orteil.dashnet.org/cookieclicker/
	b) Name your bakery 'Science Robot' in the top left.
	c) Click Options --> Short Numbers. This should be set to OFF.
	d) Still in Options, click 'Save to File'. You should see 'ScienceRobotBakery.txt' in your downloads folder. You can now close the window.
2. Edit clicker.py to look for the newly download file in the correct path
	a) In clicker.py, find 'self.path = r"C:\Users\Zlswo\Downloads"'
	b) Change the path to be where your game file from step 1 is saved.
3. Chromedriver must be installed and passed into the program.
	a) In main.py, set 'chrome_driver_path' to the appropriate path of your chrome web driver
	b) Download can be found here: https://chromedriver.chromium.org/downloads
4. You should now be able to run the program.

Features:
-Clicks the cookie
-Clicks Golden cookies and timed on-screen events
-Efficiently buys buildings, upgrades, and technology every 30 seconds (configurable). Recommended lower values early in the game, and larger values later for max cookies.
-Launches most recent version of your saved game.
-Autosaves every 60 mins (recommended to not have more than 100 save files in 'Downloads' folder to prevent bugs)
-Transitions to Elder phase seamlessly and clicks elder pledge for max cookies (not unlocked until later)
-Plays Garden mini-game when available
-Admin mode which allows custom wait periods, pausing, and more (press Home).

Admin Mode Explained (Press Home to activate):
-Pause: Pauses the script, press ~ to resume
-Wait: Sets how long until it purchases buildings/upgrades (default 30s). Recommended lower values early in the game, and larger values later for max cookies.
-Timeout: Skips the waiting period countdown and proceeds with buying logic (buildings/upgrades/tech). Used as manual override to enter buying logic.
-Upgrade: Skips the waiting period countdown and proceeds with buying logic for Upgrades ONLY. Used as manual override to purchase upgrades ONLY.
-Elder: Used to Pledge to Elders (not available until later). Manual override for Elder Pledge to exit Wrath mode.
-Exit: Closes the menu.

Enjoy!