-------------------
Files in the Folder
-------------------
testInput_x.txt: test cases
next_state_x.txt: next state for test case x
traverse_log_x.txt: traverse log for test case x
hw2GradingScript_move.py: script to check next state
hw2GradingScript_log.py: script to check traverse log

---------------------------------
Command Lines for Grading Scripts
---------------------------------
NEXT STATE:
python hw2GradingScript_state.py "standard_state_file" "student_state_file"

Example:
python hw2GradingScript_state.py next_state_1.txt next_state.txt


LOG FILE:
python hw2GradingScript_log.py "standard_log_file" "student_log_file"

Example:
python hw2GradingScript_log.py traverse_log_1.txt traverse_log.txt
