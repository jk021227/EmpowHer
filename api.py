from dotenv import load_dotenv
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import pandas as pd
import os

# Load environment variables from the .env file
load_dotenv()

# Load CSV file
file_name = 'razors_products.csv'
product_type = file_name.split('_')[0]
df = pd.read_csv(file_name)
# Your Personal Access Token (PAT) loaded from .env
PAT = os.getenv('PAT')

# Make sure PAT is loaded correctly
if not PAT:
    raise ValueError("PAT not found in environment. Make sure it's set in the .env file.")

# Specify the correct user_id/app_id pairings
USER_ID = 'clarifai'
APP_ID = 'main'

# Specify the model details and image URL
MODEL_ID = 'color-recognition'
MODEL_VERSION_ID = 'dd9458324b4b45c2be1a7ba84d27cd04'

# RGB to Hex conversion function
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb).lower()

# Colors that are considered "girly" (as per the provided RGB values)
GIRLY_COLORS_RGB = [
    (255, 240, 245), (255, 228, 225), (255, 192, 203), (255, 160, 122),
    (255, 127, 80), (255, 105, 180), (255, 99, 71), (255, 69, 0), 
    (255, 20, 147), (255, 0, 255), (255, 0, 0), (250, 128, 114), 
    (240, 128, 128), (238, 130, 238), (233, 150, 122), (230, 230, 250), 
    (221, 160, 221), (220, 20, 60), (219, 112, 147), (218, 165, 32), 
    (218, 112, 214), (216, 191, 216), (208, 32, 144), (205, 92, 92), 
    (199, 21, 133), (188, 143, 143), (153, 50, 204), (148, 0, 211), 
    (147, 112, 219), (139, 0, 139), (139, 0, 0), (138, 43, 226), 
    (128, 0, 128), (128, 0, 0)
]

# Convert RGB girly colors to hex
GIRLY_COLORS = [rgb_to_hex(color) for color in GIRLY_COLORS_RGB]

# Exclude white and similar colors
EXCLUDED_COLORS = ['#ffffff', '#fefdfe']

# Set up the Clarifai API with gRPC
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)

metadata = (('authorization', 'Key ' + PAT),)

def is_image_girly(image_url):
    # Send the request to the Clarifai API
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID),
            model_id=MODEL_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            url=image_url
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    # Check for success
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        return "no"

    # Get the output from the response
    output = post_model_outputs_response.outputs[0]

    girly_value_total = 0
    not_girly_value_total = 0

    # Process each color in the response
    for color in output.data.colors:
        hex_color = color.w3c.hex.lower()
        color_value = color.value

        # Exclude white and background colors
        if hex_color not in EXCLUDED_COLORS:
            if hex_color in GIRLY_COLORS:
                girly_value_total += color_value
            else:
                not_girly_value_total += color_value

    # Determine if the image is girly based on the total values
    if girly_value_total > not_girly_value_total:
        return "yes"
    else:
        return "no"

# Iterate over each row in the CSV
df['is_girly'] = df['Image URL'].apply(is_image_girly)

# Save the updated CSV
updated_file_name = f'{product_type}_updated_file.csv'
df.to_csv(updated_file_name, index=False)

print("Updated CSV with 'is_girly' column saved.")