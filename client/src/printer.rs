extern crate serial;


use std::env;
use std::io;
use std::time::Duration;

use std::io::prelude::*;
use printer::serial::prelude::*;


const SERIAL_NAME:&str = "/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0";


pub fn test() {
    let mut port = serial::open(SERIAL_NAME).unwrap();
    interact(&mut port).unwrap();
}

fn interact<T: SerialPort>(port: &mut T) -> io::Result<()> {
    try!(port.reconfigure(&|settings| {
        try!(settings.set_baud_rate(serial::Baud9600));
        settings.set_char_size(serial::Bits8);
        settings.set_parity(serial::ParityNone);
        settings.set_stop_bits(serial::Stop1);
        settings.set_flow_control(serial::FlowNone);
        Ok(())
    }));

    try!(port.set_timeout(Duration::from_millis(1000)));

    let mut buf: Vec<u8> = (0..255).collect();

    try!(port.write(&buf[..]));
    try!(port.read(&mut buf[..]));

    Ok(())
}


//
//pub struct Printer<T: SerialPort> {
//    // If None, Serial is not supported on this device
//    serial: T,
//}
//
//impl Printer<SerialPort> {
//    pub fn new() -> Printer<SerialPort>{
//        let mut port = serial::open(SERIAL_NAME).unwrap();
//
////        let mut port = serial::open(SERIAL_NAME);
////
////        let serial = match port {
////            Ok(port) => {
////                println!("Connected to serial port!");
////                Some(port)
////            },
////            Err(error) => {
////                println!("Unable to open serial port: {}", error);
////                None
////            }
////        };
//
//        Printer{port}
//    }
//
//
//    pub fn print_text(&self, text: &str){
//        println!("Pretend I'm printing some text: {}", text);
//    }
//}


//pub fn print_image(image: ...something...){
//    let _ignore = image;
//}
