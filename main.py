from newtask import *


if __name__ == '__main__':
    while True:
        task = NewTask(departure="昆明 KMG", destination="北京 BJS", trip_date="2022-02-20")
        task.start()
        task.join()

        time.sleep(scan_gap_seconds)
