# IoTCANbus

## Setup the vcan
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

## Install the python library
pip install python-can