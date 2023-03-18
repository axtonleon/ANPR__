# Use an official Python runtime as a parent image
FROM python:3.10.4 

# Set the working directory to /ANPR
WORKDIR /ANPR

# Copy the current directory contents into the container at /ANPR
COPY . /ANPR

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Expose port 8000 for the Django development server
EXPOSE 8000

# Define the command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]