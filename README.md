# Incident Management System for Flowmon Collector
This is proof-of-concept for incident management system created for Flowmon Collector and with help of Flowmon Networks (today part of Progress Software Corp.)

## incident_status
0 Reported\
1 Confirmed\
2 In progress\
3 For review\ 
4 Solved\
5 Cancelled

## incident_priority
-2 low\
0 middle\
2 high

## How to run tests
python -m pytest src/test/end_to_end.py
