# Use the official PostgreSQL Docker image
FROM postgres:13

# Set environment variables
ENV POSTGRES_USER myuser
ENV POSTGRES_PASSWORD mypassword
ENV POSTGRES_DB mydatabase

# Copy the SQL script to initialize the database
COPY init.sql /docker-entrypoint-initdb.d/
