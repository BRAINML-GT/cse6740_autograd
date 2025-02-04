FROM python:3.10-slim

# Copy the autograder files into the container
COPY . /autograder
WORKDIR /autograder

# Install dependencies: pytest and pytest-json-report
RUN pip install --no-cache-dir pytest pytest-json-report

# Ensure the run_autograder script is executable
RUN chmod +x run_autograder

# Command to run when the container starts
CMD ["./run_autograder"]
