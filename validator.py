import os


def validate_directory(path):
    
    # ------------------------------------------------------------------
    # Validate whether the given path is a readable absolute directory.
    # ------------------------------------------------------------------

    if not os.path.exists(path):
        return False

    if not os.path.isdir(path):
        return False

    if not os.path.isabs(path):
        return False

    if not os.access(path, os.R_OK):
        return False

    return True


def validate_interval(interval):
    
    # ------------------------------------------------------------------
    # Validate the time interval (in minutes).
    # ------------------------------------------------------------------
    
    if not interval.isdigit():
        return False

    interval = int(interval)

    if interval <= 0:
        return False

    return True


def validate_email(email):
    # ------------------------------------------------------------------
    # Perform basic email format validation.
    # ------------------------------------------------------------------

    if email.count("@") != 1:
        return False

    username, domain = email.split("@")

    if not username:
        return False

    if "." not in domain:
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    return True