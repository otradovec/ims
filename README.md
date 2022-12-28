# Incident Management System for Flowmon Collector
This is proof-of-concept for incident management system created for Flowmon Collector and with help of Flowmon Networks (today part of Progress Software Corp.)

## How to run app for development
0) You have installed all dependencies via PIP & did PostgreSQL setup
1) Go to code directory
2) Run: source venv/bin/activate
3) Run: uvicorn src.endpoints.ims_api:app --reload

## How to do a PostgreSQL setup for development
1) Run: sudo gedit /var/lib/pgsql/data/pg_hba.conf
2) Change ident to trust (do not use this on production!)
3) Run: sudo service postgresql restart

## How to run tests
1) Go to code directory
2) Run: source venv/bin/activate
3) Run: python -m pytest src/test/ -v




