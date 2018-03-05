mod communications;
mod gpio;
mod printer;
mod screen;

extern crate rumqtt;

use std::thread;
use std::time::Duration;

use rumqtt::QoS;

fn main() {
    println!("Hello, world!");
    let payload = String::from("{}. hello rust");

    let mut mq = communications::mqtt();

    mq.publish("hello/rust", QoS::Level1, payload.into_bytes())
         .expect("Publish failure");

    test_gpio();
//    test_printer();
//    test_screen();
}

fn test_gpio() {
    gpio::setup();
    gpio::set_light(true);
    gpio::set_bell(true);
    thread::sleep(Duration::from_millis(1000));
    gpio::set_light(false);
    gpio::set_bell(false);
    thread::sleep(Duration::from_millis(1000));

    gpio::set_light(gpio::get_button());
}

fn test_printer() {
    printer::print_text("Hello World");
}

fn test_screen() {
    screen::show_text("Hello World");

    thread::sleep(Duration::from_millis(2000));

    screen::show_url("https://www.olin.edu");

    thread::sleep(Duration::from_millis(2000));

    screen::clear()
}