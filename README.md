# Magic Chess Board

> **COMING SOON! An open-source high-tech electronic chessboard. _Not finished yet!_ Once this project is finished I will share links to a tutorial.**

## Hardware and Electronics Setup

## Software Setup instructions

- Install rpi OS lite, enable SSH

### Python dependencies

SSH into your pi and type this to install Git and venv: `sudo apt update && sudo apt install git python3-venv -y` . It will take a minute or two.

Then type `git clone https://github.com/scitronboy/open-magic-chess.git` to download the code.

Then type `cd open-magic-chess` to change into the directory. Now you will need the following:

- Bluetooth gobject requirements for bluetooth server - install with `sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0`
- Venv
- Python requirements (python-chess, dbus, gpiozero, etc.) - install with `sudo pip3 install -r requirements.txt`
- Stockfish 8 or higher - install with `sudo apt install stockfish -y`

### Enable I2C

You will need to enable I2C on the raspberry pi: type `sudo raspi-config` and then go to “Interface Options” > “I2C” and enable it.

You might also need to type `sudo nano /etc/modules` and then add the following to the bottom of the file:

    i2c-bcm2708
    i2c-dev

Then press `Ctr+x` then `y` then enter/return then `sudo reboot` to reboot the pi.

## License

This project is licensed under the MIT License.

You are free to modify and distribute copies of this software (read license for more details). If you do so, please credit this repository.
