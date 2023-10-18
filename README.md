# Profiling IoT botnet activty (BotPro)
### Project Information:

The highly heterogeneous nature of IoT devices and their broad deployments have resulted in the emergence of numerous security issues and measurement-based difficulties, which strongly impede the collection, analysis, and correlation of IoT-centric data. Therefore, it is significantly important to build an empirical ground truth data and perform a macroscopic measurements analysis in order to adequately profile and track the activity of IoT botnet the wild. 


-----------------

# BotPro Analysis Dashboard

BotPro is an open-source cybersecurity dashboard for profiling IoT botnet activity. This tool offers a range of features and visualizations to help you analyze and understand the behavior of IoT botnets.

![BotPro Screenshot](screenshot.png)

## Installation

Follow these steps to set up BotPro on your local machine:

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

- 
### 1. Clone the Repository

bash
git clone https://github.com/almazarqi/BotPro.git
cd BotPro


### 2. Create a Virtual Environment
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS and Linux
source venv/bin/activate


### 3. Install Dependencies

pip install -r requirements.txt



#### Dataset:
The first layer of our proposed framework aims to build a real ground truth data. In order to build such data, it is essential to operate with Open-source intelligence (OSINT) feeds that presents real IoT-based botnets traffic. Globally distributed honeypots has been utilized to simulate any vulnerabilities which can easily be compromised by malicious actors. Real malicious events, including scanning and infections can be collected by monitoring such honeypots.

## Project Outline
### Services
#### - Attack Honeypots:
We collected cyber threat intelligence (CTI) data generated by attack honeypots. The honeypots detect active botnets by emulating hundreds of vulnerable IoT devices, including IP cameras, smart home devices and consumer-grade routers frequently targeted by botnets that scan the internet and engage in malicious activity.
#### - IP address reputation:
Four different IP global IP blacklist databases used in this work including: (i) Spamhaus, (ii) Barracuda, (iii) Spam Open Relay Blocking System (SORBS, and (iv) Composite Blocking List (CBL).

#### - BGP routing:
#### - DNS:
#### - Geographic distribution:


