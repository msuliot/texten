import sched
import time
import subprocess
import json

scheduler = sched.scheduler(time.time, time.sleep)
interval = None


def read_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)
    

def run_task():
    print(f"Running task at: {time.ctime()}")
    subprocess.run(["python3", "texten.py"])
    schedule_next_run()


def schedule_next_run():
    global interval
    next_run_time = time.ctime(time.time() + interval)
    print(f"\nNext run at: {next_run_time}")
    
    scheduler.enter(interval, 1, run_task)


def main():
    run_task()
    
    try:
        scheduler.run()
    except KeyboardInterrupt:
        print("Scheduler stopped.")


if __name__ == "__main__":
    config_path = 'config.json'
    config = read_config(config_path)
    interval = config.get('scheduler_interval', 600)
    main()