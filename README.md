# Graphtec GL840 interface for Python
Python script for reading values from Graphtec (GL840) device with PyVisa. Serves as minimum working example.

# Workings
The Graphtec class has been proven to work with a Graphtec GL840, and might work with other products from Graphtec since they have the same interfacing. Graphtec GL840 was connected via a ethernet hub to the computer. 

# Tips
- Check first if you can interface with the Graphtec by accessing the IP address in a browser. Graphtec IP can be found and changed on the device at "Menu > I/F > IP ADDRESS".
- See the manuals [APS GL-Connection](http://www.graphtec.co.jp/site_download/manual/APS(GL-Connection)-UM-159-05.pdf) and [Graphtec GL840](http://www.graphtec.co.jp/site_download/02_manual/data/GL840-UM-852.pdf) 
- The type of connection might be different, for me it was a Socket connection (line 13). See types of connections at [PyVisa documentation](https://pyvisa.readthedocs.io/en/1.8/names.html#visa-resource-syntax-and-examples)
