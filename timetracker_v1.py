# testi

import win32gui
import time
import os

interval = 5

home = os.path.expanduser("~")
logdir = home+"/.timetrackerlogs"


def current_time(tformat=None):
    return time.strftime("%Y_%m_%d_%H_%M_%S") if tformat == "file"\
        else time.strftime("%Y-%m-%d %H:%M:%S")


try:
    os.mkdir(logdir)
except FileExistsError:
    pass

# path to logfile
log = logdir + "/"+current_time("file")+".txt"
started = current_time()


def time_format(s):
    # converts the time from seconds to hh:mm:ss
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def get_active_window():
    w32 = win32gui
    active_window_name = w32.GetWindowText(w32.GetForegroundWindow())
    return active_window_name


def summarize():
    with open(log, "wt", encoding="utf-8") as report:
        totaltime = sum([item[1] for item in winlist])
        report.write("")
        for w in winlist:
            w_percentage = str(round(100*w[1]/totaltime))
            report.write("" + time_format(w[1]) + " (" +
                         w_percentage + " %)" + (6-len(w_percentage))*" " + w[0] + "\n")
        report.write("\n" + "="*60+"\nstarted: " + started+"\t"+"updated: " + current_time() +
                     "\n"+"="*60)


t = 0
winlist = []
print("Monitoring started at " + started)

while True:
    time.sleep(interval)
    active_window = get_active_window()
    checklist = [item[0] for item in winlist]
    if not active_window in checklist:
        winlist.append([active_window, 1*interval])
    else:
        winlist[checklist.index(active_window)][1] = winlist[checklist.index(
            active_window)][1]+1*interval
    if t == 60/interval:
        summarize()
        t = 0
    else:
        t += 1
