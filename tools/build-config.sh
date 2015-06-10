#! /bin/sh
#---------------------------------------------------------------------------

sudo apt-get install bison flex wget || exit 1

test -e cfgtool-1.00.tar.gz || \
wget http://rosand-tech.com/downloads/cfgtool-1.00.tar.gz &&
    tar -xvzf cfgtool-1.00.tar.gz &&
    cd cfgtool-1.00 &&
    ./configure &&
    make || exit 1


test -e ../cfgtool-bin || mkdir ../cfgtool-bin || exit 1

cp cfgtool ../cfgtool-bin/ &&
    cp cfgtool.conf ../cfgtool-bin/ || exit 1


#---------------------------------------------------------------------------

cd ../cfgtool-bin || exit 1
echo "Old Config:"
./cfgtool -p ridge \
          -c serial \
          -C ./cfgtool.conf \
          -U channel:r: \
          -U power:r: \
          -U panid:r: \
          -U prefix:r: || exit 1

echo "New Config with channel 22 and panid 0x123"
./cfgtool -p ridge \
          -c serial \
          -C ./cfgtool.conf \
          -U channel:w:22: \
          -U panid:w:0x123: || exit 1

#--------------------------------------------------

#  Typo in webpage:

#cp cfgtool ../cfgtool-bin/ &&
#    cp cftool.conf ../cfgtool-bin/

#---------------------------------------------------------------------------
