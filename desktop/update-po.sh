#!/bin/bash

LANG="zh_CN"

OPTIONS='--no-location --no-wrap -j'

for i in $LANG ; do
	cat /dev/null > "./po/$i.pot"

	for j in `cat po/FILES` ; do
		xgettext $OPTIONS -o "./po/$i.pot" "$j"
	done

	msgmerge -o "./po/$i.po" "./po/$i.po" "./po/$i.pot"
done

pushd po
rm -f *.pot
