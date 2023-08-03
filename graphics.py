import matplotlib.pyplot as plt

def plot_solar_illumination(time, illum):
    plt.plot(time, illum)
    plt.xlabel('time (s)')
    plt.ylabel('illumination (lux)')
    plt.title('Indoor Illumination Curve')
    plt.show()

def plot_temperatures(time, temperatures):
    plt.plot(time, temperatures)
    plt.xlabel('time (s)')
    plt.ylabel('tempearture(C)')
    plt.title('Temperature Curve')
    plt.show()

def plot_array(index, array_to_plot):
    plt.plot(index, array_to_plot)
    plt.xlabel('index')
    plt.ylabel('values')
    plt.title('Simple Array Plot Curve')
    plt.show()
def plot_array_10(index, array_to_plot):
    plt.plot(index, array_to_plot)
    #that's what I call testing
    plt.xlabel('index')
    plt.ylabel('values')
    plt.ylim(10,-10)
    plt.title('Simple Array Plot Curve')
    plt.show()
def plot_array_minutes(index, array_to_plot):
    plt.plot(index, array_to_plot)
    plt.xlabel('minutes')
    plt.ylabel('values')
    plt.title('Simple Array Plot Curve')
    plt.show()
    
def plot_compare(time1, value1, time2, value2, y_label):
    plt.plot(time1, value1)
    plt.plot(time2, value2)
    plt.xlabel('time (s)')
    plt.ylabel(y_label)
    plt.title('Comparison')
    plt.show()

def plot_compare_scaled (time1, data1, y_label1, time2, data2, y_label2):
    fig, ax1 = plt.subplots(dpi=100)
    color = 'tab:red'
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel(y_label1, color=color)
    ax1.plot(time1, data1, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel(y_label2, color=color)  # we already handled the x-label with ax1
    ax2.plot(time2, data2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()