import PIL
import streamlit as st
import datetime
import uuid
from streamlit.uploaded_file_manager import UploadedFile
from utils.utils import upload_image, create_unique_filename, save_to_google_sheet

st.title("Foodify.ai Data Collection 🍔🌯🍫")
st.write(
    "Upload or take a photo of your food and help us to build the world's biggest \
        indian food image database!"
)

# Store image upload ID as key, this will be changed once image is uploaded
if "upload_key" not in st.session_state:
    st.session_state["upload_key"] = str(uuid.uuid4())

uploaded_image = st.file_uploader(
    label="Upload an image of any indian food",
    type=["png", "jpeg", "jpg"],
    help="Tip: if you're on a mobile device you can also take a photo",
    # set the key for the uploaded file
    key=st.session_state["upload_key"],  
)


def display_image(img: UploadedFile) -> PIL.Image:
    """
    Displays an image if the image exists.
    """
    displayed_image = None
    if img is not None:
        # Show the image
        img = PIL.Image.open(img)
        print("Displaying image...")
        print(img.height, img.width)
        displayed_image = st.image(img, use_column_width="auto")
    return img, displayed_image


image, displayed_image = display_image(uploaded_image)

# Create image label form to submit
st.write("## Image details")
with st.form(key="image_metadata_submit_form", clear_on_submit=True):

    # Image label
    label = st.text_input(
        label="What food(s) it is in the image that you have uploaded? \
        You can enter text like: '*biryani*' or '*parotha, aloo parotha*' or '*dosa, masala dosa*' ",
        max_chars=100,
    )

    # Image upload location
    place = st.text_input(
        label="Where are you uploading this images? \
            You can enter state name if you are uploading image from India else you can enter country name. ",
        autocomplete="place",
        max_chars=100,
    )

    # Person email
    email = st.text_input(
        label="What's your email? (optional, we'll use this to contact you \
            about the app/say thank you for your image(s))",
        autocomplete="email",
    )

    # Disclaimer
    st.info(
        '**Note:** If you click "upload image", your image will be stored on \
            our servers and we will use this image to the largest indian food image database\
            in the world! *(Do not upload anything sensitive, \
            as we will make it publically available soon)*'
    )

    # Submit button + logic
    submit_button = st.form_submit_button(
        label="Upload image",
        help="Click to upload your image and label to Foodify.ai servers.",
    )
    if submit_button:
        if uploaded_image is None:
            st.error("Please upload an image.")
        else:
            # Generate unique filename for the image
            unique_image_id = create_unique_filename()

            # Make timestamp
            current_time = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            #Upload image object to AWS S3 Bucket
            with st.spinner("Uploading Image to our server..."):
                upload_image(
                    source_file=uploaded_image,
                    destination_file_name=unique_image_id + ".jpg",
                )
            st.success(
                f"Your image of {label} has been uploaded sucessfully! Thank you for your contribution :)"
            )

            info = [
                [
                    unique_image_id,
                    current_time,
                    image.height,
                    image.width,
                    label,
                    place,
                    email     
                ]
            ]

            save_to_google_sheet(info)

            # Remove (displayed) image after upload successful
            displayed_image.empty()
            
            # To do this, the key it's stored under Streamlit's
            # UploadedFile gets changed to something random
            st.session_state["upload_key"] = str(uuid.uuid4())
