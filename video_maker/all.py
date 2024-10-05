import os
import subprocess

py_files = [
    f for f in os.listdir(".") if f.endswith(".py") and not f.startswith("gif_")
]

py_files.remove("all.py")
py_files.remove("common.py")

# py_files = ["simple_demo_1.py"]  # debug purpose

for py_file in py_files:
    print(f"Running {py_file}...")
    try:
        # Run the .py file
        subprocess.run(["python", py_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {py_file}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred with {py_file}: {e}")

print("Completed running all Python files.")
