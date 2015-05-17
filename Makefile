PACKAGE = mrwelcome
VERSION = 0.1.0
GITPATH = git://git@github.com:napcok/mrwelcome.git

TEXT_FILES = Makefile

DIRS = etc usr po

FILES = $(TEXT_FILES) $(DIRS) LICENSE

clean:
	rm -f *~ \#*\#

cleandist: clean
	rm -fr $(PACKAGE)-$(VERSION) $(PACKAGE)-$(VERSION).tar.xz

install:
	make -C po DESTDIR=$(RPM_BUILD_ROOT)/usr install
	
dir:
	mkdir $(PACKAGE)-$(VERSION)

localcopy: dir
	tar c --exclude=.git $(FILES) | tar x -C $(PACKAGE)-$(VERSION)

tar: localcopy
	tar cvYf $(PACKAGE)-$(VERSION).tar.xz $(PACKAGE)-$(VERSION)
	rm -fr $(PACKAGE)-$(VERSION)

dist: cleandist dir localcopy tar
