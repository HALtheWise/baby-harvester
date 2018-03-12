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
        Err(e) => {println!("could not find device name: {}", e); return},
    };
    let passwd = match env::var("APP_SECRET") {
        Ok(val) => val,
        Err(e) => {println!("could not find app secret: {}", e); return},
    };
    let credentials = Basic {
        username: user,
        password: Some(passwd),
    };
    // Consider reading this from environment variable too, in order to enable:
    // * Developers/contributors can fork the repo and run it against their own
    //   servers
    // * Using a local server during integration testing
    // * Using distinct servers for staging and production
    let mut response = client.get("https://baby-harvester-gateway.herokuapp.com/changetoken")
        .header(Authorization(credentials))
        .send()
        .expect("Failed to send request");
    println!("Token request status: {}", response.status());
}
