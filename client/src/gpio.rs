extern crate rppal;


use std::thread;
use std::time::Duration;

use gpio::rppal::gpio::{Gpio, Mode, Level};
use gpio::rppal::system::DeviceInfo;
use gpio::rppal::system::Error;

// The GPIO module uses BCM pin numbering. BCM 18 equates to physical pin 12.
const LED_PIN:u8 = 18;

pub struct GPIOHandler {
    // If None, GPIO is not supported on this device
    gpio: Option<Gpio>,
}

impl GPIOHandler {

    pub fn new() -> GPIOHandler{
        let device_info = DeviceInfo::new();

        let gpio = match device_info {
            Ok(device_info)=>{
                println!("Model: {} (SoC: {})", device_info.model(), device_info.soc());
                let mut gpio = Gpio::new().unwrap();
                gpio.set_mode(LED_PIN, Mode::Output);

                // Blink an LED attached to the pin on and off
                gpio.write(LED_PIN, Level::High);
                thread::sleep(Duration::from_millis(500));
                gpio.write(LED_PIN, Level::Low);

                Some(gpio)
                },
            Err(error) => {
                println!("Error encountered, perhaps this is a laptop?, {}", error);
                None
            }
        };

        println!("This device {} a Raspi", match gpio { Some(_)=>"is", None=>"is not"});

        GPIOHandler{gpio}



     }

    pub fn set_bell(&self, ringing: bool){
        let _ignore = ringing;
        return;
    }

    pub fn set_light(&self, on: bool){
        match &self.gpio {
            &Some(ref gpio)=>{
                gpio.write(LED_PIN, match on{true=>Level::High,false=>Level::Low})
            },
            &None=>{
                println!("Pretend I'm turning {} the light!", match on { true=>"on", false=>"off"})
            }
        }
        return;
    }

    pub fn get_button(&self) -> bool{
        false
    }

    fn from_bool(status:bool) -> (Level, &'static str) {
        match status {
            true => (Level::High, "on"),
            false => (Level::Low, "off")
        }
    }

}
