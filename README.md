# This is an CO2 Sensor MQTT Bridge.
It forwards messages from the MH-Z19 Co2 sensor attached via serial to an mqtt topic in regular intervals.
It is useful if you want to monitor Co2 concentration in multiple rooms in Homeassistant.
My setup looks like this:

```
   Room 1                Room 2
 BridgeClient          MQTT Broker and HASS.io
  +-------+             +-------+
  |       |             |       |
  |       |             |       |
  | Raspi |+----------->| Raspi |
  |   1   |    MQTT     |   2   |
  |       |             |       |
  |       |             |       |
  +---+---+             +---+---+
      |                     |
      |                     |
   +--+--+               +--+--+
   |MZH19|               |MZH19|
   |-----|               |-----|
   |     |               |     |
   |     |               |     |
   |     |               |     |
   |     |               |     |
   +-----+               +-----+
```

On _Raspi1_, connect the MH-Z19 to the pis GPIOs:


|RPi Pin|MH-Z19|
|-------|------|
|Tx     |Rx    |
|Rx     |Tx    |
|Gnd    |Gnd   |
|5v     |Vin   |

![](http://gerneth.info/files/co2sensor.jpg)


Hacked toghether by Christoph Gerneth

How to run (on a pi - quick and hacky way):

```
git clone https://github.com/c7h/co2bridge.git
cd co2bridge
vim co2bridge.py # Edit the parameters (reminder hacky)
sudo pip install -r requirements.txt
sudo cp co2bridge.service /etc/systemd/system
service co2bridge start
```

if you want to autostart the service on boot, run

```
sudo service co2bridge enable
```


## Homeassistant Integration

You can monitor the CO2 concentration in [Homeassistant](https://www.home-assistant.io).
Add the following lines to your `configuration.yaml`.

```yaml
  - platform: mqtt
    name: "Meeting Room 1 Co2"
    state_topic: "devices/raspi/co2sensor"
    availability_topic: "devices/raspi/co2sensor/state"
    unit_of_measurement: "ppm"
    value_template: "{{ value_json.ppm }}"
  - platform: mqtt
    name: "Meeting Room 1 Temperature"
    state_topic: "devices/raspi/co2sensor"
    availability_topic: "devices/raspi/co2sensor/state"
    unit_of_measurement: "°C"
    value_template: "{{ value_json.temperature }}"
```


