extern crate rumqtt;
extern crate reqwest;

use rumqtt::{MqttOptions, MqttClient, MqttCallback, QoS};
use communications::reqwest::header::{Authorization, Basic};
use std::env;
use std::thread;
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};

pub fn mqtt() {
    let mqtt_user = match env::var("MQTT_USER") {
        Ok(val) => val,
        Err(e) => {println!("could not find mqtt user: {}", e); return},
    };
    let mqtt_pass = match env::var("MQTT_PASS") {
        Ok(val) => val,
        Err(e) => {println!("could not find mqtt pass: {}", e); return},
    };
    let dev_name = match env::var("DEVICE_NAME") {
        Ok(val) => val,
        Err(e) => {println!("could not find device name: {}", e); return},
    };
    let client_options = MqttOptions::new()
        .set_reconnect(5)
        .set_broker("llama.rmq.cloudamqp.com:1833")
        .set_user_name(&mqtt_user)
        .set_password(&mqtt_pass);

    let count = Arc::new(AtomicUsize::new(0));
    let count = count.clone();

    let counter_cb = move |message| {
        count.fetch_add(1, Ordering::SeqCst);
        println!("message --> {:?}", message);
    };

    let msg_callback = MqttCallback::new().on_message(counter_cb);

    let mut request = MqttClient::start(client_options, Some(msg_callback)).expect("Coudn't start");
    //let print_channel = format!("{}/print/text", &dev_name);
    let topics = vec![("harvey/print/text", QoS::Level0)];
    request.subscribe(topics).expect("Subcription failure");
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
    let response = client.get("https://baby-harvester-gateway.herokuapp.com/changetoken")
        .header(Authorization(credentials))
        .send()
        .expect("Failed to send request");
    println!("Token request status: {}", response.status());
}