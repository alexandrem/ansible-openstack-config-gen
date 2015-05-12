#!/bin/bash

RELEASES=icehouse

for release in $RELEASES; do
  ./build.sh originals/nova/$release nova $release
  ./build.sh originals/keystone/$release keystone $release
done
