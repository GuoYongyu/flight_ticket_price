from newtask import *


if __name__ == '__main__':
    while True:
        task = NewTask(departure="ζζ KMG", destination="εδΊ¬ BJS", trip_date="2022-02-20")
        task.start()
        task.join()

        time.sleep(scan_gap_seconds)
