#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  arfedora-hdinfo.py
#  
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  require python3-dbus
import dbus
import math


def get_all_devices():
	bus = dbus.SystemBus()
	result  = []
	object_   = bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2")
	for i in object_.get_dbus_method("GetManagedObjects","org.freedesktop.DBus.ObjectManager")():
		if i.startswith("/org/freedesktop/UDisks2/block_devices/") and i[39:-1]=="sd":
			ob        = bus.get_object("org.freedesktop.UDisks2",i)
			interface = dbus.Interface(ob,"org.freedesktop.DBus.Properties")
			drive=interface.Get("org.freedesktop.UDisks2.Block","Drive")
			result.append(["/dev/{}".format(i[39:]),drive])

	return result
	

 
def get_drives_info(drives):
	bus = dbus.SystemBus()
	for drive in drives:
		try:
			object_       = bus.get_object("org.freedesktop.UDisks2",drive[1])
			propos        = dbus.Interface(object_,"org.freedesktop.DBus.Properties")
			id_           = propos.Get("org.freedesktop.UDisks2.Drive","Id")
			model         = propos.Get("org.freedesktop.UDisks2.Drive","Model")
			size          = propos.Get("org.freedesktop.UDisks2.Drive","Size") /1024 /1024
			speed         = propos.Get("org.freedesktop.UDisks2.Drive","RotationRate")
			removable     = "True" if propos.Get("org.freedesktop.UDisks2.Drive","Removable") else "False"
			connectionbus = propos.Get("org.freedesktop.UDisks2.Drive","ConnectionBus")
			if not connectionbus:
				connectionbus = "None"
			print("Drive\t\t"+drive[0]+ " :")
			print("Id\t\t"+id_)
			print("Model\t\t"+model)
			print("Size\t\t"+str(round(size,2))+"MB"+" {}GB".format(math.ceil(size/1024)))
			print("Speed\t\t"+str(speed))
			print("Removable\t"+removable)
			print("ConnectionBus\t"+connectionbus)
			print("\n\n")
		except:
			pass

if __name__ == "__main__":
	get_drives_info(get_all_devices())
