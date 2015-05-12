#!/bin/bash

folder=$1
name=$2
release=$3

genroot=generated/$name/$release

# clean previous runs
rm -fr $genroot

mkdir -p $genroot/defaults $genroot/templates

get_namespace() {
	filename=$1

	# remove file extension and replace - by _
	namespace=$(echo ${filename%.*} | sed 's/-/_/g')

	if [[ $namespace != ${name}* ]]; then
		namespace=${name}_${namespace}
	fi
	echo $namespace
}

echo "Building ansible files for service $name from release $release..."

default_files=""

for confpath in $(find $folder -name *.conf); do
	# remove number prefix from conf name
	conf=${confpath##*_}

	echo "file: $conf ($confpath)"

	basename=$(basename $conf | awk '{print tolower($0)}')
	ori_basename=$(basename $confpath | awk '{print tolower($0)}')

	namespace=$(get_namespace $basename)
	echo "namespace $namespace"

	echo "generating default variables..."
	python gen_ansible_defaults.py $confpath $namespace os_cfg "release: $release" > ./$genroot/defaults/$ori_basename.yml

	echo "generating template files..."
	python gen_conf_template.py $confpath $namespace os_cfg "release: $release" > ./$genroot/templates/$basename.j2

	default_files+="$basename.yml "
done

echo "merging generated var defaults into a single one..."
out=./$genroot/defaults/main.yml
files=$(find ./$genroot/defaults -name *.yml)
echo "---" > $out
for file in $files; do
	cat $file | sed 's/^\-\-\-$//g' >> $out
	echo "" >> $out
done

echo "final output is in: $genroot"
