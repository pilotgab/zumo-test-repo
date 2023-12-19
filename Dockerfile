FROM python:3.9-slim

# Setting the working directory in the container to /app
WORKDIR /app

# Copying the current directory contents into the container at /app
COPY . /app

# Installing all needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Making port 8080 available to the world outside this container
EXPOSE 8080

# Defining environment variable
ENV NAME World

# Runing app.py when the container launches
CMD ["python", "app.py"]

