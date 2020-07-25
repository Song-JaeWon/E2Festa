from receive import *
import extract
import threading
import training
import serial
import signal
from realtime_classification import *


def run():
    print("Select Process:")
    print("1. Data Receive \n2. Read Data and Compile Model\n3. Test Score\n4. Predict")
    num = int(input("Select Num : "))
    if num == 1:
        signal.signal(signal.SIGINT, handler)

        receiver = Receiver("IMU_1", "IMU_2", "IMU_3", "IMU_4", "IMU_5", "IMU_6", "IR_L", "IR_R", type="receiver")
        receiver.set_using_sensor("IMU_4", "IMU_5", "IMU_6", "IR_L", "IR_R")
        extract.set_extract_options(pattern_name="yy")

        # receiver.set_port_num("COM7")
        # receiver.set_baud_rate(9600)
        """
        wide = input("wide[Default=100] : ")
        show = input("Frequency[Default=10] : ")
        low = input("Y Limitation - below [Default=-10000]: ")
        high = input("Y Limitation - upper [Default=10000]: ")
        graph_options = [wide, show, low, high]

        receiver.set_graph_option()
        """
        print("Receiving Data...")
        stop_receive = get_stop_situation()
        ser = serial.Serial("COM7", 9600, timeout=0)
        time.sleep(0.1)1
        ser.readline()
        time.sleep(0.1)
        ser.readline()
        thread_serial = threading.Thread(target=receiver.receive, args=(ser, None))
        thread_serial.start()

        extract.sensor_data = receiver.sensor_data

        with extract.Listener(on_press=extract.on_press) as listener:
            while not extract.stop_listener:
                listener.join()
        print("Successfully Received!")

    elif num == 2:
        trainer = training.Training()
        train_X, test_X, train_y, test_y = trainer.split()

        model = trainer.get_model()
        model = training.compile_model(model)

        model, history = training.training_model(model=model, X=train_X, y=train_y, validation_split=2/9)
        # print(model.predict(test_X[0].reshape(1,31,5)))

        training.get_learning_curve(history)

    elif num == 3:
        signal.signal(signal.SIGINT, handler)

        receiver = Receiver("1", "2", "3", "4", "5", "6", "7", "8")
        receiver.set_using_sensor("4", "5", "6", "7", "8")
        ser = serial.Serial("COM7", 9600, timeout=0)
        model = get_model()

        time.sleep(0.1)
        ser.readline()
        time.sleep(0.1)
        ser.readline()
        thread_serial = threading.Thread(target=receiver.receive, args=(ser, model))
        thread_serial.start()


"""
def get_exitThread():
    return extract.exitThread
"""

def handler(signum, frame):
    exitThread = extract.exitThread
    exitThread = True


if __name__ == "__main__":
    run()
