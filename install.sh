#!/bin/bash

apt-get update
apt-get upgrade
apt-get -y install \
    bluetooth \
    libbluetooth-dev \
    libbluetooth3 \
    python3-pip \
    git \
    libgles2-mesa-dev \
    build-essential \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    libsdl-image1.2-dev \
    libsdl-mixer1.2-dev \
    libsdl-ttf2.0-dev \
    libsmpeg-dev \
    libsdl1.2-dev

pip3 install --upgrade pip
rm -f /usr/bin/pip3
ln -s /usr/local/bin/pip3 /usr/bin/pip3
pip3 install Cython
cd /home
git clone https://gitlab.com/igor.bannicov/R3C.git
cd R3C
pip3 install -r requirements.txt
garden install graph --app
garden install navigationdrawer --app

