extern crate rumqtt;
extern crate reqwest;

use rumqtt::{MqttOptions, MqttClient};
use communications::reqwest::header::{Authorization, Basic};
use std::env;

pub fn mqtt() -> MqttClient{
    let client_options = MqttOptions::new()
        .set_keep_alive(5)
        .set_reconnect(2)
        .set_client_id("baby-harvester-client")
        .set_broker("test.mosquitto.org:1883");

    let mq = MqttClient::start(client_options, None);

    mq.expect("Unable to start mq client")
}

pub fn change_token() {
    let client = reqwest::Client::new();
    let user = match env::var("DEVICE_NAME") {
        Ok(val) => val,
        Err(e) => panic!("could not find device name: {}", e),
    };
    let passwd = match env::var("APP_SECRET") {
        Ok(val) => val,
        Err(e) => panic!("could not find app secret: {}", e),
    };
    let credentials = Basic {
        username: user,
        password: Some(passwd),
    };
    let mut response = client.get("https://baby-harvester-gateway.herokuapp.com/changetoken")
        .header(Authorization(credentials))
        .send()
        .expect("Failed to send request");
    println!("Token request status: {}", response.status());
}