#!/bin/bash
#modifications taken from https://www.snip2code.com/Snippet/3301030/Building-WPE-with-Yocto-for-Raspberry-Pi

set -o errexit

export MACHINE= "raspberrypi0-wifi"

DISTRO_FEATURES_remove = "x11"
DISTRO_FEATURES_append = "opengl"
__EOF__
bitbake wpe-westeros-image

source poky/oe-init-build-env
bitbake-layers add-layer ../meta-openembedded/meta-oe
bitbake-layers add-layer ../meta-openembedded/meta-python
bitbake-layers add-layer ../meta-openembedded/meta-multimedia
bitbake-layers add-layer ../meta-openembedded/meta-networking
bitbake-layers add-layer ../meta-raspberrypi
bitbake-layers add-layer ../meta-wpe
cat <<'__EOF__' >> conf/local.conf