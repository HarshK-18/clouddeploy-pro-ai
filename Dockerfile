
# Use a small official Python image.
FROM python:3.14-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy only the application file.
COPY src/app.py ./app.py

# Use a non-root user for better security.
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

# Set the default application environment.
ENV APP_ENV=development

# Run the local demonstration entry point.
CMD ["python", "app.py"]
