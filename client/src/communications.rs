extern crate rumqtt;

use rumqtt::{MqttOptions, MqttClient};

pub fn mqtt() -> MqttClient{
    let client_options = MqttOptions::new()
        .set_keep_alive(5)
        .set_reconnect(2)
        .set_client_id("baby-harvester-client")
        .set_broker("test.mosquitto.org:1883");

    let mq = MqttClient::start(client_options, None);

    mq.expect("Unable to start mq client")
}