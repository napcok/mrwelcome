import time
import Queue
import thread
import urllib

import gtk
import gobject

try:
    import webkit
    have_webkit = True
except:
    have_webkit = False

class UseWebKit: pass



use = UseWebKit 

class WebKitMethods(object):

    @staticmethod
    def create_browser():
        return webkit.WebView()

    @staticmethod
    def inject_javascript(browser, script):
        browser.execute_script(script)

    @staticmethod
    def connect_title_changed(browser, callback):
        def callback_wrapper(widget, frame, title): callback(title)
        browser.connect('title-changed', callback_wrapper)

    @staticmethod
    def open_uri(browser, html):
        browser.load_html_string(html, 'file:///usr/share/mrwelcome/')


if use is UseWebKit:
    implementation = WebKitMethods


def asynchronous_gtk_message(fun):

    def worker((function, args, kwargs)):
        apply(function, args, kwargs)

    def fun2(*args, **kwargs):
        gobject.idle_add(worker, (fun, args, kwargs))

    return fun2


def synchronous_gtk_message(fun):

    class NoResult: pass

    def worker((R, function, args, kwargs)):
        R.result = apply(function, args, kwargs)

    def fun2(*args, **kwargs):
        class R: result = NoResult
        gobject.idle_add(worker, (R, fun, args, kwargs))
        while R.result is NoResult: time.sleep(0.01)
        return R.result

    return fun2

def launch_browser(html, quit_function=None, echo=True):

    window = gtk.Window()
    browser = implementation.create_browser()
    settings = browser.get_settings()
    settings.set_property('enable-default-context-menu', False)

    box = gtk.VBox(homogeneous=False, spacing=0)
    window.add(box)


    if quit_function is not None:
        window.connect('destroy', quit_function)

    box.pack_start(browser, expand=True, fill=True, padding=0)
    window.set_icon_name('preferences-desktop-personal')
    window.set_title(_('Witaj w Magicznym Remiksie!'))
    window.set_position(gtk.WIN_POS_CENTER)
    window.set_default_size(800, 500)
    window.set_size_request(800, 500)
    window.set_resizable(False)
    window.show_all()

    message_queue = Queue.Queue()

    def title_changed(title):
        if title != 'null': message_queue.put(title)

    implementation.connect_title_changed(browser, title_changed)

    implementation.open_uri(browser, html)

    def web_recv():
        if message_queue.empty():
            return None
        else:
            msg = message_queue.get()
            if echo: print '>>>', msg
            return msg

    def web_send(msg):
        if echo: print '<<<', msg
        asynchronous_gtk_message(implementation.inject_javascript)(browser, msg)

    return browser, web_recv, web_send


def start_gtk_thread():
    # Start GTK in its own thread:
    gtk.gdk.threads_init()
    gtk.gdk.threads_enter()
    thread.start_new_thread(gtk.main, ())

def kill_gtk_thread():
    asynchronous_gtk_message(gtk.main_quit)()
