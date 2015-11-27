#!/bin/bash

./build.sh originals/nova/icehouse nova icehouse
./build.sh originals/keystone/icehouse keystone icehouse
./build.sh originals/glance/icehouse glance icehouse
./build.sh originals/cinder/icehouse cinder icehouse

./build.sh originals/nova/juno nova juno
./build.sh originals/keystone/juno keystone juno
./build.sh originals/glance/juno glance juno
./build.sh originals/cinder/juno cinder juno

./build.sh originals/nova/liberty nova liberty
