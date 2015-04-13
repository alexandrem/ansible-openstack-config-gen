#!/bin/bash

folder=$1
name=$2
distro=$3

genroot=generated/$name/_dist/$distro
tmp=generated/.tmp/$name/_dist/$distro

# clean previous runs
rm -fr $genroot $tmp

mkdir -p $genroot
mkdir -p $tmp

echo "build distro vars for $name from release $release"

for conf in $(find $folder -name *.conf); do
    echo "file: $conf"

    basename=$(basename $conf | awk '{print tolower($0)}')
    base=$(echo ${basename%.*})

    python gen_ansible_defaults.py $conf $name os_dist > ./$tmp/${base}_defaults.yml
    python gen_ansible_dyn_defaults.py $conf $name os_dist > ./$tmp/$base.yml
done

