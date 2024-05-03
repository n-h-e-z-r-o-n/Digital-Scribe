import threading
import time

# Define a function to print active threads
def print_active_threads():
    print("Active Threads:")
    for thread in threading.enumerate():
        print("- ", thread.name)

# Define a function that will run as a thread
def my_function():
    print("Thread started:", threading.current_thread().name)
    time.sleep(5)
    print("Thread finished:", threading.current_thread().name)

# Create a new thread
thread = threading.Thread(target=my_function, name="MyThread")
thread.start()

# Print active threads before waiting for the thread to finish
print_active_threads()

# Wait for the thread to finish
thread.join()

# Print active threads after the thread has finished
print_active_threads()
