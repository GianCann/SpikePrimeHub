import 	ubluetooth 
#	import BLE, UUID, FLAG_NOTIFY, FLAG_READ, FLAG_WRITE
import	micropython
#	import const
import 	utime
import struct 

_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)
_IRQ_GATTS_WRITE                     = const(1 << 2)
_IRQ_GATTS_READ_REQUEST              = const(1 << 3)
_IRQ_SCAN_RESULT                     = const(1 << 4)
_IRQ_SCAN_COMPLETE                   = const(1 << 5)
_IRQ_PERIPHERAL_CONNECT              = const(1 << 6)
_IRQ_PERIPHERAL_DISCONNECT           = const(1 << 7)
_IRQ_GATTC_SERVICE_RESULT            = const(1 << 8)
_IRQ_GATTC_CHARACTERISTIC_RESULT     = const(1 << 9)
_IRQ_GATTC_DESCRIPTOR_RESULT         = const(1 << 10)
_IRQ_GATTC_READ_RESULT               = const(1 << 11)
_IRQ_GATTC_WRITE_STATUS              = const(1 << 12)
_IRQ_GATTC_NOTIFY                    = const(1 << 13)
_IRQ_GATTC_INDICATE                  = const(1 << 14)
send_hs = 0
state_c = 0
_COMMAND_1                           = const(1 << 0)
_COMMAND_2                           = const(1 << 1)
_COMMAND_3                           = const(1 << 2)
_COMMAND_4                           = const(1 << 3)
_COMMAND_5                           = const(1 << 4)
_COMMAND_6                           = const(1 << 5)
_COMMAND_7                           = const(1 << 6)

def adv_decode(adv_type, data):
    i = 0
    while i + 1 < len(data):
        if data[i + 1] == adv_type:
            return data[i + 2:i + data[i] + 1]
        i += 1 + data[i]
    return None

def adv_decode_name(data):
    n = adv_decode(0x09, data)
    if n:
        return n.decode('utf-8')
    return data

def bt_irq(event, data):
  global state_c    
  global send_hs    
  if event == _IRQ_SCAN_RESULT:
    print('event == _IRQ_SCAN_RESULT')    
    print('scan --> addr_type, addr, connectable, rssi, adv_data = data')
    # A single scan result.
    addr_type, addr, connectable, rssi, adv_data = data
    print(addr_type, addr, adv_decode_name(adv_data))
  elif event == _IRQ_SCAN_COMPLETE:
    print('event == _IRQ_SCAN_RESULT')    
    # Scan duration finished or manually stopped.
    print('scan complete')
    
  elif event == _IRQ_PERIPHERAL_CONNECT:
    print('event == _IRQ_PERIPHERAL_CONNECT')    
    # A successful gap_connect().
    conn_handle, addr_type, addr = data
    print(conn_handle, addr_type,addr)
    #bt.gattc_discover_services(conn_handle)
    
    ar  =struct.pack('<BBBBBBBBBB', 0x0A,0x0,0x41,0x00,0x00,0x01,0x00,0x00,0x00,0x01)
    bt.gattc_write(conn_handle,0x0B,ar,1)
    utime.sleep(2)
    print('aaaaaa complete..0x0B write 0x0A,0x0,0x41,0x00,0x00,0x01,0x00,0x00,0x00,0x01')
    
    al  =struct.pack('<BBBBBBBBBB', 0x0A,0x0,0x41,0x01,0x00,0x01,0x00,0x00,0x00,0x01)   
    bt.gattc_write(conn_handle,0x0B,al,1)
    utime.sleep(2)
    print('aaaaaa complete..0x0B  write 0x0A,0x0,0x41,0x01,0x00,0x01,0x00,0x00,0x00,0x01')
    
    bt.gattc_write(conn_handle,0x0C,struct.pack('<BB',0x01,0x00),1)
    print('connect complete.activate notifications.write Handel 0x0c data  0100... starting write')
    utime.sleep(2)
    
  elif event == _IRQ_PERIPHERAL_DISCONNECT:
    print('event == _IRQ_PERIPHERAL_DISCONNECT')    
    # Connected peripheral has disconnected.
    conn_handle, addr_type, addr = data
  elif event == _IRQ_GATTC_SERVICE_RESULT:
    print('event == _IRQ_GATTC_SERVICE_RESULT')    
    # Called for each service found by gattc_discover_services().
    conn_handle, start_handle, end_handle, uuid = data
    print(conn_handle, start_handle, end_handle, uuid) 
    print(str(end_handle) + ' check_end_handle')
    #bt.gattc_discover_characteristics(conn_handle, start_handle, end_handle)
    #bt.gattc_discover_descriptors(conn_handle,start_handle,end_handle)
    print('discover service...')
  elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
    print('event == IRQ_GATTC_CHARACTERISTIC_RESULT')        
    # Called for each characteristic found by gattc_discover_services().
    conn_handle, def_handle, value_handle, properties, uuid = data
    print(conn_handle, def_handle, value_handle, properties, uuid)
    print('discover char ...')
  elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
    print('event == _IRQ_GATTC_DESCRIPTOR_RESULT')
    # Called for each descriptor found by gattc_discover_descriptors().
    conn_handle, dsc_handle, uuid = data
    print(conn_handle, dsc_handle, uuid)
    print('discover descript  ...')
  elif event == _IRQ_GATTC_READ_RESULT:
    print('event == _IRQ_GATTC_READ_RESULT')    
    # A gattc_read() has completed.
    conn_handle, value_handle, char_data = data
  elif event == _IRQ_GATTC_WRITE_STATUS:
    print('event == _IRQ_GATTC_WRITE_STATUS')
    # A gattc_write() has completed.
    print (str(send_hs))
    send_hs = 0
    conn_handle, value_handle, status = data
  elif event == _IRQ_GATTC_NOTIFY:
    print('event == _IRQ_GATTC_NOTIFY')
    # A peripheral has sent a notify request.
    conn_handle, value_handle, notify_data = data
    #print(value_handle)
    print(notify_data)
  elif event == _IRQ_GATTC_INDICATE:
    print('event == _IRQ_GATTC_INDICATE')    
    # A peripheral has sent an indicate request.
    conn_handle, value_handle, notify_data = data

# Scan for 10s (at 100% duty cycle)

bt = ubluetooth.BLE()
bt.active(True)
bt.irq(handler=bt_irq)

# Scan for 10s (at 100% duty cycle)
#bt.gap_scan(10000, 30000, 30000)

#Connect to specific BLE Adress
#bt.gap_connect(0,b'\xa4\x34\xf1\x9b\x07\x9e',2000)
