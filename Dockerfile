FROM cbekins/babyharvester:pizero

COPY udev-rules/ /etc/udev/rules.d/

# ENV WPE_URL="www.celinabekins.com"

COPY wpe-init /wpe-init

CMD [ "/wpe-init" ]