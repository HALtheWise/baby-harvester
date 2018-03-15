# baby-harvester

## Resin deploy setup
We decided to use resin.io to take care of deploying to multiple RasPis. Using resin, we were able to easily deploy code to all our devices at once.

Resin.io has useful documentation for getting started with their system. Go to https://docs.resin.io/learn/getting-started/raspberrypi3/nodejs/ to review their documentation and set up your own device(s).

Be careful about testing that what you deploy to resin actually works. There is a log terminal for each device available from the resin dashboard, and those logs might be your only clue as to whether or not there were failures in a given build. Sometimes things will fail, but the container will still build, so unless you check the logs you might find yourself assuming that everything worked even if it didn't.

## Developing on a single device
If you want to develop on one device without deploying your code to all other devices, look into using resin's built-in local mode. You can find information on local mode and how to use it at https://docs.resin.io/development/local-mode/.

## Deploying WPE to the screen
We forked and copied material from https://github.com/resin-io-projects/resin-wpe in order to deploy to our PiTFT screen.

**Note:** The base_image folder in the above linked repo is only useful if you intend to 1) examine what went into the base image, or 2) build your own image. It is *not* a necessary part of getting WPE to work via resin because the Dockerfile pulls from a Docker repo which holds the original base image.

We ran into issues trying to use this repo with a RasPi Zero W. The resin-wpe repo is based on developing with a RasPi3, which could be part of the problem, although the same Docker repo used for the base image also has another base image tagged as raspi-zero. When we switched over to using Python for our demo, we discovered that we were using some of the wrong GPIO pins to connect to the screen, and that ignoring the screen's touch capability made things easier. It is possible that had we had the same realization while developing using resin on a Zero W, we would have gotten the screen to work. It is also possible that using that knowledge to test on a RasPi3 would work. However given that we pivoted to Python and did not test either of these possibilities, we can't say for sure.