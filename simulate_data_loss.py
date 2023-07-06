import psycopg2
from psycopg2 import sql
from typing import List, Tuple
import random


def connect_to_database(host: str, port: int, database: str, user: str, password: str) -> psycopg2.extensions.connection:
    """
    Connect to the PostgreSQL database.

    Args:
        host (str): Hostname or IP address of the database server.
        port (int): Port number to connect to the database server.
        database (str): Name of the database.
        user (str): Username for authentication.
        password (str): Password for authentication.

    Returns:
        psycopg2.extensions.connection: The database connection object.
    """
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)


def get_primary_key_values(connection: psycopg2.extensions.connection, table_name: str, primary_key_field: str) -> List[Tuple]:
    """
    Retrieve the primary key values from the specified table.

    Args:
        connection (psycopg2.extensions.connection): The database connection object.
        table_name (str): Name of the table.
        primary_key_field (str): Name of the primary key field.

    Returns:
        List[Tuple]: The primary key values.
    """
    try:
        cursor = connection.cursor()

        # Retrieve the primary key values from the table
        cursor.execute(sql.SQL("SELECT {} FROM {}").format(
            sql.Identifier(primary_key_field),
            sql.Identifier(table_name)
        ))
        primary_key_values = cursor.fetchall()

        cursor.close()
        return primary_key_values
    except psycopg2.Error as e:
        print("Error retrieving primary key values:", e)


def backup_records(connection: psycopg2.extensions.connection, table_name: str, backup_table_name: str, primary_key_field: str, primary_key_values: List[Tuple]) -> None:
    """
    Safely backs up the identified records to a separate backup table.

    Args:
        connection (psycopg2.extensions.connection): The database connection object.
        table_name (str): Name of the table containing the records.
        primary_key_values (List[Tuple]): List of primary key values identifying the records to back up.
    """
    try:
        cursor = connection.cursor()

        # Create a backup table with the same structure as the original table
        cursor.execute(sql.SQL("CREATE TABLE IF NOT EXISTS {} (LIKE {} INCLUDING ALL)").format(
            sql.Identifier(backup_table_name),
            sql.Identifier(table_name)
        ))
        import pdb; pdb.set_trace()
        # Copy the identified records into the backup table
        for primary_key_value in primary_key_values:
            cursor.execute(sql.SQL("INSERT INTO {} SELECT * FROM {} WHERE {} = %s").format(
                sql.Identifier(backup_table_name),
                sql.Identifier(table_name),
                sql.Identifier(primary_key_field)
            ), primary_key_value)

        connection.commit()
        cursor.close()
        print(f"These records {primary_key_values} are backed up successfully to {backup_table_name}.")
    except psycopg2.Error as e:
        connection.rollback()
        print("Error backing up records:", e)


def remove_records(connection: psycopg2.extensions.connection, table_name: str,  primary_key_field: str, primary_key_values: List[Tuple]) -> None:
    """
    Remove records from the original table.

    Args:
        connection (psycopg2.extensions.connection): The database connection object.
        table_name (str): Name of the table containing the records.
        primary_key_field (str): Name of the primary key field.
        primary_key_values (List[Tuple]): List of primary key values.

    """
    try:
        cursor = connection.cursor()

        # Delete the sampled records from the original table
        for primary_key_value in primary_key_values:
            cursor.execute(sql.SQL("DELETE FROM {} WHERE {} = %s").format(
                sql.Identifier(table_name),
                sql.Identifier(primary_key_field)
            ), primary_key_value)

        connection.commit()
        cursor.close()
        print(f"Records {primary_key_values} removed successfully.")
    except psycopg2.Error as e:
        connection.rollback()
        print("Error backing up and removing records:", e)


def restore_records(connection: psycopg2.extensions.connection, table_name: str, backup_table_name: str, primary_key_field: str, primary_key_values: List[Tuple]) -> None:
    """
    Restores the identified records from the backup table to the original table.

    Args:
        connection (psycopg2.extensions.connection): The database connection object.
        table_name (str): Name of the table to restore the records to.
        backup_table_name (str): Name of the backup table.
        primary_key_values (List[Tuple]): List of primary key values identifying the records to restore.
    """
    try:
        cursor = connection.cursor()

        # Restore the identified records from the backup table
        for primary_key_value in primary_key_values:
            cursor.execute(sql.SQL("INSERT INTO {} SELECT * FROM {} WHERE {} = %s").format(
                sql.Identifier(table_name),
                sql.Identifier(backup_table_name),
                sql.Identifier(primary_key_field)
            ), primary_key_value)

        connection.commit()
        cursor.close()
        print(f"Records {primary_key_values} restored successfully.")
    except psycopg2.Error as e:
        connection.rollback()
        print("Error restoring records:", e)


# Example usage
if __name__ == "__main__":
    # Connect to the database
    connection = connect_to_database("localhost", 5432, "mydatabase", "myuser", "mypassword")

    # Specify the table name, primary key field, and the number of records to sample
    table_name = "customers"
    backup_table_name = "customers_backup"
    primary_key_field = "customer_id"
    sample_size = 10

    # Retrieve the primary key values from the table
    primary_key_values = get_primary_key_values(connection, table_name, primary_key_field)

    # Randomly sample records for simulation
    sampled_primary_keys = random.sample(primary_key_values, sample_size)

    # Backup and remove the randomly sampled records
    backup_records(connection, table_name, backup_table_name, primary_key_field, sampled_primary_keys)
    import pdb; pdb.set_trace()
    remove_records(connection, table_name, primary_key_field, sampled_primary_keys)
    pdb.set_trace()
    restore_records(connection, table_name, backup_table_name, primary_key_field, sampled_primary_keys)
    pdb.set_trace()
    # Close the database connection
    connection.close()
