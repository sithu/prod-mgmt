sudo apt-get install uuid-dev xsltproc docbook-xsl
wget http://mosquitto.org/files/source/mosquitto-1.4.5.tar.gz
tar -xzf mosquitto-1.4.5.tar.gz
cd mosquitto-1.4.5
sudo make 
sudo make install