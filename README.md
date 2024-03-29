# Incident Management System for Flowmon Collector
This is proof-of-concept for incident management system created for Flowmon Collector and with help of Flowmon Networks (today part of Progress Software Corp.)

## How to run app for development
0) You have installed all dependencies via PIP & did PostgreSQL setup
1) Go to code directory
2) Run: source venv/bin/activate (if you did pip install under environment)
3) Run: uvicorn src.endpoints.ims_api:app --reload
4) Check documentation on http://127.0.0.1:8000/docs

## How to do a PostgreSQL setup for development
1) Run: sudo gedit /var/lib/pgsql/data/pg_hba.conf (to locate the file run: locate pg_hba.conf)
2) Change ident method to trust for IPv4 & IPv6(do not use this on production!)
3) Run: sudo service postgresql restart
4) Create database "ims_db"
5) Fill database schema with: psql -s ims_db < /path/to/the/repo/ims/postgresql_dump_file

## How to run tests
1) Go to code directory
2) Run: source venv/bin/activate
3) Run: python -m pytest src/test/ -v

### Code coverage 
To run test with code coverage execute: coverage run -m pytest src/test/ -v \
To generate report run: coverage html

## How to make a hash
1) Go to code directory
2) Run: source venv/bin/activate
3) Run: python
4) Enter: from passlib.hash import argon2
5) Enter: argon2.using(rounds=4).using(memory_cost=2097152).using(time_cost=1).hash("password")





