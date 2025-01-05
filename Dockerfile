# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install -y gcc libpq-dev libjpeg-dev zlib1g-dev

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

#RUN echo "from django.contrib.auth.models import User; \
#          User.objects.create_superuser('yash', 'yash@gmail.com', 'yash')" | python manage.py shell


# Expose the port the app runs on
EXPOSE 8000

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]