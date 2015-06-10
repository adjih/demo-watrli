#! /bin/sh
#---------------------------------------------------------------------------
# http://watr.li/samr21-dev-setup-ubuntu.html

sudo apt-get install git pkg-config autoconf \
    libudev-dev libusb-1.0-0-dev libtool unzip \
    valgrind

#---------------------------------------------------------------------------

TMP=$(mktemp) &&
    rm -r $TMP &&
    mkdir -p $TMP &&
    cd $TMP &&
    git clone http://github.com/signal11/hidapi.git &&
    cd hidapi &&
    ./bootstrap &&
    ./configure &&
    make &&
    sudo make install &&
    sudo ln -s /usr/local/lib/libhidapi-hidraw.so.0 \
        /usr/lib/libhidapi-hidraw.so.0 || exit 1

#---------------------------------------------------------------------------

TMP=$(mktemp) &&
    rm -r $TMP &&
    mkdir -p $TMP &&
    cd $TMP &&
    git clone https://github.com/watr-li/OpenOCD.git openocd &&
    cd openocd &&
    ./bootstrap &&
    ./configure --enable-maintainer-mode \
                --enable-cmsis-dap \
                --enable-hidapi-libusb && \
    make && \
    sudo make install || exit 1

#---------------------------------------------------------------------------

sudo apt-get remove binutils-arm-none-eabi gcc-arm-none-eabi &&
    sudo add-apt-repository ppa:terry.guo/gcc-arm-embedded &&
    sudo apt-get update &&
    sudo apt-get install gcc-arm-none-eabi

#---------------------------------------------------------------------------

sudo usermod --append --groups dialout user

#---------------------------------------------------------------------------

sudo apt-get install libc6-dev-i386

#---------------------------------------------------------------------------

cd /etc/udev/rules.d && (
  test -e 99-hidraw-permissions.rules \
  || sudo bash -c "echo 'KERNEL==\"hidraw*\", SUBSYSTEM==\"hidraw\", MODE=\"0664\", GROUP=\"plugdev\"' > 99-hidraw-permissions.rules " )

#---------------------------------------------------------------------------
