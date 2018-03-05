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

    communications::mqtt();

    //test_gpio();
    //test_printer();
//    test_screen();
    communications::change_token();
}

fn test_gpio() {
    let mut io = gpio::GPIOHandler::new();
    io.set_light(true);
    io.set_bell(true);
    thread::sleep(Duration::from_millis(1000));
    io.set_light(false);
    io.set_bell(false);
    thread::sleep(Duration::from_millis(1000));

//    let button_state =io.get_button();
//    io.set_light(button_state);
}

fn test_printer() {
//    let mut print = printer::Printer::new();
//    print.print_text("Hello World");
//    printer::test();
    let mut print = printer::get_printer();
    printer::print_text(&mut print,"Baby Harvester Active");
}

fn test_screen() {
    screen::show_text("Hello World");

    thread::sleep(Duration::from_millis(2000));

    screen::show_url("https://www.olin.edu");

    thread::sleep(Duration::from_millis(2000));

    screen::clear()
}