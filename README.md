To use this script you will currently need to run it with a role that has super user privileges in postgres as well as having login privileges. You can also use the postgres user:

#Change the script owner
sudo chown postgres:postgres dump_database_data_to_csv.py

#Change to the postgres user
sudo su postgres

#Run the script to produce .csv files for a database's tables and it's data.
python dump_database_data_to_csv.py -d <yourdatabasename> 

#List all databases and their tables
python dump_database_data_to_csv.py -l

#Show help
python dump_database_data_to_csv.py --help

Currently the output files are placed in /tmp by default with the table names as the file name and .csv extension. If you want to specify a different directory using the -f option please note that the COPY command used requires an absolute path.
