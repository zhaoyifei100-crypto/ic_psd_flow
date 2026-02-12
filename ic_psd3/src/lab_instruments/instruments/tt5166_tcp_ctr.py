# coding: utf-8
import socket
import time
import struct
import sys

class TemperatureController:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.client_socket = None
        self.now_temperature = 0

        #yfzhao fix init bug
        #self._connect_to_device()

    def _modbus_tcp_msg(self, address, function_code, start_addr_high, start_addr_low, data_high, data_low):
        # create a modbus TCP message


        if sys.version_info.major == 3:
            package_start=bytes([0x00, 0x01, 0x00, 0x00, 0x00, 0x06])
            msg = package_start + bytes([address, function_code, start_addr_high, start_addr_low, data_high, data_low])
        else:
            #python2
            msg = '\x00\x01\x00\x00\x00\x06' + chr(address) + chr(function_code) + chr(start_addr_high) + chr(start_addr_low) + chr(data_high) + chr(data_low)
        return msg

    def _connect_to_device(self):
        # create a socket object and connect to the device
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip_address, self.port))
        #if sys.version_info.major == 3:
            #self.client_socket.setblocking(False)
    def _off_connect(self):
        #add try
        try:
            self.client_socket.close()
            return
        except:
            # if error do nothing
            return



    def _set_temperature(self, temperature):
        if temperature >= 0:
            temperature_hex = hex(int(temperature * 10))[2:].zfill(4)
        elif temperature < 0:
            temperature_hex = hex(65536 + int(temperature * 10))[2:].zfill(4)  
        # set the temperature on the device
        temperature_str = str(temperature_hex)
        data_high = int(temperature_str[:2], 16)
        data_low  = int(temperature_str[2:], 16)

        self._connect_to_device()
        msg = self._modbus_tcp_msg(0x00, 0x06, 0x00, 0x26, data_high, data_low)
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        self._off_connect()

        return response

    def _display_temperature(self):
        self._connect_to_device()
        # read the temperature from the device and display it
        msg = self._modbus_tcp_msg(0x00, 0x03, 0x00, 0x00, 0x00, 0x01)
        self.client_socket.send(msg)
        response = self.client_socket.recv(1024)
        self._off_connect()
        temperature = struct.unpack('!h', response[-2:])[0] / 100.0
        return temperature

    def _check_temperature(self, temperature):
        self._set_temperature(temperature)
        print("instrument::set_temperature is " + str(temperature) + " deg")
        while True:
            try:
                self.now_temperature = self._display_temperature()
            except:
                print("instrument::get temp error, dont care, continue.")
                #maybe connection wrong
                self._off_connect()
                #ADD error detect, yfzhao
                time.sleep(1)
                continue
            print("instrument::now temper is ", str(self.now_temperature) + " deg")
            time.sleep(1)
            if abs(self.now_temperature - temperature) < 0.3:
                break
            elif self.now_temperature == 150:
                break
        print("instrument::target temper is already")

    def _turn_on_power(self):
        self._connect_to_device()
        # turn on the power to the device
        msg = self._modbus_tcp_msg(0x00, 0x05, 0x00, 0x00, 0xff, 0x00)
        self.client_socket.send(msg)
        self._off_connect()

    def _turn_off_power(self):
        self._connect_to_device()
        # turn off the power to the device
        msg = self._modbus_tcp_msg(0x00, 0x05, 0x00, 0x01, 0xff, 0x00)
        self.client_socket.send(msg)
        self._off_connect()

    def temper_ctr(self, temperature):
        #self._connect_to_device()
        # turn on the power to the device
        self._turn_on_power()

        self._check_temperature(temperature)
        return temperature

    def turn_off_controller(self):
        if self.client_socket is not None:
            self._turn_off_power()
            time.sleep(1)  # 增加延时等待电源关闭
            self.client_socket.close()


            
            
if __name__ == '__main__':
    controller = TemperatureController('192.168.6.211', 3000)
    #controller = TemperatureController('192.168.6.211', 5900)
    #controller._turn_on_power()
    controller.temper_ctr(53)
    time.sleep(10)

    #controller._turn_on_power()
    print(controller._display_temperature())


    controller.turn_off_controller()
    
      