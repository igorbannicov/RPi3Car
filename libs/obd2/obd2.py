# -*- coding: utf-8 -*-
"""
OBD2 Class file
"""
import os
import bluetooth
import subprocess
from time import sleep
from threading import Thread, Event
from obd import OBDStatus, OBD, commands, logger, console_handler
from configobj import ConfigObj
from libs.utils import celsius_to_kelvin
from libs.obd2.gauges import GaugeLabel, GaugeGraph
logger.removeHandler(console_handler)


class OBD2(Thread):
    """
    OBD2 Class
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.passkey = kwargs['passkey']
        self.baud = kwargs['baud']
        self.protocol = kwargs['protocol']
        self.vef = kwargs['vef']
        self.eds = kwargs['eds']
        self.parent = kwargs['parent']
        self.port = None
        self.path = os.getcwd() + "/configs/pids.ini"
        self.config = ConfigObj(self.path)
        self.plottime = float(kwargs['time'])
        self.connection = None
        self.mai = 28.97    # Молекуляная масса воздуха
        self.rgas = 8.314      # Газовая постоянная
        self.d_gasoline = 750      # Плотность бензина (АИ-95)
        self.daemon = True
        self.pids = {}
        mypids = list(self.config['PIDS'].sections)
        for pid in mypids:
            gtype = self.config['PIDS'][pid]['type']
            if gtype == 'graph':
                try:
                    color = list(self.config['PIDS'][pid]['color'])
                except:
                    color = [1, 1, 1, 1]
                gauge = GaugeGraph(name=self.config['PIDS'][pid]['name'],
                                   color=color,
                                   grid=True,
                                   gtype=gtype,
                                   parent=self)
                self.pids[pid] = {'values': [],
                                  'name': self.config['PIDS'][pid]['name'],
                                  'gauge': gauge}
            elif gtype == 'label':
                try:
                    color = list(self.config['PIDS'][pid]['color'])
                except:
                    color = [1, 1, 1, 1]
                gauge = GaugeLabel(name=self.config['PIDS'][pid]['name'],
                                   color=color,
                                   gtype=gtype,
                                   parent=self)
                self.pids[pid] = {'value': 0,
                                  'name': self.config['PIDS'][pid]['name'],
                                  'gauge': gauge}

        self.start()
        self._stop_event = Event()

    def init_bt(self):
        """
        Connect to OBDII bt device
        """
        devices = bluetooth.discover_devices(duration=4,
            lookup_names=True,
            flush_cache=True,
            lookup_class=False)
        print(devices)
        for device in devices:
          if device[1] == 'OBDII':
            addr = device[0]
            subprocess.call("kill -9 `pidof bluetooth-agent`",shell=True)
            port = 1
            status = subprocess.call("bluetooth-agent " + self.passkey + " &",shell=True)
            try:
                self.port = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.port.connect((addr,port))
            except bluetooth.btcommon.BluetoothError as err:
                print('Bluetooth couldn\'t connect due to error: \n')
                print(err)
                pass

    def run(self):
        """
        Main class function
        :return:
        """
        while True:
            if self.connection:
                if not self.connection.status() == OBDStatus.CAR_CONNECTED:
                    self.connection = OBD(self.port, self.baud, self.protocol)
                elif self.connection.status() == OBDStatus.CAR_CONNECTED:
                    self.get_all_pids()
            else:
                self.init_bt()
                self.connection = OBD(self.port, self.baud, self.protocol)

    def get_pid(self, pid):
        """
        Get data for specific PID
        :param pid:
        :return:
        """
        if self.connection.status() == OBDStatus.CAR_CONNECTED:
            cmd = commands[pid]
            response = self.connection.query(cmd)
            if response == "":
                return None
            else:
                res = response.value.magnitude
            return res
        else:
            print("Not connected to OBD2")
            return None

    def get_all_pids(self):
        """
        Get data from all pids from internal list
        :return:
        """
        for pid in self.pids.keys():
            val = self.get_pid(pid)
            gtype = self.pids[pid]['gauge'].gtype
            if gtype == 'graph':
                values_list = self.pids[pid]['values']
                values_list.append(val)
                self.pids[pid]['values'] = values_list[-49:]
            if gtype == 'label':
                self.pids[pid]['value'] = val
            self.pids[pid]['gauge'].update()
            sleep(self.plottime)

    def fuel_consumption(self):
        """
        Calculates fuel consumption based on MAP sensor
        :return:
        """
        rpm = int(self.get_pid("RPM"))
        intake_temp = celsius_to_kelvin(self.get_pid("INTAKE_TEMP"))
        intake_pressure = self.get_pid("INTAKE_PRESSURE")
        speed = self.get_pid("SPEED")
        if speed > 0:
            if (rpm != -999) and (intake_temp != -999) and (intake_pressure != -999):
                vfl = ((((((rpm * intake_pressure / (intake_temp * 2)) / 60) * (self.vef / 100) *
                          self.eds * self.mai / self.rgas) / 14.7) /
                        self.d_gasoline) * 3600) * 100 / speed
            else:
                vfl = 0
            units = "LPK"
        else:
            if (rpm != -999) and (intake_temp != -999) and (intake_pressure != -999):
                vfl = (((((rpm * intake_pressure / (intake_temp * 2)) / 60) *
                         (self.vef / 100) * self.eds * self.mai / self.rgas) / 14.7) /
                       self.d_gasoline) * 3600
            else:
                vfl = 0
            units = "LPH"
        return (vfl, units)

    def get_available_pids(self):
        """
        Get a list of available PIDS
        :return:
        """
        for command in self.connection.supported_commands:
            try:
                response = self.connection.query(command)
                print("PID : " + str(command) + " ->  " + str(response.value))
                sleep(self.plottime)
            except:
                print("PID : " + str(command) + "said OOPS!")

    def get_errors(self):
        """
        Get the current errors list
        :return:
        """
        try:
            cmd = commands["GET_DTC"]
            response = self.connection.query(cmd)
            if response == "":
                res = "None"
            else:
                res = response.value
            return res
        except Exception as exceptn:
            return exceptn

    def clear_errors(self):
        """
        Clear errors
        :return:
        """
        try:
            cmd = commands["CLEAR_DTC"]
            self.connection.query(cmd)
            return None
        except Exception as exceptn:
            return exceptn
