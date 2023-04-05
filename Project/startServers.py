import subprocess
import platform

# Determine the command to use to open a new terminal window
system = platform.system()
if system == "Windows":
    new_window_command = "start"
elif system == "Darwin":
    new_window_command = "open"
else:
    new_window_command = "gnome-terminal"

# Start Django server in a new terminal window
django_dir = "cancer_diagnosis"
django_cmd = "python manage.py runserver"
django_proc = subprocess.Popen([new_window_command, "-a", "Terminal", "-e", f"bash -c 'cd {django_dir} && {django_cmd}; exec bash'"])

# Start FastAPI server in a new terminal window
fastapi_dir = "image_processing"
fastapi_cmd = "uvicorn app:app --reload --host 127.0.0.1 --port 8001"
fastapi_proc = subprocess.Popen([new_window_command, "-a", "Terminal", "-e", f"bash -c 'cd {fastapi_dir} && {fastapi_cmd}; exec bash'"])

# Wait for both processes to finish
django_proc.wait()
fastapi_proc.wait()
