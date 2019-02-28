# 8103RoboticsDataAnalysis
The csv produced by the program orders teams twice. Each team has a GlMedian and a SlMedian, and each respective table is ordered based on these values. Only the top 15 teams on each side are shown. Null Robotics’ program doesn’t take into account teams with no Median on a given side, shunting them automatically to the bottom of the pile, most likely not to be displayed.
•Team #
	o   The team number of a team. Click on it to pull up their team’s picture
•Name
	o   A team’s name
•DQ
	o   The number of disqualifiers a team has
	o   Disqualifiers include:
		1. Not having a full auto (average auto is less than 60 points)
 		2. More than 1 disconnection
		3. Missing more than 1 hang
		4. The pit scouting sheet lists them as “breakable”
•Breakable:	
	o   Whether or not a pit-scouter considers a team “Breakable”
	o   Acts as a disqualifier
•FullCrater:
	o   Whether or not the pit-scouting sheet says they have a full auto starting from the crater
•FullDepot:
	o   Whether or not the pit-scouting sheet says they have full auto from the depot
•Gl/Sl:
	o   Gl means gold
	o   Sl means silver
	o   Median:
		The median of their scores on a side
		Defaults to NA if there is not a score on that side
	o   Avg.:
		Average on a side
		Defaults to NA if there is not a score on that side
	o   Auto Avg.:
		The average autonomous score of a robot on a side.
	o   StdDev.:
		The standard deviation on a side
		Defaults to NA if there aren’t at least two scores on that side
	o   Med(-+)Std:
		Median plus/minus standard deviation on a side
		Defaults to NA if StdDev or Median are NA
•Disconnects:
	o   The number of disconnections a robot has in a match
•Preferred Side:
	o   The side a team “prefers” based on the pit scouting sheet
