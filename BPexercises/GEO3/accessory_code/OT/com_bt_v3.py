#!/usr/bin/python

try:
	import os, sys
except ImportError:
	print("Os and Sys libraries are required.")

try:
	import bluepy.btle
except ImportError:
	print("BluePy library is required.")
	
try:
	import time
except ImportError:
	print("time library is required.")

import numpy as np

class demoDelegate(bluepy.btle.DefaultDelegate):
	def __init__(self):
		bluepy.btle.DefaultDelegate.__init__(self)
		# ... initialise here

	def handleNotification(self, cHandle, data):
		# ... perhaps check cHandle
		# ... process 'data'
		print("Notification received")
		print(cHandle)
		print(data)

class blueToothDemo(object):

	def __init__(self,num_rows=12,num_cols=16):
		self.N_ROWS = num_rows
		self.N_COLUMNS = num_cols
		self.BY_ARRAY = [0 for i in range(2*self.N_ROWS)]
		
		self.ADDR_NULL = "00:00:00:00:00:00"
		self.ADDR_DEMO1 = "88:6b:0f:2f:65:67"
		self.ADDR_DEMO2 = "88:6b:0f:2f:66:96"
		self.ADDR_DEMO3 = "88:6b:0f:2f:64:8c"
		self.ADDR_DEMO4 = "88:6b:0f:5f:49:50"
		self.ADDR_DEMO5 = "88:6b:0f:5f:49:53"
		self.ADDR_DEMO6 = "88:6b:0f:5f:49:54"
		self.ADDR_DEMO7 = "88:6b:0f:5f:49:52"
		self.ADDR_DEMO8 = "88:6b:0f:5f:49:51"
		
		self.handleL = 10
		self.handleR = 14
		
		self.DELAY_HALF_MAT = 0.1
		self.SCAN_TIMEOUT = 3.0
		self.SCAN_NUM = 10
	
		#Scan for devices 
		self.scanner = bluepy.btle.Scanner()
		self.find_bluetooth_demo()
		if (self.addr_demo == self.ADDR_NULL):
			print("No demos found")
			sys.exit()
		
		#Try to connect to first device found 
		self.isConnected = False
		for i in range(0,self.SCAN_NUM):
			#print(i)
			try:
				self.demo = bluepy.btle.Peripheral(self.addr_demo)
				self.demo.setDelegate( demoDelegate() )
				self.isConnected = True
				print("connected")
				
				print('getting Services()...', end='', flush=True)
				self.Services = self.demo.getServices()
				print ("%s services found" % (len(self.Services)))
		
				print('getting Characteristics()...', end='', flush=True)
				self.Charact = self.demo.getCharacteristics()
				print ("%s characteristics found" % (len(self.Charact)))
				
				#print('getting Descriptors()...', end='', flush=True)
				#self.Descriptors = self.demo.getDescriptors()
				#print ("%s descriptors found" % (len(self.Descriptors)))
				
				break
			except bluepy.btle.BTLEException:
				print("Could not connect, #%d of %d" % (i+1,self.SCAN_NUM))
		
		
		if (self.isConnected == False):
			print("Could not connect, exit")
			sys.exit()
		return	


	def find_bluetooth_demo(self):
		devices = self.scanner.scan(self.SCAN_TIMEOUT)
		self.addr_demo = self.ADDR_NULL
		for dev in devices:
			#print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
			if dev.addr == self.ADDR_DEMO1:
				print ("Found demo 1")
				self.addr_demo = self.ADDR_DEMO1
			if dev.addr == self.ADDR_DEMO2:
				print ("Found demo 2")
				self.addr_demo = self.ADDR_DEMO2
			if dev.addr == self.ADDR_DEMO3:
				print ("Found demo 3")
				self.addr_demo = self.ADDR_DEMO3
			if dev.addr == self.ADDR_DEMO4:
				print ("Found demo 4")
				self.addr_demo = self.ADDR_DEMO4
			if dev.addr == self.ADDR_DEMO5:
				print ("Found demo 5")
				self.addr_demo = self.ADDR_DEMO5
			if dev.addr == self.ADDR_DEMO6:
				print ("Found demo 6")
				self.addr_demo = self.ADDR_DEMO6
			if dev.addr == self.ADDR_DEMO7:
				print ("Found demo 7")
				self.addr_demo = self.ADDR_DEMO7
			if dev.addr == self.ADDR_DEMO8:
				print ("Found demo 8")
				self.addr_demo = self.ADDR_DEMO8				
		return
	
	def print_TwoVec(self, matL, matR):
		try:
			self.demo.writeCharacteristic(self.handleL,matL, withResponse=True)
			time.sleep(self.DELAY_HALF_MAT)
			self.demo.writeCharacteristic(self.handleR,matR, withResponse=True)
			time.sleep(self.DELAY_HALF_MAT)
			return True
		except bluepy.btle.BTLEException.DISCONNECTED:
			print("Device disconnected")
			return False
	
	def to_byte_arr(self, grid):
		for i in range(1,self.N_ROWS+1):
			arr1 = grid[i][8:0:-1]
			arr2 = grid[i][16:8:-1]
			self.BY_ARRAY[i-1] = int(''.join(str(x) for x in arr1),2)
			self.BY_ARRAY[i-1+self.N_ROWS] = int(''.join(str(x) for x in arr2),2)
		return self.BY_ARRAY
	
	def print_Grid(self,grid):
		arrL = bytes(self.to_byte_arr(grid)[:12])
		arrR = bytes(self.to_byte_arr(grid)[12:])
		#print(arrL)
		#print(arrR)
		return self.print_TwoVec(arrL,arrR) 
		
	def close(self):
		self.demo.disconnect()

	def send_cmd(self, msg):
		mymap =(self.convert_lines_to_map(msg))
		self.print_Grid(mymap)

	def convert_lines_to_map(self, msg):
		mymap = np.zeros((13, 17))
		#msg = "line(0,11,0,10,1,*L01);line(1,11,1,4,1,*L02);line(2,11,2,6,1,*L03);"
		cmd_list = msg.split(';')
		for c in range(len(cmd_list) - 1):

			strcmd = cmd_list[c][5:]
			arr_values = strcmd.split(",")
			for v in range(5):
				arr_values[v] = int(arr_values[v])

			positions = arr_values[0:4]
			value = arr_values[4]

			if positions[0] == positions[2]:
				# vertical
				if positions[1] > positions[3]:
					for r in range(positions[3], positions[1]+1, 1):
						mymap[r + 1][positions[0] + 1] = value
				else:
					for r in range(positions[1], positions[3]+1, 1):
						mymap[r + 1][positions[0] + 1] = value

			elif positions[1] == positions[3]:
				# horizontal
				if positions[0] > positions[2]:
					for c in range(positions[2], positions[0]+1, 1):
						mymap[positions[1]][c + 1] = value
				else:
					for r in range(positions[1], positions[3]+1, 1):
						mymap[positions[1]][c + 1] = value

			elif positions[1] == positions[3] and positions[0] == positions[2]:
				# point
				mymap[positions[1] + 1][positions[1] + 1] = value

		return mymap


