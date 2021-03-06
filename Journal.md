## MacKenzie Pennington
## Technical Journal - CSC 490
## Thursdays 3pm-4pm with Dr. Ngo

### ----------------------------------------------------------

# Friday, December 7th:
-Final planning meeting with Dr. Ngo
  -Set goals and expectation to work towards to
-GitHub repository created

# Thursday, January 24th:
-Project start

# Thursday, January 31st:
-Examined similar projects and set up Anaconda/Python 3
-Laid out GUI format for mouse/keyboard recording, goal is to have a base on 2/7

# Sunday, February 3rd:
-Started creating interface using TKinter library for Python
-Created table layout and buttons, currently the buttons have no function
-Notes: Adjusting from Java to Python is definitely a challenge for me, but I am enjoying it. Luckily, the TKinter library is very similar to the ReactJS Material-UI library I used at my internship over the summer.

# Tuesday, February 5th:
-Began practicing with the button functionality, followed some online tutorials for simple changes such as configuring the labels
-Worked mainly on actual button functionality afterwards

# Wednesday, February 6th:
-Created Treeview table with tkinter in GUI window
-Issues:
  -Button widgets cannot be embedded within Treeview widgets.
-To-Do:
  -Make tree insertion work together with record
  -Add functionality to clear, record, and save buttons
-Ideas for later in project:
  -Add file menu widget to be able to load previous recordings
  -Treeview allows for items to be selected - maybe be able to tab through mouse recordings?
  
# Thursday, February 7th:
-Pre-meeting: Tried to find workaround for using buttons and treeview at the same time
-Ideas: Could go back to using grid instead of treeview, but might not be as efficient?

# Monday, February 11th:
-Now using PyQt5 for interface
-Created tables and buttons Clear, Record, and Stop
-Need to adjust window size
-Testing populating table with data, not working yet

# Thursday, February 14th:
-Table populating with strings, but not with list items
-After meeting, assigned task to begin mouse recording step

# Thursday, February 21st:
-Meeting cancelled this week

# Friday, February 22nd:
-Experimenting with pyautogui, functionality to control mouse and keyboard but not record?
-Researching other mouse recording methods, found Pynput (https://pypi.org/project/pynput/)

# Tuesday, February 26th:
-Created new branch mouse-recording
-Added mouse listener/monitor
-Recording occurs without error but doesn't populate the data table, just the console
-Recording happens on file execution, not on button press
-Added stop button, but the buttons don't seem to control the recording
-When running file, the recording begins, and the window pops up only after clicking once. Clicking the buttons does not do much

# Thursday, February 28th:
-Discussed collecting data THEN displaying results
-Added hotkeys to start all button functinality
-Discussed adjusting and scaling for different screen resolutions
-Planned to add keyboard recording

# Tuesday, March 5th:
-Began working out recording errors
  -Actions not starting with button click/hotkey press
  -Results print in console instead of in gui
-Incorporated pandas dataframe to collect data

# Thursday, March 7th:
-Fixed mouse recording actions (move, click, scroll)
-Properly displays data in Dataframe
-Still working out how to print data into gui instead of console
-Created new branch keyboard-recording
  -Added keyboard listener, current errors:
    -When recording, using the keyboard then stopping recording crashes the program

# Thursday, March 21st:
-Pre-meeting issues:
    -Able to control mouse
    -Unsure how to control with pre-recorded coordinates
    -Scrolling works but not when navigating to new page?
    -Still need to incorporate keyboard input
-To-Do:
    -Collect data from dataframe by column
    -Scan for event other than move, only move to that coordinate instead of pixel-by-pixel
    -Keyboard input!!
    -Download awards, save files as "nsf..."
-Merged in mouse-recording branch

# Wednesday, March 27th:
-Worked mainly on play button functionality
-Play button successfully replays the recorded movements, but stuck on an endless loop where I cannot control the mouse. Only logging out and logging in stops the program now. Spending time debugging...
-Couldn't get movement to only move to action-based coordinates, so it moves fluidly/pixel-by-pixel
-On break, spent time figuring out keyboard listener. Seems like both cannot run at once, so there has to be keys to start and stop the listeners? There has to be a workaround, though.

# Thursday, March 28th:
-Fixed endless loop
    -No need for nested for-loop (was running the recorded actions for the amount of recorded actions there were, i.e. if 46 actions were recorded, it played through all 46 actions 46 times)
-Worked on keyboard listener, still unable to find good fix
-Tried to make buttons change color when recording/stopped so the user knows without looking at the console. Was able to get buttons to change colors on immediate click but not remain changed.
-Successfully tested play button by recording on NSF website and downloading awards - unable to change names in download yet since there is no keyboard control

# Friday, March 29th:
-Keyboard and mouse listeners and controllers work together now - had to start, stop, and control separately
-Finding some issues where the keyboard types different characters than what's recorded? Looking into it now...

# Tuesday, April 2nd:
-Still having problems with keyboard/recording compatibility, can't seem to find anyone else experiencing this bug with Pynput
-Cleaned up some of the code, added comments
-Played around with window layout

# Thursday, April 4th:
-Discovered during meeting with Dr. Ngo that the keyboard recording issue was due to type inconsistency
  -Type-casting the key variables to char's fixed the problem
-Discussed beginning to test program on more advanced tasks - i.e. downloading multiple files, changing file names, and repeating
-Challenge finding website where you can download all files on page/select amount of files, changing pages at top of screen to avoid scrolling issues (we don't know exactly how far to scroll)

# Friday, April 5th:
-Change some of the ways I access the dataframe after learning more about it at the Python Bootcamp
-Made row/column access more efficient

# Wednesday, April 10th:
-Current issues/questions:
  -How to add wait-times for windows to load?
  -How to interact with file saving dialog?
  -How to detect special keys, i.e. arrow keys and enter key?
-Tried working with Selenium on the wait times, not much success with that

# Thursday, April 11th:
-Added in time sleeps after releasing a mouse-click, fixed wait-time issue but made playback painfully slow
-Discussed in-meeting attempting to advance the program a little bit:
  -User inserting wait times after recording - would have to add function to insert rows
  -Giving user option to repeat x amount of rows x amount of times
-Merged in mouse-controlling branch
-Created advanced branch
  
# Sunday, April 14th:
-Added insert button, clear-all button, and clear-one button
-Added in status label - trying to change it with button actions (ie. "Recording..." or "Replaying...")
  -No success on this - struggling to change out-of-class variables in Python?
  -Tried changing it to setting the window title with each button click, also didn't work. Went back to the inital label
  
# Thursday, April 18th:
-Playing around with insert function
  -Successfully asks the user what they want to input in each column of the row, stores the answers in a variable
  -Following a pandas dataframe tutorial on inserting row at a selected position
    -Instructed using a separate insert function - thinks I'm passing in 4 arguments when I'm passing in 3?
-Changed row-selection properties - selects an entire row, only one at a time. Plan on using this to find the index of the selected row and insert one row below the selected one
-Work in progress: Wait-time functionality in playback
  -if device = "Wait", extract integer from the string in the event "Wait ___ seconds" and wait that long
-Made working "Clear One" button
-Plan on adding repeat functionality once this is working

# Thursday, April 25th:
-Roadblocks of today:
  -Inserting a row at given index instead of appending on the end of the table/beginning of table/replacing row
  -Reads in device as "nan" after sorting?
  -Occasionally program crashes during recording, have to restart kernel everytime
-Been working on getting the insert function to work

-***look at Model View Control (MVC Framework) 
