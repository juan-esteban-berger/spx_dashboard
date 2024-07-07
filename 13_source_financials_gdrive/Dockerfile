# Using official Python runtime (version 3.11.2) as a parent image
FROM python:3.11.2

# Set the working directory in the docker image
WORKDIR /spx_dashboard

# Copy the requirements.txt file into our workdir in image
COPY requirements.txt ./

# Use pip to install all the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy current directory content into the working directory in image
# It will respect .dockerignore file if it exists
COPY . .

# Command to run when the container starts
CMD [ "python", "etl.py" ]
