# -*- coding: utf-8 -*-

import signal
import os
import time
import urllib
import commands
import subprocess
import shlex
import gettext
import string
import gtk

from user import home

from simplejson import dumps as to_json
from simplejson import loads as from_json

from webgui import start_gtk_thread
from webgui import launch_browser
from webgui import synchronous_gtk_message
from webgui import asynchronous_gtk_message
from webgui import kill_gtk_thread

from helpers import *

# i18n
gettext.install("mrwelcome")

class Global(object):
    quit = False
    @classmethod
    def set_quit(cls, *args, **kwargs):
        cls.quit = True



def main():
    start_gtk_thread()
    # Changing working directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    #collect sys info
    #release = open("/etc/release", "r").read()
    release = commands.getoutput('lsb_release -sd')
    release = release[1:-1]
    kernel = commands.getoutput('uname -r')
    if os.uname()[4] == 'x86_64':
      arch = '64-bit'
    else:
      arch = '32-bit'
    home = os.getenv("HOME")
    username = os.getenv("USER")
    desktop = get_desktop_name(os.getenv("DESKTOP_SESSION"))
    
    if desktop == 'Other':
      desktop = get_desktop_name2(os.getenv("XDG_CURRENT_DESKTOP"))
    
   
    #collect packages nad its status
    listapp = get_listapp()
    
    #TODO check if non-free and tainted enabled
    restricted_repos = "disabled"
    
   
    l={}
    l['name'] = _("Welcome to Mageia!")
    l['show'] = _("Show this window at startup")
    l['close'] = _("Close")
   
    l['release'] = release
    l['kernel_l'] = _("kernel:") 
    l['kernel'] = kernel
    l['arch_l'] = _("arch:")
    l['arch'] = arch
    l['desktop_l'] = _("Desktop:")
    l['desktop'] = desktop
    l['welcome_btn'] = _("Welcome")
    l['welcome'] = _("Welcome<!--user//-->")
    l['user'] = username
    l['welcome_msg'] = _("<p>Thank you for choosing Mageia!</p><p>We have put in a lot of effort to provide you with the best possible system. We hope you will have a good experience with Mageia. If you feel that our project is a good idea, we would also appreciate any contribution you can make to it for next versions.</p><p>To find out how you can help <a class='weblink' href='http://www.mageia.org/en/contribute/'>click here</a>.</p><p>Don't forget to tell your friends about Mageia.</p>")
    l['mcc'] = _("Mageia Control Center")
    l['conf_update'] = _("Configure media sources and update system")
    l['inst_remove'] = _("Install and remove software")
    l['h_documentation'] = _("Documentation")
    l['features'] = _("New Features")
    l['relnotes'] = _("Release Notes")
    l['errata'] = _("Errata")
    l['newcomers'] = _("Newcomers Howto")
    l['h_support'] = _("Support")
    l['forum'] = _("Forums")
    l['wiki'] = _("Wiki")
    l['chat'] = _("Chat Room")
    l['bugs'] = _("Bugzilla")
    l['h_community'] = _("Community")
    l['comm_center'] = _("Community Center")
    l['contribute'] = _("Contribute")
    l['donate'] = _("Donations")
    l['joinus'] = _("Join us!")
    l['mccdesc'] = _("Mageia Control Center (aka drakconf) is a set of tools to help you configure your system")
    l['SM'] = _("Software Management")
    l['Oa'] = _("Online administration")
    l['H'] = _("Hardware")
    l['NI'] = _("Network & Internet")
    l['S'] = _("System")
    l['NS'] = _("Network Sharing")
    l['LD'] = _("Local Disks")
    l['Sec'] = _("Security")
    l['B'] = _("Boot")
    l['adminpass'] = _("Administrator password is needed")
    l['userpass'] = _("User password is needed")
    l['conf_media'] = _("Configure media sources ...")
    l['mag_media'] = _("Mageia official repositories contain:")
    l['core'] = _("<span class='label green'>core</span> - the free-open-source packages, i.e. software licensed under a free-open-source license")
    l['nonfree'] = _("<span class='label red'>non-free</span> - some programs which are not free, or closed source. For example this repository includes Nvidia and ATI graphics card proprietary drivers, firmware for various WiFi cards, etc")
    l['tainted'] = _("<span class='label red'>tainted</span> - includes packages released under a free license. However, they may infringe on patents and copyright laws in some countries, e.g. multimedia codecs needed to play various audio/video files; packages needed to play commercial video DVD, etc. ")
    l['note'] = _("<strong>Note!</strong> non-free and tainted are not enabled by default.")
    l['editss'] = _("Edit software sources")
    l['updsys'] = _("... and update system")
    l['chkupd'] = _("Check system updates")
    l['guirpmdrake'] = _("GUI - RPMDrake")
    l['rpmdrake_desc'] = _("<span class='label green'>Rpmdrake</span> is a program for installing, uninstalling and updating packages. It is the graphical user interface of <span class='label green'>urpmi</span>")
    l['readmore'] = _("read more (wiki)")
    l['r_rpmdrake'] = _("RPMdrake")
    l['urpmi'] = _("URPMI - from command line")
    l['r_term'] = _("Terminal")
    l['small_selection'] = _("This is just small selection of popular packages, for more run")
    l['featured'] = _("Featured")
    l['games'] = _("Games")
    l['internet'] = _("Internet")
    l['video'] = _("Video")
    l['audio'] = _("Audio")
    l['office'] = _("Office")
    l['graphics'] = _("Graphics")
    l['system'] = _("System")
    l['programming'] = _("Programming")
    l['selected'] = _("Selected packages:")
    l['inst_sel'] = _("Install selected")
    l['youcan'] = _("You can always launch MageiaWelcome from menu")    
    
    l['rpm_install'] = _("Applications") 
    l['applist'] = listapp
    l['bodyclass'] = restricted_repos
    l['besure_repos'] = _("Be sure you have enabled <a>online repositories</a>")
    
    
    if os.path.exists(home + "/.mrwelcome/norun.flag"):
            l['checked'] = ("")
    else:
            l['checked'] = ("CHECKED")
   
    
    l['home'] = home
    
    
    l['about'] = _("About")
    
    # Translations
   
    file = os.path.abspath('index.html')
    template = open(file).read()
    html = string.Template(template).safe_substitute(l)
    
    browser, web_recv, web_send = \
        synchronous_gtk_message(launch_browser)(html, quit_function=Global.set_quit)

    # Finally, here is our personalized main loop
  
    while not Global.quit:
     
        again = False
        msg = web_recv()
        if msg:
            msg = from_json(msg)
            again = True
            if msg == "close":
	      my_quit_wrapper()
	    elif msg == "checkbox checked":
	      if os.path.exists(home + "/.mrwelcome/norun.flag"):
		  os.system("rm -rf " + home + "/.mrwelcome/norun.flag")
	    elif msg == "checkbox unchecked":
	      os.system("mkdir -p " + home + "/.mrwelcome")
	      os.system("touch " + home + "/.mrwelcome/norun.flag")
	    elif msg.startswith("http"):
	      os.system("xdg-open " + msg)
	    elif msg == "irc":
	      irc_client = get_irc_client()
	      if irc_client == "none":
		if desktop == "KDE":
		  subprocess.Popen("gurpmi konversation", shell=True)
		else:
		  subprocess.Popen("gurpmi hexchat", shell=True)
	      else: os.system(irc_client)
	    elif msg.startswith("run"):
	      args = shlex.split(msg)
	      args.pop(0)
	      print args
	      if args[0] == "xvt":
		os.chdir(home)
	      subprocess.Popen(args)
	    
	    elif msg.startswith("gurpmi"):
		print msg
		args = shlex.split(msg)
		cat = args.pop(1)
		print args
		proc = subprocess.Popen(args, stdout=subprocess.PIPE)
		proc.wait()
		print proc.returncode
		if (proc.returncode == 0):
		  listapp = get_listapp()
		  web_send('$("ul#lista_applikacji").html("'+listapp+'");$("li#'+cat+'").trigger("click");')
		else: pass
	    elif msg.startswith("install_selected"):
		print msg
		msg2 = msg.replace('install_selected','gurpmi')
		args = shlex.split(msg2)
		cat = args.pop(1)
		print args
		proc = subprocess.Popen(args, stdout=subprocess.PIPE)
		proc.wait()
		print proc.returncode
		if (proc.returncode == 0):
		  listapp = get_listapp()
		  web_send('$("ul#lista_applikacji").html("'+listapp+'");$("li#'+cat+'").trigger("click");')
		else: pass
        if again: pass
        else:     time.sleep(0.1)


def my_quit_wrapper(fun):
    signal.signal(signal.SIGINT, Global.set_quit)
    def fun2(*args, **kwargs):
        try:
            x = fun(*args, **kwargs) # equivalent to "apply"
        finally:
            kill_gtk_thread()
            Global.set_quit()
        return x
    return fun2


if __name__ == '__main__': # <-- this line is optional
    my_quit_wrapper(main)()
