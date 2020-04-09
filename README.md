
# COVID-19 stats -  Phone Call
This was the first time using a twilio api, it was pretty cool. I built an app which asks the user for a country or continent, and when given dring the phone call, an automated message will tell the number of total cases and numeber of deaths, for that specific country, along with a positive message. I made this for people who have a hard time seeing, but have decent hearing. I have seen lots of apps for people who can see, but not much for people who have bad eye sight.

## Getting Started
* Download files and unzip them
* there shold be 1 file named make_call.py, and a folder named ENV
* you will need to have virtualenv installed, https://pypi.org/project/virtualenv/
* you will need a twilio account, with a phone number

## Running program
* go into the project filer, where the two item you see are 'make_call.py' and the ENV folder
* if virtualenv is installed properly, you should be able to use the command 'source'

```
source ENV/bin/activate
python make_call.py
```

* Open another terminal, and type

```
source ENV/bin/activate
ngrok http 5000
```

*after executing the second command, you will get an address similar to 'https://ac1234567.ngrok.io'

* copy it, and paste it here in the "A CALL COMES IN SECTION"
* MAKE SURE TO ADD A "/voice" at the end 

<img style="-webkit-user-select: none;margin: auto;" src="https://nootropicdesign.com/projectlab/wp-content/uploads/2018/11/Twilio_phone_number_setup.png">

* To get here, you will need to have bought a number, and click on it to configure/set it up

## Future Work
* In the future, I hope to ask the user for the language in the beginning of the application, then the rest of the interaction will be in the language specified

## Acknowledgments
* twilio
* dev.to

## Author
* Michael Oppong