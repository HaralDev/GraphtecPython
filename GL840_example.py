from bs4 import BeautifulSoup
from requests import get
from pandas import DataFrame
from pyvisa import ResourceManager

from time import sleep

class Graphtec:

    #-----------------------------------
    def __init__(self, address, resource_manager):
        self.address = address
        self.tcpip_gl = f"TCPIP::{self.address}::8023::SOCKET"                          # TCPIP adress to contact
        self.instrument = resource_manager.open_resource(self.tcpip_gl, 
                                                            write_termination='\n', 
                                                            read_termination='\r\n')
        self.query_id = self.get_graphtec_idn()
        self.data = []                                                                  # Holds measurement data

    #-----------------------------------
    def append_graphtec_readings(self):
        """Find all the measurements of the channels and append to self.data list"""
        # Format URL
        address_channel_data = f"http://{self.address}/digital.cgi?chgrp=13"

        # Get http response
        response = get(address_channel_data)                        # Get response from the channel data page

        # Create response table
        soup_object = BeautifulSoup(response.text, 'html.parser')   # Create a soup object from this, which is used to create a table 
        table = soup_object.find(lambda tag: tag.name=='table')     # Table with all the channels as subtables > based on the HTML table class > example: [table: [table, table, table]]
        channel_readings_html = table.findAll('table')              # Tables of all the individual channels > Search for table again to get: [table, table, table], each one corresponds to one channel

        # Loop over table to yield formatted data
        channels_data = []                                          # Holds all the found data > in format: [('CH 1', '+  10', 'degC'), (CH2 ....]

        for channel_read_html in channel_readings_html:
            reading_html = channel_read_html.find_all('b')          # Returns a row for each measurement channel with relevant data > [<b> CH 1</b>, <b> -------</b>, <b> degC</b>]

            reading_list = [read_tag.get_text(strip=True) for read_tag in reading_html] # Strips the string of its unicode characters and puts it into a list > ['CH 1', '-------', 'degC']
            channels_data.append(reading_list)

        # Append the data to the list
        self.data.append(channels_data)

    #-----------------------------------
    def get_graphtec_idn(self):
        """SCPI command to get IDN"""
        idn = self.instrument.query("*IDN?")
        return idn

    #-----------------------------------
    def add_channel_data_to_df(self):
        """Post processing method to format self.data list into a Pandas DataFrame"""

        name_index = 0      # Format is ['CH 1', '23.56', 'degC']
        reading_index = 1   # so index 0, 1 and 2 are, respectively channel name, value reading and unit.
        unit_index = 2      

        channel_count = len(self.data[0])    # Amount of channels to loop over, might depend on Graphtec device (I have 20)
        df = DataFrame()

        # Loop over each channel
        for channel_ind in range(channel_count):

            channel_name = self.data[0][channel_ind][name_index]    # get the channel name
            channel_unit = self.data[0][channel_ind][unit_index]    # and unit
            column_name = f"GRPH {channel_name} [{channel_unit}]"   # Format column name "GRPH CH1 [degC]"

            channel_readings = []                                   # Stores the channel data > [0.0, 0.1, 0.0 ....]
            
            # Loop over each row and retrieve channel data
            for row in self.data:
                channel_reading = row[channel_ind][reading_index]   # Read the data of channel for this row
                
                # Value formatting
                if channel_reading == '-------' or channel_reading == '+++++++':
                    channel_reading = "NaN"                                 # NaN for false values
                else:
                    channel_reading = float(channel_reading.replace(' ',''))# Float for other values, remove spaces in order to have +/-   

                channel_readings.append(channel_reading)            
                
            df[column_name] = channel_readings          # Add a new column with data

        return df


if __name__ == "__main__":
        
    rm = ResourceManager() # Need a resourcemanager to communicate with Graphtec via PyVisa

    ip_graphtec = "169.254.26.184"      # Can be setup on Graphtec with "Menu > I/F > IP ADDRESS" (change with buttons)
    graphtec = Graphtec(ip_graphtec, rm)# Sometimes errors arise here if you can not connect, restarting the Graphtec or doing "Menu > I/F > Apply Setting" Sometimes helps. Also, try if you can visit the ip address in browser directly.


    for i in range(10):
        graphtec.append_graphtec_readings() # Measure and append to data list
        sleep(0.2)                          # Reading every 0.2 seconds

    df = graphtec.add_channel_data_to_df()  # Add everything to one easily accesible dataframe
    rm.close()                              # Not closing gives annoying error
    print(df)
        
