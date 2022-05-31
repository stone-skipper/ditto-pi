from tuning import Tuning
import usb.core
import usb.util
import time
import socketio


dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
sio = socketio.Client()

if dev:
    Mic_tuning = Tuning(dev)
    print(Mic_tuning.direction)

    def send_sensor_readings():
        while True:
            prev_reading = Mic_tuning.direction
            print(prev_reading, Mic_tuning.direction)
            time.sleep(1)

            if Mic_tuning.direction > prev_reading + 3 or Mic_tuning.direction < prev_reading - 3:
                sio.emit('my_message', {'doa': Mic_tuning.direction})
                print('emitted doa : ', Mic_tuning.direction)
        # while True:
        #     sio.emit('my_message', {'doa':Mic_tuning.direction})
        #     sio.sleep(0.5)

    @sio.event
    def connect():
        print('connection established')
        sio.emit('connect', {'connection': 'true'})
        sio.start_background_task(send_sensor_readings)

    @sio.event
    def disconnect():
        print('disconnected from server')
        sio.emit('disconnect', {'connection': 'false'})

    sio.connect('http://192.168.50.106:5000',
                headers={'device_id': 'raspberrypi'})

    while True:
        try:
            # with open('/var/www/html/data.csv', 'a') as datafile:
            #     datafile.write(str(Mic_tuning.direction) + "\n")
            # print(Mic_tuning.direction)
            # readings[0] = {'doa': Mic_tuning.direction}
            # print(readings)
            # data = json.dumps(readings)
            # response = requests.put(url, headers=header, data=data[0])
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
