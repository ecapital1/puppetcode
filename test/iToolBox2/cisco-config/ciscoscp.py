#!/usr/bin/python

import sys, os

print "\nPlease Choice which cisco device to get startup and running config from: \n\n"
print "\t(1) Epcau-router-cisco1"
print "\t(2) Epcau-sw-cisco1"
print "\t(3) Epcau-sw-cisco2"
print "\t(4) Epcau-sw-cisco3"
print "\t(5) Epcau-sw-cisco4"
print "\t(6) Epcau-sw-cisco5"
print "\t(7) Epcau-sw-cisco6"
print "\t(8) alc-router-cisco1"
print "\t(9) alc-router-cisco2"
print "\t(10) alc-router-cisco3"
print "\t(11) alc-sw-cisco1"
print "\t(12) alc-sw-cisco2"
print "\t(13) alc-sw-cisco3"
print "\t(14) alc-sw-cisco4"
print "\t(15) alc-sw-cisco5"
print "\t(16) alc-sw-arista1"
print "\t(17) alc-sw-arista2"
print "\t(18) alc-sw-arista3"
print "\t(19) Epcuk-router-cisco1"
print "\t(20) Epcuk-router-cisco2"
print "\t(21) Epsyd-router-cisco1"
print "\t(22) Epsyd-sw-cisco1"
print "\t(23) Epsyd-sw-cisco2"
print "\t(24) Epsyd-sw-cisco3"
print "\t(25) Epsgx-sw-cisco1"
print "\t(26) Epsgx-sw-cisco2"
print "\t(27) Epsgx-router-cisco1"
print "\t(28) Epsgx-router-cisco2"
print "\t(29) Epsgx-router-cisco2"
print "\t(30) Epoch_UC"

choice = sys.stdin.readline().strip()

if choice == "1":
	router = "epcau-router-cisco1"

elif choice == "2":
	router = "epcau-sw-cisco1"

elif choice == "3":
        router = "epcau-sw-cisco2"

elif choice == "4":
        router = "epcau-sw-cisco3"

elif choice == "5":
        router = "epcau-sw-cisco4"

elif choice == "6":
        router = "epcau-sw-cisco5"

elif choice == "7":
        router = "epcau-sw-cisco6"

elif choice == "8":
        router = "alc-router-cisco1"

elif choice == "9":
        router = "alc-router-cisco2"

elif choice == "10":
        router = "alc-router-cisco3"

elif choice == "11":
        router = "alc-sw-cisco1"

elif choice == "12":
        router = "alc-sw-cisco2"

elif choice == "13":
        router = "alc-sw-cisco3"

elif choice == "14":
        router = "alc-sw-cisco4"

elif choice == "15":
        router = "alc-sw-cisco5"

elif choice == "16":
        router = "alc-sw-arista1"

elif choice == "17":
        router = "alc-sw-arista2"

elif choice == "18":
        router = "alc-sw-arista3"

elif choice == "19":
        router = "epcuk-router-cisco1"

elif choice == "20":
        router = "epcuk-router-cisco2"

elif choice == "21":
	router = "epsyd-router-cisco1"

elif choice == "22":
        router = "epsyd-sw-cisco1"

elif choice == "23":
        router = "epsyd-sw-cisco2"

elif choice == "24":
        router = "epsyd-sw-cisco3"

elif choice == "25":
        router = "epsgx-sw-cisco1"

elif choice == "26":
        router = "epsgx-sw-cisco2"

elif choice == "27":
        router = "epsgx-router-cisco1"

elif choice == "28":
        router = "epsgx-router-cisco2"

elif choice == "29":
        router = "Epsgx-router-cisco1"

elif choice == "30":
        router = "10.10.10.206"

else:
	print "You Didnt Enter a valid Number"
	exit(0)

os.popen ('scp scp@' + router + ':running-config ./' + router + '-running')
os.popen ('scp scp@' + router + ':startup-config ./' + router + '-startup')

