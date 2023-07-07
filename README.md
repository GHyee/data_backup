# Data Loss Simulation

## Overview
This repository contains the files required to simulate a data loss scenario.
The main python script `simulate_data_loss.py` will:
1.	Connect to the customer database using appropriate credentials.
2.	Identify a specific set of records from a chosen table that will be subjected to data loss simulation.
3.	Safely back up the identified records to a separate backup location or table.
4.	Simulate data loss by deleting the identified records from the original table.
5.	Execute the recovery process to restore the deleted records from the backup.

## Mock database and data generation
To simulate the data loss, we can use Docker to:
1. Create a PostgreSQL database
2. Create a table `customers` with 2 fields - `customer_id` (Primary Key) and `customer_name`.
3. Insert 100 mock data records.

Execute the following codes to build the Docker file and inject mock data.
```bash
docker build -t my-postgres .
```

Run the below code to run the container.
```bash
docker run -d -p 5432:5432 my-postgres
```

Verify that the tables are created correctly.
```bash
docker exec -it <container_id> psql -U myuser mydatabase
```

Once connected, you can execute SQL queries to interact with the database and fetch all records from the customers table.
```sql
SELECT * FROM customers;
```

Sample output:
```
mydatabase=# select * from customers
;
 customer_id | customer_name  
-------------+----------------
         101 | Customer 1-1
         102 | Customer 1-2
         103 | Customer 1-3
         104 | Customer 1-4
         105 | Customer 1-5
         106 | Customer 1-6
```

## Performing the simulation
Install the required dependency.
```bash
pip install -r requirements.txt
```

Execute the below code to simulate the data loss and recovery process.
```bash
python -m simulate_data_loss                                                      ─╯
```

Sample output:
```bash
python -m simulate_data_loss
Backup table name already exists. It will be renamed to customers_backup_v1.
These records [(104,), (118,), (115,), (125,), (108,), (181,), (117,), (126,), (156,), (196,)] are backed up successfully to customers_backup_v1.
Records [(104,), (118,), (115,), (125,), (108,), (181,), (117,), (126,), (156,), (196,)] removed successfully.
Records [(104,), (118,), (115,), (125,), (108,), (181,), (117,), (126,), (156,), (196,)] restored successfully.
```