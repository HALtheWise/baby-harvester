FROM resin/raspberrypi-debian

ENV INITSYSTEM on

# TODO: merge these, add the cache removal again, add -q flag to install
RUN apt-get -q --allow-unauthenticated update
RUN apt-get install -y -f --allow-unauthenticated apt-utils libssl-dev \
	build-essential curl file
#	&& apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN curl https://sh.rustup.rs -sSf | sh -s --  -y

COPY . /usr/src/app

RUN cd client && \
    $HOME/.cargo/bin/cargo build

CMD .client/target/debug/client
