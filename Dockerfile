FROM python:3.9-slim-buster

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Copy requirements and install
COPY requirements.txt /myportfolio/requirements.txt
WORKDIR /myportfolio
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /myportfolio

# Expose port 5000
EXPOSE 5000

# Run Flask
CMD ["flask", "run"]
