import argparse
import pandas as pd
from . import Session

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user', help='user for database login')
    parser.add_argument('password', default=None, help='password for login if necessary')
    parser.add_argument('host', help='host IP for database')
    parser.add_argument('database', help='database to run queries on')
    parser.add_argument('table', help='table to insert into (will create new if doesn\'t exist)')
    parser.add_argument('filename', help='filepath of CSV file to insert')
    args = parser.parse_args()

    # create session for login
    sess = Session.Session(args.user, args.password, args.host, db=args.database)

    # use insert_from_CSV() method to insert csv into table
    sess.insert_from_CSV(args.filename, args.table)