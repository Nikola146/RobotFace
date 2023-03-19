from buildhat import Motor, ColorSensor

## Set up the motors
mouth_r = Motor('A')
mouth_l = Motor('B')
eyebrows = Motor('C')

# Move the motors to 0 position
mouth_r.run_to_position(0)
mouth_l.run_to_position(0)
eyebrows.run_to_position(0)

# Set up the color sensor
color = ColorSensor('C')


# Link names of expressions to motor movement and to eye display in a dictionary
faces = {
    "neutral": {"mouth": 0, "eyebrows": 0},
    "happy": {"mouth": 45, "eyebrows": -150},
    "angry": {"mouth": -20, "eyebrows": 150},
    "sad": {"mouth": -45, "eyebrows": -40}
}

reactions = {
    "black": "neutral",
    "white": "happy",
    "red": "angry",
    "yellow": "happy",
    "green": "neutral",
    "blue": "sad"
}

# Define the functions for moving the motors
def move_mouth(position):
    mouth_l.run_to_position(position * -1, blocking=False)
    mouth_r.run_to_position(position, blocking=False)

def move_eyebrows(position):
    current_position = eyebrows.get_aposition()
    if position < current_position:
        rotation = 'anticlockwise'
    else:
        rotation = 'clockwise'
    eyebrows.run_to_position(position, direction=rotation)

# Define the function to set the facial expression
def set_face(face):
    move_mouth(face["mouth"])
    move_eyebrows(face["eyebrows"])

# Set the initial facial expression to neutral
current_face = faces["neutral"]
set_face(current_face)

# Loop forever and check the color sensor for new colors
while True:
    c = color.wait_for_new_color()
    if c in reactions.keys():
        new_face = faces[reactions[c]]
        if new_face != current_face:
            current_face = new_face
            set_face(current_face)