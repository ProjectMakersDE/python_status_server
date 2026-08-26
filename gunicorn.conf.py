import os


def positive_int(name, default):
    value = int(os.getenv(name, default))
    if value < 1:
        raise ValueError(f"{name} must be at least 1")
    return value


bind = f"0.0.0.0:{positive_int('STATUS_SERVER_PORT', 5000)}"
workers = positive_int("GUNICORN_WORKERS", 2)
threads = positive_int("GUNICORN_THREADS", 4)
timeout = positive_int("GUNICORN_TIMEOUT", 30)
accesslog = "-"
errorlog = "-"
capture_output = True
