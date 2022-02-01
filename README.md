# Project-Hydroponic-Farm :computer: :seedling:

## Installation

- #### Update/Upgrade system packages
  ``` bash
  sudo apt-get update && sudo apt-get upgrade
  ```

- #### Install git
  ``` bash
  sudo apt install git -y
  ```

- #### Install / Config Docker
  ``` bash
  curl -sSL https://get.docker.com | sh
  sudo usermod -aG docker ${USER}
  sudo systemctl enable docker
  ```

- #### Install pip3 (for pip Docker-Compose)
  ``` bash
  sudo apt-get install libffi-dev libssl-dev 
  sudo apt install python3-dev
  sudo apt-get install -y python3 python3-pip
  ```

- #### Install Docker-Compose
  ``` bash
  sudo pip3 install docker-compose
  ```

- #### Enable Cameara/I2C (reboot device after finish this step)
  ``` bash
  sudo raspi-config
    
    -> 3 Interface Options
      -> I1 Legacy Camera
        -> <Yes>
        
    -> 3 Interface Options
      -> I5 I2C
        -> <Yes>
        
    -> <Finish>
  ```

- #### Download Project
  ``` bash
  git clone https://github.com/stupidwolfy/Project-Hydroponic-Farm.git
  ```

- #### Config Project (optional)
    #### If you device hostname is not ```raspberrypi``` (default)
    - Edit file ``` docker-compose.yml ```
      - at ```HOST_HOSTNAME: ${HOST_HOSTNAME:-raspberrypi}``` change "raspberrypi" to your device hostname
    - Edit file ``` services/frontend/.env ```
      - at ```VUE_APP_HOST_HOSTNAME=raspberrypi``` change "raspberrypi" to your device hostname

- #### Build/Run Project
  ``` bash
  cd Project-Hydroponic-Farm/
  docker-compose up -d
  ``` 
  ---
  
## Usage
  #### From other device in same local network.
  - #### Access Frontend : Go to http://raspberrypi.local:8080 or ```http://<your-device-hostname>.local:8080```
  - #### Access Backend : Go to http://raspberrypi.local:5000 or ```http://<your-device-hostname>.local:5000```
