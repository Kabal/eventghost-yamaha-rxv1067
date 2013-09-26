eg.RegisterPlugin(
    name = "Yamaha RX-V1067 Receiver",
    author = "Tom Wilson",
    version = "0.1.0",
    kind = "external",
    guid = "f3de6b4f-5aba-4c88-ad5e-01adb6c9512c}",
    url = "",
    description = (''),
    canMultiLoad = True,
    createMacrosOnAdd = True,
)


# Now we import some other things we will need later
import new
import thread

# Define commands
# (name, title, description (same as title if None), command)
commandsList = (
(
    'Sleep',
    (
        ('Sleep Off', 'Turn off sleep', None, '@MAIN:SLEEP=Off'),
        ('Sleep 120 min', 'Sleep in 120 minutes', None, '@MAIN:SLEEP=120 min'),
        ('Sleep 90 min', 'Sleep in 90 minutes', None, '@MAIN:SLEEP=90 min'),
        ('Sleep 60 min', 'Sleep in 60 minutes', None, '@MAIN:SLEEP=60 min'),
        ('Sleep 30 min', 'Sleep in 30 minutes', None, '@MAIN:SLEEP=30 min'),
    )
),
(
    'Power',
    (
        ('PowerOn', 'Power on', None, '@SYS:PWR=On'),
        ('PowerOff', 'Power off', None, '@SYS:PWR=Standby')
    )
),
(
'Output',
    (
        ('HDMI1', 'HDMI Output 1', None, '@MAIN:HDMIOUT=OUT1'),
        ('HDMI2', 'HDMI Output 2', None, '@MAIN:HDMIOUT=OUT2'),
        ('HDMI1+2', 'HDMI Output 1+2', None, '@MAIN:HDMIOUT=OUT1 + 2'),
        ('HDMI Off', 'HDMI Output Off', None, '@MAIN:HDMIOUT=Off')
    )
),
(
    'Volume',
    (
        ('Mute Off', 'Mute off', None, '@MAIN:MUTE=Off'),
        ('Mute On', 'Mute on', None, '@MAIN:MUTE=On'),
        ('Mute toggle', 'Mute toggle', None, '@MAIN:Mute=On/Off')
    )
),
(
    'Inputs',
    (
        ('Tuner', 'Tuner', None, '@MAIN:INP=TUNER'),
        ('MULTI CH', 'Multi Channel', None, '@MAIN:INP=MULTI CH'),
        ('AV1', 'AV1', None, '@MAIN:INP=AV1'),
        ('AV2', 'AV2', None, '@MAIN:INP=AV2'),
        ('AV3', 'AV3', None, '@MAIN:INP=AV3'),
        ('AV4', 'AV4', None, '@MAIN:INP=AV4'),
        ('AV5', 'AV5', None, '@MAIN:INP=AV5'),
        ('AV6', 'AV6', None, '@MAIN:INP=AV6'),
        ('AV7', 'AV7', None, '@MAIN:INP=AV7'),
        ('V-AUX', 'V-AUX', None, '@MAIN:INP=V-AUX'),
        ('AUDIO1', 'AUDIO1', None, '@MAIN:INP=AUDIO1'),
        ('AUDIO2', 'AUDIO2', None, '@MAIN:INP=AUDIO2'),
        ('AUDIO3', 'AUDIO3', None, '@MAIN:INP=AUDIO3'),
        ('AUDIO4', 'AUDIO4', None, '@MAIN:INP=AUDIO4'),
        ('iPod', 'iPod', None, '@MAIN:INP=iPod'),
        ('Bluetooth', 'Bluetooth', None, '@MAIN:INP=Bluetooth'),
        ('UAW', 'UAW', None, '@MAIN:INP=UAW'),
        ('USB/NET', 'USB/NET', None, '@MAIN:INP=USB/NET'),
        ('PC', 'PC', None, '@MAIN:INP=PC'),
        ('NET RADIO', 'Internet Radio', None, '@MAIN:INP=NET RADIO'),
        ('USB', 'USB', None, '@MAIN:INP=USB')
    )
),
(
    'Scenes',
    (
        ('Scene 1', 'Select scene 1', None, '@MAIN:SCENE=Scene 1'),
        ('Scene 2', 'Select scene 2', None, '@MAIN:SCENE=Scene 2'),
        ('Scene 3', 'Select scene 3', None, '@MAIN:SCENE=Scene 3'),
        ('Scene 4', 'Select scene 4', None, '@MAIN:SCENE=Scene 4'),
        ('Scene 5', 'Select scene 5', None, '@MAIN:SCENE=Scene 5'),
        ('Scene 6', 'Select scene 6', None, '@MAIN:SCENE=Scene 6'),
        ('Scene 7', 'Select scene 7', None, '@MAIN:SCENE=Scene 7'),
        ('Scene 8', 'Select scene 8', None, '@MAIN:SCENE=Scene 8'),
        ('Scene 9', 'Select scene 9', None, '@MAIN:SCENE=Scene 9'),
        ('Scene 10', 'Select scene 10', None, '@MAIN:SCENE=Scene 10'),
        ('Scene 11', 'Select scene 11', None, '@MAIN:SCENE=Sceen 11'),
        ('Scene 12', 'Select scene 12', None, '@MAIN:SCENE=Scene 12'),
    )
)
)

class YamahaV1067SerialAction(eg.ActionClass):
    
    def __call__(self):
        self.plugin.sendCommand(self.serialcmd)



class YamahaV1067SerialsetVolumeAbsolute(eg.ActionWithStringParameter):
    name='Set absolute volume'
    description='Sets the absolute volume'

    def __call__(self, volume):
        return self.plugin.setVolume(volume, False)

    def GetLabel(self, volume):
        return "Set Absolute Volume to %d" % volume
        
    def Configure(self, volume=-40):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(volume, min=-80.5, max=16.5)
        panel.AddLine("Set absolute volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())



class YamahaV1067SerialsetVolumeRelative(eg.ActionWithStringParameter):
    name='Set relative volume'
    description='Sets the relative volume'

    def __call__(self, volume):
        return self.plugin.setVolume(volume, True)

    def GetLabel(self, volume):
        return "Set Relative Volume to %d" % volume
        
    def Configure(self, volume=0):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(volume, min=-80.5, max=16.5)
        panel.AddLine("Set relative volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())



class YamahaV1067Serial(eg.PluginClass):
    def __init__(self):
        self.serial = None
        self.response = None

        for groupname, list in commandsList:
            group = self.AddGroup(groupname)
            for classname, title, desc, serial in list:
                if desc is None:
                    desc = title
                clsAttributes = dict(name=title, description=desc, serialcmd=serial)
                cls = new.classobj(classname, (YamahaV1067SerialAction,), clsAttributes)
                group.AddAction(cls)

            if (groupname == 'Volume'):
                group.AddAction(YamahaV1067SerialsetVolumeAbsolute)
                group.AddAction(YamahaV1067SerialsetVolumeRelative)


    def sendCommandSerial(self, cmd):
        if self.serial is None:
            return True

        # Send command
        cmd += '\r\n'
        self.serial.write(cmd)

        return True


    # Serial port reader
    def reader(self):
        line=""
        while self.readerkiller is False:
            ch=self.serial.read()
            if ch=='\r':
                continue;
            if ch=='\n':
                if line != "":
                    self.parseLine(line)
                    self.TriggerEvent(line)
                    line=""
            else:
                line+=ch

    def parseLine(self, line):
        if line.startswith("@MAIN:VOL="):
            self.volume = float(line.split("=")[1])
            print "The volume is now: %f" % self.volume

    def getResponseFloat(self):
        return float(self.response)


    def getResponseInt(self):
        self.PrintError(self.response)
        if (self.response[0] == '-' or self.response[0] == '+'):
            if not self.response[1:].isdigit():
                self.PrintError("Bad response")
                return None

        elif not self.response.isdigit():
            self.PrintError("Bad response")
            return None

        return int(self.response)


    def sendCommand(self, serialcmd):
        result = self.sendCommandSerial(serialcmd)
        return result


    def setVolume(self, volume, relative):

        if relative and self.volume is None:
            # can't set the relative volume if we don't know the current state...
            return

        if relative:
            volume = self.volume + volume

        if volume > 16.5:
            volume = 10
        elif volume < -80.5:
            volume = -80.5
        
        command = "@MAIN:VOL=%.1f" % (volume)
        self.sendCommandSerial(command)
        return volume


    def getInitialState(self):
        self.sendCommandSerial("@MAIN:VOL=?")


    def __start__(self, port=0):
        try:
            self.serial = eg.SerialPort(port)
            self.serial.baudrate = 9600
            self.serial.timeout = 0.5
            self.serial.setDTR(1)
            self.serial.setRTS(1)
            self.readerkiller = False
            thread.start_new_thread(self.reader,())

            self.getInitialState()
        except:
            self.PrintError("Unable to open serial port")


    def __stop__(self):
        self.readerkiller = True
        if self.serial is not None:
            self.serial.close()
            self.serial = None


    def Configure(self, port=0):
        portCtrl = None

        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)

        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())
        

