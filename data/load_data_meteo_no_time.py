import urllib.request
import requests
import datetime
import tb_rest as tb
import json as json

def list_devices(tb_url, jwtToken, types_keys, customerId):
    device_list = []
    for type in types_keys.keys():
        resp = tb.get_devices(tb_url, jwtToken, customerId, device_type=type, limit=300)
        if len(resp)>0:
            print('Loaded type \'' + type + '\' : ' + str(len(resp)))
            for device_data in resp:
                device_list.append({'id':device_data['id']['id'], 'name':device_data['name'], 'type':type, 'keys':types_keys[type]})
            
    return device_list

def load_telemetry(tb_url, jwtToken, device_list, startTs, endTs):
    for device in device_list:
        resp = tb.get_timeseries(tb_url, device['id'], jwtToken, device['keys'], startTs, endTs, limit=2678400)
        if resp.status_code == 200:
            device['data'] = resp.json()            
        else:
            print(resp)
    return device_list

def format_ts(ts):
    dt = datetime.datetime.fromtimestamp(tb.fromJsTimestamp( ts ) )
    dt = dt.replace(microsecond=0)
    return str(dt)

####### time series data in columns ######################
def print_transposed_csv(device_list, folder):
	for i,device in enumerate(device_list):
		fileName = device['type'] + '_' + device['id'] + '_' + device['name'] +'.csv'
		CSV_DELIM = ','
		for key in device['data'].keys():
			fileMeteoValueName = device['type'] + key + '.csv'
			with open(fileMeteoValueName, 'w') as file:
				headForValue = ['ts', key]
				file.write(CSV_DELIM.join(headForValue) + '\n')
				sorted_data = sorted(device['data'][key], key = lambda x: x['ts'])
				for data_entry in sorted_data:
					data_row = [str(data_entry['ts']//1000), str(data_entry['value'])]
					file.write(CSV_DELIM.join(data_row) + '\n')
                	#key_ts = [ format_ts( data_entry['ts'] ) for data_entry in sorted_data ]
                #key_val = [ str(data_entry['value']) for data_entry in sorted_data ]
                #row_ts = ['ts_' + key ] + key_ts
                #row_val = [key] + key_val   
                #file.write(CSV_DELIM.join(row_ts) + '\n')
                #file.write(CSV_DELIM.join(row_val) + '\n')
            
def print_csv(device_list, folder):
    for i,device in enumerate(device_list):
        #table = make_table(device['data'])
        fileName = device['type'] + ' ' + str(i+1) +'.csv'
        CSV_DELIM = ';'
        with open(fileName, 'w') as file:
            file.write( CSV_DELIM.join([device['id'], device['name']]) + '\n' )
            for key in device['data'].keys():
                #key_ts = [ str(data_entry['ts']) for data_entry in device['data'][key] ]
                sorted_data = sorted(device['data'][key], key = lambda x: x['ts'])
                key_ts = [ format_ts( data_entry['ts'] ) for data_entry in sorted_data ]
                key_val = [ str(data_entry['value']) for data_entry in sorted_data ]
                row_ts = ['ts_' + key ] + key_ts
                row_val = [key] + key_val   
                file.write(CSV_DELIM.join(row_ts) + '\n')
                file.write(CSV_DELIM.join(row_val) + '\n')
            #file.write('ts;'+ ';'.join( sorted(device.keys() ) ) + '\n' )    
    
if __name__ == "__main__":
    file = "tb.access"

    device_type = 'Vega Smart-UM'
    device_type_meteo = 'MPV-702'
    keys = ['anglevertical', 'charge', 'co2', 'humidity', 'illumination', 'noise', 'powerstate', 'temperature', 'timestamp', 'type']
    keys_meteo = ['ts','BaroPressure','DewPoint','Humidity','Temperature','WindDirection','WindSpeed']
    types_keys = {device_type:keys}
    #### time points of start and stop of downloading #####
    startTs = tb.toJsTimestamp(datetime.datetime(2022, 8, 1, hour = 0).timestamp())
    endTs = tb.toJsTimestamp(datetime.datetime(2022, 9, 1, hour = 0).timestamp())

#    params = tb.load_access_parameters(file)
    tb_url, tb_user, tb_password, customerId = ["http://tb.ipu.ru", "shushko.ni@phystech.edu", "12345678", ""]

    print('Loading token ...')
    bearerToken, refreshToken, resp = tb.getToken(tb_url, tb_user, tb_password)
#    devices = list_devices(tb_url, bearerToken, types_keys, customerId)[0:2]
   # for d in devices:
   #     d["keys"] = keys

    #deviceId = params["device_id"]
    devices = [{'id': 'e9827990-172e-11ed-a610-2dd4a9227126', 'keys':keys, 'type':'Vega Smart-UM', 'name':'VSm_383437315E396B0E'},
               {'id': '8f66d910-172e-11ed-a610-2dd4a9227126', 'keys':keys, 'type':'Vega Smart-UM', 'name':'VSm_3834373155398E0D'},
	       {'id': 'edaae300-172d-11ed-a610-2dd4a9227126', 'keys':keys, 'type':'Vega Smart-UM', 'name':'VSm_3834373167398A0D'},
               {'id': 'c5f6b3c0-172d-11ed-a610-2dd4a9227126', 'keys':keys, 'type':'Vega Smart-UM', 'name':'VSm_3834373175396E0E'}]
    devices_meteo = [{'id': '4dc14d40-4749-11ea-bd76-a73c738b665f', 'keys':keys_meteo, 'type':device_type_meteo, 'name':'Метеостанция 1'}]   
    print('Total: ' + str(len(devices_meteo)) + ' devices')
    print(devices_meteo)
    print('Loading telemetry ...')
    devices_m = load_telemetry(tb_url, bearerToken, devices_meteo, startTs, endTs)
    folder = '~/bazenkov'
    #jsonFile = devices[0]['name'] + '.json'
    #with open(jsonFile, 'w') as file:
    #    json.dump(devices, file)
    #with open(jsonFile, 'w') as file:
    #    file.write(str(devices))
    print_transposed_csv(devices_m, folder)
    
#4dc14d40-4749-11ea-bd76-a73c738b665f
