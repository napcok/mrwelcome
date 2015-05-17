# -*- coding: utf-8 -*-


import csv
import os
import gettext

gettext.install("mageiawelcome")

install = _("Install")
launch = _("Launch")

def get_desktop_name(x):
  return {
    '01KDE4':'KDE',
    '02GNOME':'Gnome',
    'gnome': 'Gnome',
    'LXDE':'LXDE',
    '10MATE':'Mate',
    '10Cinnamon':'Cinnamon',
    '05RazorDesktop':'RazorQt',
    '23E17':'Enlightenment',
    '07IceWM':'IceWM',
    '26Openbox':'Openbox',
    '03WindowMaker':'WindowMaker',
    '09Fvwm2':'Fvwm2',
  }.get(x,'Other')

def get_desktop_name2(x):
  return {
      'KDE':'KDE',
      'XFCE':'Xfce',
      'LXQt':'LXQt',
    }.get(x,'unknown')
  
def get_irc_client():
  if os.path.exists("/usr/bin/hexchat"): irc_client = "/usr/bin/hexchat &"
  elif os.path.exists("/usr/bin/xchat-gnome"): irc_client = "/usr/bin/xchat-gnome &"
  elif os.path.exists("/usr/bin/xchat"): irc_client = "/usr/bin/xchat &"
  elif os.path.exists("/usr/bin/konversation"): irc_client = "/usr/bin/konversation &"
  elif os.path.exists("/usr/bin/quassel"): irc_client = "/usr/bin/quassel &"
  else: irc_client = "none"
  return irc_client

def is_installed(name):
  return os.WEXITSTATUS(os.system('rpm -q --quiet ' + name))

  
def get_listapp():
  listapp = ''
  with open("apps.csv", 'rb') as f:
      mycsv = csv.reader(f,delimiter='|')
      mycsv.next()
      for r in mycsv:
	if (r[5] == 'false'):
	  start_btn = ""
	else:
	  start_btn = "<button class='cmd small green' data-run='"+ r[5] + "'><i class='icon-ok-sign'> </i>" + launch +"</button>" 
	if (r[6] != ''):
	  label = "<span class='label red'>" + r[6] + "</span>"
	else:
	  label = ""  
	if ( is_installed(r[1]) != 0):# NOT INSTALLED
	  listapp += "<li class='" + r[3] +"' id='" + r[0] + "'><img class=icon src=img/" + r[0] + ".png /><div class='chkbox'><input type='checkbox' datasrc='" + r[1] +"'></div> \
<h6>" + r[2] + "</h6><p class='description'>" + r[4] + "</p>" + label + "<button class='inst small' data-rpm='" + r[1] + "'><i class='icon-circle-arrow-down'> </i>" + install +"</button></li>"
	else: # INSTALLED
	  listapp += "<li class='urpme " + r[3] +"' id='" + r[0] + "'><img class=icon src=img/" + r[0] + ".png /><div class='chkbox'></div> \
<h6>" + r[2] + "</h6><p class='description'>" + r[4] + "</p>" + start_btn + label + "</li>"
  return listapp
 