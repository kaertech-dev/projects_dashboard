# Projects Dashboard

A small Flask dashboard using PyMySQL to read project names and destination URLs from the MySQL `projectsdb.dashboard` table. The list refreshes automatically every 15 seconds.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Set the database connection values in `.env`.
4. Start the app with `python app.py` and open `http://localhost:5000`.

The table must contain `projects_name` and `url_link` columns. URLs may include `http://` or `https://`; bare private IP addresses default to `http://`, and other bare hostnames default to `https://`. Keep `.env` private; it is excluded from Git. Use the **Projects Dashboard** launch configuration with F5 to start the app and open it in your browser.

## Run with Docker

1. Set the database connection values in `.env`.
2. Build and start the dashboard with `docker compose up --build -d`.
3. Open `http://localhost:5000` (or the host port set by `PORT` in `.env`).

Stop the container with `docker compose down`. The `.env` file is supplied to the container at runtime and is excluded from the Docker build context.