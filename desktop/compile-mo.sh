#!/bin/bash

for i in `ls po/*.po`; do
	ii=`basename "$i"`
	ii="${ii%.*}"
	mkdir -p "desktop/mo/$ii/LC_MESSAGES/"
	msgfmt -o "desktop/mo/$ii/LC_MESSAGES/atomudesktop.mo" "${i}"
done
