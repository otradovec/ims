# Incident Management System for Flowmon Collector
This is proof-of-concept for incident management system created for Flowmon Collector and with help of Flowmon Networks (today part of Progress Software Corp.)

## How to run app for development
1) Go to code directory
2) Run: source venv/bin/activate
3) Run: uvicorn src.ims_api:app --reload

## How to run tests
1) Go to code directory
2) Run: source venv/bin/activate
3) Run: python -m pytest src/test/end_to_end/*


