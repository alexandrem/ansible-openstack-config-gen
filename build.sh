#!/bin/bash

folder=$1
name=$2
release=$3

genroot=generated/$name/$release
tmp=generated/.tmp/$name/$release

# clean previous runs
rm -fr $genroot $tmp

mkdir -p $genroot/vars $genroot/vars/defaults $genroot/templates $tmp/vars

echo "Building default vars for $name from release $release..."

default_files=""

for conf in $(find $folder -name *.conf); do
	echo "file: $conf"

	basename=$(basename $conf | awk '{print tolower($0)}')
	#base=$(echo ${basename%.*})

	# generate default variables
	python gen_ansible_defaults.py $conf $name os_$release > ./$genroot/vars/defaults/$basename.yml

	# generate dynamic variables remapping
	python gen_ansible_dyn_defaults.py $conf $name os_$release > ./$tmp/vars/$basename.yml

	# generate template file
	python gen_conf_template.py $conf $name os_$release > ./$genroot/templates/$basename.j2

	default_files+="$basename.yml "
done

# merge generated dynamic var files into single one
out=./$genroot/vars/defaults.yml
echo "---" > $out
for file in $(find ./$tmp/vars -name *.yml); do
	cat $file >> $out
	echo "" >> $out
done

# generate main.yml that includes all default variables
include_defaults=$(echo $default_files | tr " " "\n" | sed '/^$/d' | sed 's|\(.*\.yml\)|include_vars: defaults/\1|')
cat <<EOF | tee ./$genroot/vars/main.yml &> /dev/null
---
$include_defaults

include_vars: defaults.yml
EOF

echo "Final output is in: $genroot"