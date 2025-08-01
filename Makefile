.PHONY: install build-deb clean

export PACKAGE_NAME=geomapper

install: check-settings
	poetry install

check-settings:
	./check_settings.sh

test: install
	poetry run pytest

set-version:
	$(eval VERSION := $(shell poetry version -s))
	@echo $(VERSION)
	sed -i -e "s/###RELEASE_VERSION###/$(VERSION)/" debian/changelog

build-deb: check-settings set-version

	poetry export --without-hashes --format=requirements.txt > requirements.txt

	$(shell echo ${GPG_KEY} | base64 --decode | gpg --batch --import)
	$(eval KEYID := $(shell gpg --list-keys --with-colons | grep pub | cut -d: -f5))
	@echo "Signing with key id: $(KEYID)"

	@echo "Build package"
	dpkg-buildpackage --no-sign
	
	@echo "Signing package"
	$(shell echo "${PASSPHRASE}" | debsign -k$(KEYID) -p"gpg --batch --pinentry-mode loopback --passphrase-fd 0" ../${PACKAGE_NAME}_*.changes)	

	mkdir -p target
	mv ../${PACKAGE_NAME}_* target/

test:
	@echo "Unit tests not implemented yet"

clean:
	rm -rf dist
	rm -rf target
	rm -rf *.egg-info
	rm -rf debian/.debhelper
	rm -f debian/files
	rm -f debian/*.substvars
	rm -f debian/*.log
	rm -f debian/debhelper-build-stamp
	rm -f debian/${PACKAGE_NAME}.postinst.debhelper
	rm -f debian/${PACKAGE_NAME}.postrm.debhelper
	rm -f debian/${PACKAGE_NAME}.prerm.debhelper
	rm -rf debian/${PACKAGE_NAME}
	rm -f *.tar.gz
	rm -f requirements.txt