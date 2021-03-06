# Graphtec GL840 interface for Python
Python script for reading values from [Graphtec GL840](http://www.graphtec.co.jp/en/instruments/gl840/index.html) device (see Figure 1) with PyVisa. Serves as minimum working example.

<p align="center">
<img src="https://github.com/HaralDev/GraphtecPython/blob/master/Graphtec_GL840.png" width="500">
  <br>Figure 1: Graphtec GL840 in operation
</p>

# Workings
The Graphtec class has been proven to work with a Graphtec GL840, and might work with other products from Graphtec since they have the same interfacing. Graphtec GL840 was connected via a ethernet hub to the computer. 

# Tips
- See the manuals [APS GL-Connection](http://www.graphtec.co.jp/site_download/manual/APS(GL-Connection)-UM-159-05.pdf) and [Graphtec GL840](http://www.graphtec.co.jp/site_download/02_manual/data/GL840-UM-852.pdf)
- Check first if you can interface with the Graphtec by accessing the IP address in a browser. Graphtec IP can be found and changed on the device at "Menu > I/F > IP ADDRESS".
- You computer's IP address first three numbers, so the x's in 192.168.1.8=x.x.x.8, **must** be the same as the Graphtec device. Consequently, the Graphtec IP address **must** be something like 192.168.1.9. This cost me some time to find out, it was somewhere in the [APS GL-Connection](http://www.graphtec.co.jp/site_download/manual/APS(GL-Connection)-UM-159-05.pdf) manual. So change it accordingly on the Graphtec device using tip 1! 
- The type of connection might be different, for me it was a Socket connection (line 13 in [GL840_example.py](https://github.com/HaralDev/GraphtecPython/blob/master/GL840_example.py)). See types of connections at [PyVisa documentation](https://pyvisa.readthedocs.io/en/1.8/names.html#visa-resource-syntax-and-examples)
- At start, sometimes the Graphtec does not seem to connect. Try accessing the Graphtec directly from browser (simply plug the ip address into the address bar). You should see an interface. Perhaps only one connection with the Graphtec may be open (depending on socket connection), so close the browser when you run the code. Code should work when the browser connection works, otherwise the problem lies somewhere else. See the manuals (tip 2)
