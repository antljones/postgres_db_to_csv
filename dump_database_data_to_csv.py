import sys
import argparse
from subprocess import check_output

#Remove the table headings, separators, result count and trailing lines
def filter_headers_and_tail(pg_database_data):
    pg_database_data = pg_database_data.split("\n")
    return pg_database_data[3:-3]

def retrieve_columns(pg_database_data, column_list):
    columns = []
    #Remove unnecessary formatting and database information and get data from correct columns
    for database_data in pg_database_data:
        database_data = database_data.split("|")
        column_data = []
        for column in column_list:
            if column < len(database_data): 
                if not database_data[column].isspace() and len(database_data[column]) > 1:
                    column_data.append(database_data[column].strip())
                else:
                    column_data = []
                    continue
        if len(column_data) > 0:
            columns.append(column_data)
    return columns

def retrieve_column_data(command, column_list):
    data = check_output(command)
    data = filter_headers_and_tail(data)
    return retrieve_columns(data, column_list)

#Set the argument parser and command line arguments
parser = argparse.ArgumentParser(description="Dump a postgresql database's tables to a set of csv files")
parser.add_argument('-d', dest='database', action='store', help='the name of the database to dump')
parser.add_argument('-l', dest='database_list', action='store_true', help='list the available databases and their associated tables')
parser.add_argument('-f', dest='folder', action='store', default='/tmp/', help='Directory to store the table data csv files')

args = parser.parse_args()

#Check and act on the arguments
if args.database == None or len(args.database) == 0:
    if args.database_list:
        unusable_databases = ['template0','template1']
        #display a list of databases
        databases = retrieve_column_data(["psql","-l"],[0])
        for database in databases:
            if database[0] in unusable_databases:
                databases.remove(database)
        for database in databases:
            print(database[0])
            for table in retrieve_column_data(["psql",database[0],"-c","\d"],[1]):
                print(" - " + table[0])
        sys.exit()
    else:
        print("No valid options given (--help to list options)")
        sys.exit()
else:
    #Check the output folder path is absolute
    if not args.folder.startswith("/"):
        sys.exit("Please supply an absolute path")
    if not args.folder.endswith("/"):
        args.folder += "/"
    #retrieve a list of databases
    databases = retrieve_column_data(["psql","-l"],[0])
    for database in databases:
        if args.database == database[0]:
            #retrieve a list of tables in the chosen database
            tables = retrieve_column_data(["psql",args.database,"-c","\d"],[1,2])
            for table in tables:
                if table[1] == 'table':
                    print table[0]
                    check_output(["psql", args.database, "-c", "COPY " + table[0] + " TO '" + args.folder + table[0] + ".csv' CSV HEADER;"])
    sys.exit("Complete")
