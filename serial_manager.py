# coding: utf-8
import wx
import random

import serial
from serial import SerialException
from serial.tools.list_ports import comports


G_CURRENT_CONN = None


def get_com_list():
    """Get serial port list."""
    coms = comports()
    device_names = [item.device for item in coms]
    return device_names


class MainPanel(wx.Panel):

    """Main panel defined here."""

    def __init__(self, parent):
        """Intializer of the main panel."""
        wx.Panel.__init__(self, parent)

        radio_list = ['On', 'Off', 'Fault']

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.main_controller = wx.RadioBox(
            self, label='Main Controller',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_COLS
        )
        self.sizer2.Add(self.main_controller, 1, wx.EXPAND)

        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.rb1 = wx.RadioBox(
            self, label='Switch Number 1',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer3.Add(self.rb1, 1, wx.EXPAND)
        self.rb2 = wx.RadioBox(
            self, label='Switch Number 2',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer3.Add(self.rb2, 1, wx.EXPAND)
        self.rb3 = wx.RadioBox(
            self, label='Switch Number 3',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer3.Add(self.rb3, 1, wx.EXPAND)
        self.rb4 = wx.RadioBox(
            self, label='Switch Number 4',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer3.Add(self.rb4, 1, wx.EXPAND)
        self.rb5 = wx.RadioBox(
            self, label='Switch Number 5',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer4.Add(self.rb5, 1, wx.EXPAND)
        self.rb6 = wx.RadioBox(
            self, label='Switch Number 6',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer4.Add(self.rb6, 1, wx.EXPAND)
        self.rb7 = wx.RadioBox(
            self, label='Switch Number 7',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer4.Add(self.rb7, 1, wx.EXPAND)
        self.rb8 = wx.RadioBox(
            self, label='Switch Number 8',  choices=radio_list,
            majorDimension=3, style=wx.RA_SPECIFY_ROWS
        )
        self.sizer4.Add(self.rb8, 1, wx.EXPAND)

        # Use some sizers to see layout options
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.sizer3, 1, wx.EXPAND)
        self.sizer.Add(self.sizer4, 1, wx.EXPAND)

        # Layout sizers
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)

        # Set a timer to fetch com data and display
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(5000)

    def OnTimer(self, evt):
        """Fetch data from com and display it."""
        global G_CURRENT_CONN
        if G_CURRENT_CONN is None:
            # self.dlg = wx.MessageDialog( self, "Com connection is not open!", "Notify", wx.OK)
            # self.dlg.ShowModal()
            # self.dlg.Destroy()
            pass
        else:
            main_controller_value = random.randint(0, 2)
            rb1_value = random.randint(0, 2)
            rb2_value = random.randint(0, 2)
            rb3_value = random.randint(0, 2)
            rb4_value = random.randint(0, 2)
            rb5_value = random.randint(0, 2)
            rb6_value = random.randint(0, 2)
            rb7_value = random.randint(0, 2)
            rb8_value = random.randint(0, 2)
            self.main_controller.SetSelection(main_controller_value)
            self.rb1.SetSelection(rb1_value)
            self.rb2.SetSelection(rb2_value)
            self.rb3.SetSelection(rb3_value)
            self.rb4.SetSelection(rb4_value)
            self.rb5.SetSelection(rb5_value)
            self.rb6.SetSelection(rb6_value)
            self.rb7.SetSelection(rb7_value)
            self.rb8.SetSelection(rb8_value)


class ConfigPanel(wx.Panel):

    """Configuration panel defined here."""

    def __init__(self, parent):
        """Intializer of the configuration panel."""
        wx.Panel.__init__(self, parent)
        self.voltage = wx.StaticText(self, label="Voltage:", pos=(20, 30))
        self.v_edit = wx.TextCtrl(self, value="Enter here the value", pos=(100, 25), size=(140,-1))
        self.current = wx.StaticText(self, label="Current:", pos=(20, 60))
        self.c_edit = wx.TextCtrl(self, value="Enter here the value", pos=(100, 55), size=(140,-1))

        # Save botton
        self.button =wx.Button(self, label="Save", pos=(100, 100))


class SettingsPanel(wx.Panel):

    """Settings panel defined here."""

    def __init__(self, parent):
        """Intializer of the settings panel."""
        wx.Panel.__init__(self, parent)
        self.s_line = wx.StaticText(self, label="Serial line to connect to:", pos=(20, 30))
        self.com_list = get_com_list()
        self.com_list = ['COM1'] if len(self.com_list) == 0 else self.com_list
        self.com_list_combo = wx.ComboBox(
            self, pos=(180, 25), size=(140, -1), value=self.com_list[0],
            choices=self.com_list, style=wx.CB_DROPDOWN|wx.CB_READONLY
        )

        self.speed = wx.StaticText(self, label="Speed(baud):", pos=(20, 60))
        self.speed_edit = wx.TextCtrl(self, value="9600", pos=(180, 55), size=(140,-1))

        self.data_bits = wx.StaticText(self, label="Data bits:", pos=(20, 90))
        self.db_edit = wx.TextCtrl(self, value="8", pos=(180, 85), size=(140,-1))

        self.stop_bits = wx.StaticText(self, label="Stop bits:", pos=(20, 120))
        self.sb_edit = wx.TextCtrl(self, value="1", pos=(180, 115), size=(140,-1))

        self.parity_list = ['None', 'Odd', 'Even', 'Mark', 'Space']
        self.parity_value_mapping = {
            self.parity_list[0]: serial.PARITY_NONE,
            self.parity_list[1]: serial.PARITY_EVEN,
            self.parity_list[2]: serial.PARITY_ODD,
            self.parity_list[3]: serial.PARITY_MARK,
            self.parity_list[4]: serial.PARITY_SPACE
        }
        self.parity = wx.StaticText(self, label="Parity:", pos=(20, 150))
        self.p_combo = wx.ComboBox(
            self, pos=(180, 145), size=(140, -1), value='None',
            choices=self.parity_list, style=wx.CB_DROPDOWN|wx.CB_READONLY
        )

        self.fc_list = ['None', 'XON/XOFF', 'RTS/CTS', 'DSR/DTR']
        self.flow_control = wx.StaticText(self, label="Flow Control:", pos=(20, 180))
        self.p_combo = wx.ComboBox(
            self, pos=(180, 175), size=(140, -1), value=self.fc_list[0],
            choices=self.fc_list, style=wx.CB_DROPDOWN|wx.CB_READONLY
        )

        # Connect botton
        self.button =wx.Button(self, label="Connect", pos=(180, 210))
        self.Bind(wx.EVT_BUTTON, self.OnConnect, self.button)

    def OnConnect(self, event):
        port = self.com_list_combo.GetStringSelection()
        baudrate = int(self.speed_edit.GetLineText(0))
        bytesize = int(self.db_edit.GetLineText(0))
        stopbits= int(self.sb_edit.GetLineText(0))
        timeout = 3
        parity_value = self.p_combo.GetStringSelection()
        fc_value = self.p_combo.GetStringSelection()
        parity = self.parity_value_mapping[parity_value]
        if fc_value == self.fc_list[0]:
            xonxoff, rtscts, dsrdtr = False, False, False
        else:
            xonxoff = True if fc_value == self.fc_list[1] else False
            rtscts = True if fc_value == self.fc_list[2] else False
            dsrdtr = True if fc_value == self.fc_list[3] else False

        try:
            global G_CURRENT_CONN
            G_CURRENT_CONN = serial.Serial(
                port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits,
                timeout=timeout, xonxoff=xonxoff, rtscts=rtscts, dsrdtr=dsrdtr, write_timeout=timeout
            )
        except ValueError:
            self.dlg = wx.MessageDialog( self, "Parameter not right, please verify!", "Notify", wx.OK)
        except SerialException:
            self.dlg = wx.MessageDialog( self, "Port is occupied or other error happened.", "Notify", wx.OK)
        else:
            self.dlg = wx.MessageDialog( self, "Connect successfully!", "Notify", wx.OK)
        finally:
            self.dlg.ShowModal()
            self.dlg.Destroy()


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title='Serial Manager', size=(500, 500))
    nb = wx.Notebook(frame)

    setting_panel = SettingsPanel(nb)
    main_panel = MainPanel(nb)
    config_panel = ConfigPanel(nb)
    nb.AddPage(setting_panel, 'Settings')
    nb.AddPage(main_panel, 'Panel')
    nb.AddPage(config_panel, 'Configuration')
    frame.Show()
    app.MainLoop()