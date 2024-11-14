# Maico Powerbox WS 75

![License](https://img.shields.io/badge/license-MIT-green)
![HACS Custom Integration](https://img.shields.io/badge/HACS-Custom-orange.svg)

A custom integration for Home Assistant to control and monitor the Maico Powerbox WS 75 ventilation system. The device provides decentralized ventilation with heat and humidity recovery.

With this integration, you can automate, monitor, and manage key features of the Maico Powerbox WS 75, including mode switching, airflow rate, temperature, and humidity tracking directly from Home Assistant.

## Features

- **Mode Control**: Switch between ventilation modes.
- **Change device parameter**: Switch between ventilation modes.
- **Temperature and Humidity Monitoring**: Real-time tracking of temperatures and air humidity.
- **Real time Energy Monitoring**: Real-time tracking of power consumption.
- **Real time device parameter monitoring**: Real-time tracking of device parameters (air flow, internal states, etc.)
## Installation

1. **Download via HACS**:
   - Make sure [HACS](https://hacs.xyz/) is installed on your Home Assistant.
   - In HACS, go to **Integrations** > **+ Explore & Download Repositories**.
   - Search for "Maico Powerbox WS 75 S/H" or add select the repository https://github.com/markusmauch/powerbox-ws-75-custom-integration manually
   - Click **Download** and follow the prompts to add the integration.

2. **Manual Installation**:
   - Clone or download this repository.
   - Copy the `maico_powerbox` folder to the `custom_components` directory within your Home Assistant configuration.
   - Restart Home Assistant.

## Configuration

After installation, add the integration to connect it with your Maico Powerbox device.

name: "Maico Powerbox"
host: "192.168.1.xx"  # IP address of your Maico Powerbox device
port: 80              # Port (default is 80, change if necessary)
unit_id: 60     # (Optional) Polling interval in seconds


## Support
If you want to support my work feel free to
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/markusmauch)