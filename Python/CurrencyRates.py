############################################
#
# I. Import SECTION
#
############################################


import requests, configparser
import pandas as pd
from datetime import date, timedelta


############################################
#
# II. Functions
#
############################################


#defining GET-request to API

def get_exchange_rates(endpoint_url, api_key, date):
    try:
        params = {"access_key": api_key, "date": date}
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()  # Raises an exception for 4xx and 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
#defining CSV Export

def export_to_csv(data_frame, file_name, output_dir):
    try:
        file_path = f"{output_dir}/{file_name}"
        data_frame.to_csv(file_path,mode='a', sep=';', index=False)
        #print(f"Data exported to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred while exporting to CSV: {e}")

#defining date-range

def get_diff_days():
    try:    
        
        Cdate = date(date.today().year, date.today().month, date.today().day)
        #PDate = date(date.today().year-1, 1,1)
        PDate = date(date.today().year, date.today().month, date.today().day-4)

        delta = Cdate-PDate
        return(delta.days)
    except Exception as e:
        print(f"An error occurred while generating timeframe: {e}")
        return None

# defining INI-read

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    if 'settings' in config:
        settings = config['settings']
        output_dir = settings.get('output_dir', '')
        url = settings.get('url', '')
        api_key = settings.get('api_key', '')
        file_nam = settings.get('file_nam', '')
        
        return output_dir, url, api_key, file_nam
    else:
        raise ValueError('No [settings] section found in the config file.')



############################################
#
# III. MAIN SECTION
#
############################################


# Code can be exectuted in interpreter only

if __name__ == "__main__":

    # Path to config file - single hardcoded information in script

    config_file = "C:\Python\Scripts\CurrencyRates\config.ini"

    # load param values loaded from ini-file - correct order dependant of output statement

    output_dir, url, api_key, file_nam = load_config(config_file)

    delta = get_diff_days()
    #print(x)


    #empty csv file
    try:
        filename = output_dir+file_nam
        f = open(filename, "w+")
        f.close
    except Exception as e:
        print(f"An error occurred while clearing CSV File: {filename} {e}")

    # defining today´s date as first day of which currency rate is loaded
    ExtractDate =date.today()
    

    for i in range(delta):

        endpoint_url = url + ExtractDate.strftime("%Y-%m-%d")

        #GET currency data from API
        exchange_rates_data = get_exchange_rates(endpoint_url, api_key, ExtractDate.strftime("%Y-%m-%d"))  
     
        if exchange_rates_data:
            # Print the entire JSON response
            #print("Exchange Rates Data (JSON Format):")
            #print(exchange_rates_data)
            
            # Extract currency rates data
            rates_data = exchange_rates_data.get("rates")
            if rates_data:
                # Convert the rates data to a DataFrame
                data_frame = pd.DataFrame(rates_data.items(), columns=["Currency", "Currency Rate"])
                               
                # Add additional columns for "Date", "Base Currency", "Historical", and "Type"
                data_frame["Date"] = ExtractDate.strftime("%Y-%m-%d")
                data_frame["Base Currency"] = exchange_rates_data.get("base")
                data_frame["Historical"] = True
                data_frame["Type"] = "historical"
                
                # Reorder the DataFrame columns to match the desired table format
                data_frame = data_frame[["Date", "Type", "Base Currency", "Currency", "Currency Rate"]]

                if i == 0:
                    full_df = data_frame
                else:           
                    full_df = pd.concat([full_df, data_frame], ignore_index=True)

                ExtractDate = (ExtractDate - timedelta(days = 1))
        
        else:
            print("No data received.")

    # Export the JSON response to a CSV file
                
    export_to_csv(full_df, file_nam, output_dir)  
    print(f"Data for {i+1}-days exported to {filename}")