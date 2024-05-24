# Use an appropriate base image with Python and Django installed
FROM python:3

# Install Django
RUN pip install django

# Set the working directory
WORKDIR /app

# Copy the app into the container
#COPY mooc-sec-project-I /app/
COPY . .

# Run server 
CMD ["python", "secprojectI/manage.py", "runserver", "0.0.0.0:8080"]


