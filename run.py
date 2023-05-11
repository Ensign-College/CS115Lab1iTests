import subprocess
import os
import signal

# Global variable to store the running process
running_process = None


def remove_main(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error deleting file: {e.filename} - {e.strerror}")


def run_job(cmd, input_data=None):
    global running_process
    current_directory = os.getcwd()

    running_process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=current_directory,
        stdin=subprocess.PIPE,
        text=True,
    )

    stdout, stderr = running_process.communicate(input_data)
    returncode = running_process.returncode

    result = subprocess.CompletedProcess(
        running_process.args, returncode, stdout, stderr
    )
    running_process = None

    return result


def stop_job():
    global running_process
    if running_process is not None and running_process.poll() is None:
        running_process.send_signal(signal.SIGTERM)
        print("Stopped the process from another function.")


if __name__ == "__main__":
    # Compile
    compile_result = run_job("javac src/Main.java")

    if compile_result.returncode != 0:
        print(
            f"Compilation error:\n{compile_result.stderr}"
        )  # Use stderr attribute to print the error message
        remove_main("src/Main.class")
    else:
        stop_job()
        print("Compilation successful.")
        remove_main("src/Main.class")
