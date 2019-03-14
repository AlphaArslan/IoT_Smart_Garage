# project works as follows:
*  it checks if there is a place inside the garage
	* = if no:
	 	* the door will not open
	*	= if yes:
		* the camera at the door will check the plate
		* if the car is allowed, door will open
		* if the car is not allowed, door stays closed
---

# Technical:
### project contains two parts:
1. __insider__ ( checks for places inside the garage ):

		An Arduino uses for IR sensors to check for cars in for places.
		there will be two LEDs ( green & red )in every place close to an IR sensror.
		if there is a car, red LED turns on. otherwise, green LED turns on.
		a signal wire will go out from the arduino to the other part (Raspberry).
		the SIGNAL WIRE will be HIGH if there is no place inside and LOW otherwise.

1. __outsider__ ( checks for the car plates and controls the door ):

		Initializing, it tries to update the database.
		If it couldn't:
				it uses an old one.
		If SIGNAL WIRE is HIGH:
	 			we just keep the door closed.
		if SIGNAL WIRE is LOW:
				we wait for a signal from Ultrasonic indicating the presence
				of a car.
				when we detect a car, we capture a pic and send it online to be processed.
				we get a response including plate number assumption.
				we check for the assumptions in the database.
				if found, we open the door.
--------------------------------------------------------------------------------
## notes:
* 	Door is repesented by a servo motor.
		four places in the garage is just for modulation. it can be expanded.
