# Magic Chess Board

> **COMING SOON! An open-source high-tech electronic chessboard. _Not finished yet!_ Once this project is finished I will share links to a tutorial.**

## Hardware and Electronics Setup

## Software Setup Instructions

- Install rpi OS lite, enable SSH

### Installing the Software

You will need to install the following components (in this order)

1. Required packages. This includes git, build requirements for the python packages, and Stockfish 8 or higher (the chess engine). Install all this with `sudo apt install git libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0 stockfish -y`. It might take a while to install everything.
2. The chessboard software: download this with `git clone https://github.com/bashbaugh/magic-chess.git && cd magic-chess`
3. Python requirements (python-chess, gpiozero, etc.) - install with `sudo pip3 install -r requirements.txt`

### Enable I2C

You will need to enable I2C on the raspberry pi: type `sudo raspi-config` and then go to “Interface Options” > “I2C” and enable it.

You might also need to type `sudo nano /etc/modules` and then add the following to the bottom of the file:

    i2c-bcm2708
    i2c-dev

Then press `Ctr+x` then `y` then enter/return then `sudo reboot` to reboot the pi.

## License

This project is licensed under the MIT License.

You are free to modify and distribute copies of this software (read license for more details). If you do so, please credit this repository.
