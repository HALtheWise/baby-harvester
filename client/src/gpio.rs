extern crate rppal;


use std::thread;
use std::time::Duration;

use gpio::rppal::gpio::{Gpio, Mode, Level};
use gpio::rppal::system::DeviceInfo;

// The GPIO module uses BCM pin numbering. BCM 18 equates to physical pin 12.
const LED_PIN:u8 = 18;

pub fn setup(){
    let device_info = DeviceInfo::new().unwrap();
    println!("Model: {} (SoC: {})", device_info.model(), device_info.soc());

    let mut gpio = Gpio::new().unwrap();
    gpio.set_mode(LED_PIN, Mode::Output);

    // Blink an LED attached to the pin on and off
    gpio.write(LED_PIN, Level::High);
    thread::sleep(Duration::from_millis(500));
    gpio.write(LED_PIN, Level::Low);
}

pub fn set_bell(ringing: bool){
    let _ignore = ringing;
    return;
}

pub fn set_light(on: bool){
    let _ignore = on;
    return;
}

pub fn get_button() -> bool{
    false
}
