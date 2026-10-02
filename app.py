import os
import re
from ipaddress import ip_address
from urllib.parse import urlsplit

import pymysql
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, send_from_directory

load_dotenv()

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.20.210"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "labeling"),
    "password": os.getenv("DB_PASSWORD", "labeling"),
    "database": os.getenv("DB_NAME", "projectsdb"),
}
DB_TABLE = os.getenv("DB_TABLE", "dashboard")

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/brand-logo.png")
def brand_logo():
    return send_from_directory(app.root_path, "kaertech_logo192.png", mimetype="image/png")

@app.get("/api/projects")
def projects():
    if not re.fullmatch(r"[A-Za-z0-9_]+", DB_CONFIG["database"]) or not re.fullmatch(
        r"[A-Za-z0-9_]+", DB_TABLE
    ):
        return jsonify({"error": "Database and table names must use letters, numbers, and underscores."}), 500

    try:
        connection = pymysql.connect(
            **DB_CONFIG,
            cursorclass=pymysql.cursors.DictCursor,
        )
        try:
            cursor = connection.cursor()
            try:
                cursor.execute(
                    f"SELECT `projects_name`, `url_link` FROM `{DB_TABLE}`"
                )
                records = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            connection.close()
    except pymysql.MySQLError:
        app.logger.exception("Could not load project links from MySQL")
        return jsonify({"error": "The project list is temporarily unavailable."}), 503

    result = []
    for record in records:
        name = str(record.get("projects_name") or "").strip()
        url = str(record.get("url_link") or "").strip()
        if "://" not in url:
            hostname = urlsplit(f"//{url}").hostname
            try:
                is_private_ip = hostname is not None and ip_address(hostname).is_private
            except ValueError:
                is_private_ip = False
            scheme = "http" if is_private_ip else "https"
            url = f"{scheme}://{url}"
        parsed_url = urlsplit(url)
        try:
            parsed_url.port
        except ValueError:
            continue
        if name and parsed_url.scheme in {"http", "https"} and parsed_url.hostname:
            result.append({"name": name, "url": url})

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)