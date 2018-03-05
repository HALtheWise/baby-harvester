FROM resin/raspberrypi-debian

ENV INITSYSTEM on

RUN apt-get -q update && apt-get install -yq -f apt-utils libssl-dev \
	build-essential curl file \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

COPY . /usr/src/app

RUN cd client \
    $HOME/.cargo/bin/cargo build

FROM petrosagg/resin-wpe:raspberrypi3-06da0ed

COPY udev-rules/ /etc/udev/rules.d/

COPY wpe-init /wpe-init

CMD [ "/wpe-init" ]

ENV WPE_URL="www.google.com"