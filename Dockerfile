# FROM resin/raspberrypi-debian AS compiler

# ENV INITSYSTEM on

# RUN apt-get -q update && apt-get install -yq -f apt-utils libssl-dev \
# 	build-essential curl file \
# 	&& apt-get clean && rm -rf /var/lib/apt/lists/*

# WORKDIR /usr/src/app

# RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# COPY . /usr/src/app

# RUN cd client \
#     $HOME/.cargo/bin/cargo build

FROM cbekins/babyharvester:pizero

# COPY --from=compiler .client/target/debug/client .client/target/debug/client

COPY udev-rules/ /etc/udev/rules.d/

COPY wpe-init /wpe-init

ENV WPE_URL="www.google.com"

CMD [ "/wpe-init" ]