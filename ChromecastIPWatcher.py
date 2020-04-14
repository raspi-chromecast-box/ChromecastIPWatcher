#!/usr/bin/env python3
import os
import sys
import time
import pychromecast
import json
from uuid import UUID
from pathlib import Path
import redis
import schedule

class ComplexEncoder( json.JSONEncoder ):
	def default( self , obj ):
		if isinstance( obj , UUID ):
			return str( obj )
		return json.JSONEncoder.default( self , obj )

def try_to_connect_to_redis():
	try:
		redis_connection = redis.StrictRedis(
			host="127.0.0.1" ,
			port="6379" ,
			db=1 ,
			#password=ConfigDataBase.self[ 'redis' ][ 'password' ]
			)
		return redis_connection
	except Exception as e:
		return False

def try_to_get_chromecasts():
	try:
		print( "Trying to Find Local Google-Cast Devices" )
		redis_connection = try_to_connect_to_redis()
		if redis_connection is False:
			raise RuntimeError( "Couldn't Connect to Redis" ) from error
		chromecast_output_uuid = redis_connection.get( "CONFIG.CHROMECAST_OUTPUT.UUID" )
		chromecast_output_uuid = str( chromecast_output_uuid , 'utf-8' )
		chromecasts = pychromecast.get_chromecasts()
		results = []
		for _cast in chromecasts:
			cast_object = {}
			info = vars( _cast )
			cast_object[ 'ip' ] = info[ 'host' ]
			cast_object[ 'port' ] = info[ 'port' ]
			device_info = json.dumps( info[ 'device' ] , cls=ComplexEncoder )
			if device_info.startswith( '[' ) and device_info.endswith( ']' ):
				device_info = device_info[ 1 : -1 ]
				device_info = device_info.split( '"' )[ 1 :: 2 ]
				cast_object[ 'friendly_name' ] = device_info[ 0 ]
				cast_object[ 'model_name' ] = device_info[ 1 ]
				cast_object[ 'manufacturer' ] = device_info[ 2 ]
				cast_object[ 'uuid' ] = device_info[ 3 ]
				cast_object[ 'cast_type' ] = device_info[ 4 ]
				#cast_object[ 'location' ] = ConfigDataBase.self[ 'location' ]
				results.append( cast_object )
				key = "UUIDS." + cast_object[ 'uuid' ]
				redis_connection.set( key , json.dumps( cast_object ) )
				print( f"{cast_object[ 'uuid' ]} == {chromecast_output_uuid}" )
				if cast_object[ 'uuid' ] == chromecast_output_uuid:
					print( "setting STATE.CHROMECAST_OUTPUT.IP" )
					redis_connection.set( "STATE.CHROMECAST_OUTPUT.IP" , cast_object[ 'ip' ] )
		print( results )
		return results
	except Exception as e:
		print( 'Error Finding Chromecasts' )
		print( e )
		return False


def try_run_block( options ):
	for i in range( options[ 'number_of_tries' ] ):
		attempt = options[ 'function_reference' ]()
		if attempt is not False:
			return attempt
		print( f"Couldn't Run '{ options[ 'task_name' ] }', Sleeping for { str( options[ 'sleep_inbetween_seconds' ] ) } Seconds" )
		time.sleep( options[ 'sleep_inbetween_seconds' ] )
	if options[ 'reboot_on_failure' ] == True:
		os.system( "reboot -f" )

def run_block():
	try_run_block({
			"task_name": "Find Chromecast Task" ,
			"number_of_tries": 5 ,
			"sleep_inbetween_seconds": 5 ,
			"function_reference": try_to_get_chromecasts ,
			"reboot_on_failure": True
		})

run_block()
schedule.every( 5 ).minutes.do( run_block )
while True:
	schedule.run_pending()
	time.sleep( 1 )