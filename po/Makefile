LANGUAGES=$(basename $(wildcard *.po))
PACKAGE_NAME=mrwelcome
DESTDIR=$(RPM_BUILD_ROOT)

all: gmo


clean:
	@echo " **CLEAN**"
	@rm -rf *.mo *~ tmp/
	@for lang in $(LANGUAGES); do \
		echo " **CLEANDIR** $$lang"; \
		rm -rf $$lang;\
	done


pot:
	xgettext --copyright-holder='Daniel Napora <napcok@gmail.com>' --package-name=mrwelcome --from-code=UTF-8 \
-L Python --msgid-bugs-address=http://bugs.mageia.org -o $(PACKAGE_NAME).pot ../usr/share/mrwelcome/mrwelcome.py ../usr/share/mrwelcome/helpers.py

po:
	@for lang in $(LANGUAGES); do \
		echo " Updating po for $$lang"; \
		if [ ! -f $$lang.po ]; then \
			msginit --input $(PACKAGE_NAME).pot -o $$lang-old.po;\
		else \
			mv $$lang.po $$lang-old.po; \
		fi ; \
		msgmerge -o $$lang.po $$lang-old.po $(PACKAGE_NAME).pot; \
		rm -f $$lang-old.po; \
	done

gmo:
	@echo " **COMPILING** languages: $(LANGUAGES)"
	@for lang in $(LANGUAGES); do \
		echo " **COMPILEMO** $$lang" ; \
		mkdir -p $$lang/LC_MESSAGES/; \
		msgfmt --verbose -o $$lang/LC_MESSAGES/$(PACKAGE_NAME).mo $$lang.po; \
	done
	
install:
	@echo " **INSTALL** languages: $(LANGUAGES)"
	@for lang in $(LANGUAGES); do \
		echo " **INSTALLMO** $$lang" ; \
		mkdir -p $(DESTDIR)/share/locale/$$lang/LC_MESSAGES/; \
		msgfmt -o $(DESTDIR)/share/locale/$$lang/LC_MESSAGES/$(PACKAGE_NAME).mo -f $$lang.po; \
	done
	
