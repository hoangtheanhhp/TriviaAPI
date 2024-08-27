# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port gunicorn will run on
EXPOSE 5000

# Run gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
CMD ["python", "app.py"]