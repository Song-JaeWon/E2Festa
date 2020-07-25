import extract
import numpy as np
from realtime_classification import *

import matplotlib.pyplot as plt
import matplotlib._color_data as mcd
from drawnow import *
import timeit
import gc


# color_map = list({name for name in mcd.CSS4_COLORS if "xkcd:" + name in mcd.XKCD_COLORS})
exitThread = False

low = -10000
high = 10000

clf_list = []


class Receiver:
    def __init__(self, *args, wide=31, show=4, type="realtime_classifier"):
        self.port_num = ""
        self.baud_rate = 9600
        self.line = []
        self.cnt = 0
        self.pre = 0
        self.now = 0
        self.elapsed_time = []
        self.signal = None
        self.num_receive = 0
        self.num_sensors = 0
        self.dataArr = []
        self.Arr = None
        self.sensor_dict = dict(zip(args, np.zeros(len(args))))
        self.sensor_data = []
        self.wide = wide
        self.show = show
        self.low = -10000
        self.high = 10000
        self.start_time = timeit.default_timer()
        self.type = type

    def set_port_num(self, port_num):
        self.port_num = port_num

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate

    def set_using_sensor(self, *args):
        for sensor in [arg for arg in args if arg in self.sensor_dict.keys()]:
            self.sensor_dict[sensor] = 1
            self.num_sensors = int(sum(self.sensor_dict.values()))

    def get_used_sensor(self):
        return [key for (key, val) in self.sensor_dict.items() if val == 1]

    def receive(self, ser, model):
        global exitThread

        self.start_time = timeit.default_timer()
        while not exitThread:
            for val in ser.read():
                self.line.append(chr(val))
                if val == 10:
                    self.Arr = self.parsing_data(self.line)
                    self.sensor_data.append(self.Arr)
                    if len(self.sensor_data) > self.wide:
                        self.sensor_data.pop(0)
                        self.elapsed_time.pop(0)
                    receive_time = timeit.default_timer()
                    self.elapsed_time.append(receive_time - self.start_time)
                    self.line = []

                    self.num_receive += 1

                    if self.num_receive % self.show == 0:
                        drawnow(self.make_fig)

                    if self.type == "realtime_classifier":
                        if (self.num_receive % self.show == 0) & (self.num_receive > self.wide):
                            arr = np.array(self.sensor_data, dtype=np.float64).reshape(1, self.wide, self.num_sensors)
                            clf = realtime_classification(model, arr)
                            pred = realtime_prediction(clf)
                    if self.num_receive % 10000 == 0:
                        gc.collect()

    def make_fig(self):
        plt.title("title")
        # cmap_list = color_map[:len(self.sensor_data)]
        # plt.plot(self.sensor_data)
        # plt.ylim(self.low, self.high)  # Set y min and max values
        # plt.grid(True)
        legend = list(self.get_used_sensor())
        # plt.legend(legend)
        # plt.figure(1)
        plt.subplot(211)
        plt.plot(np.array(self.sensor_data)[:, :3])
        plt.ylim(self.low, self.high)
        plt.grid(True)
        plt.legend(legend[:3])

        plt.subplot(212)
        plt.plot(np.array(self.sensor_data)[:, 3:])
        plt.ylim(0, 1024)
        plt.grid(True)
        plt.legend(legend[3:])

    def parsing_data(self, data, strip='[]', split=','):
        self.line = "".join(data)
        self.dataArr = self.line.strip().strip(strip).split(split)
        self.dataArr = np.array([np.int(val) for val in self.dataArr])
        return self.dataArr[[idx for idx, (k, v) in enumerate(self.sensor_dict.items()) if v == 1]]


def set_graph_options(low_, high_):
    global low
    global high

    low = low_
    high = high_


def get_stop_situation():
    return extract.stop_listener


def get_data_folder():
    return extract.data_folder_path


def get_pattern():
    return extract.pattern
