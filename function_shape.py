## This File Defines The Two Parametters Of The Shape Of The Mask Funtion ##

# time from start to when ringtone starts (during this time the phone only vibrates)
start_time_seconds = 1

# time from the end of empty to the point in which power is 100%
time_till_full_power = 23

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.plot([0,start_time_seconds,time_till_full_power,10*60],[0,0,1,1])
    plt.show()
