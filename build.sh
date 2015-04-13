#!/bin/bash

name=$1
folder=$2
release=$3

for conf in $(ls $folder/*.conf); do
	echo "file: $conf"
	genroot=generated/$name/$release

	mkdir -p $genroot/defaults
	mkdir -p $genroot/vars
	mkdir -p $genroot/templates

	basename=$(basename $conf)
	base=${basename%.*}
	filename=${conf##*/}
	dirname=$(dirname $conf)

	python gen_ansible_defaults.py $conf $name $release > ./$genroot/defaults/$base.yml
	python gen_ansible_dyn_defaults.py $conf $name $release > ./$genroot/vars/$base.yml
	python gen_conf_template.py $conf $name $release > ./$genroot/templates/$base.conf.j2
done
