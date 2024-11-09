import openai
import base64
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
client = openai.OpenAI(api_key='sk-459QGMpr4CLLU5QWqDsWbw', base_url='https://nova-litellm-proxy.onrender.com')

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from GetImage import get_img_src

# Set up Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

# Specify the path to your chromedriver binary using Service
service = Service(executable_path="/usr/local/bin/chromedriver")

# Initialize the driver with the Service object and options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Facebook post URL (replace with the actual post URL)
facebook_url = input("Paste a url to a facebook post here: ")
src = get_img_src(facebook_url, driver)
#print(src)
image_url = src

# Download the image using the requests library
response = requests.get(image_url)

if response.status_code == 200:
    # Write the image to a file
    with open("downloaded_image.jpg", "wb") as file:
        file.write(response.content)
    #print("Image downloaded successfully.")
else:
    print("Failed to download image.")

# Close the browser
driver.quit()

image_path = "downloaded_image.jpg"

prompt = "You are an AI detection tool tasked with analyzing images in social media posts to determine the likelihood that they are AI-generated. Follow these steps: 1) Analyze the Image: Examine the image for common features of AI-generated content. Look for the following specific indicators; Unnatural Textures or Patterns: Repetitive or overly smooth areas that lack natural variation, Textures that appear too perfect or uniform. Inconsistent Lighting or Shadows: Shadows that do not align with the light source, Inconsistent lighting across different parts of the image. Anomalies in Human Features: Asymmetry in facial features (e.g., eyes at different levels), Unnatural eye shapes or reflections, Irregularities in hair patterns or unnatural hairlines. Artifacts or Distortions: Blurring or pixelation in certain areas, Distorted or warped objects, especially in the background, Unnatural edges or outlines around objects. Background Anomalies: Inconsistent or nonsensical backgrounds, Objects that appear to float or have no clear connection to the ground. 2) Assess Likelihood: Based on your analysis, assign a percentage likelihood (0-100%) that the image is AI-generated. Use the following scale: 0%: Guaranteed not AI-generated, 1-49%: Unlikely to be AI-generated, 50-74%: Possibly AI-generated, 75-99%: Likely AI-generated, 100%: Guaranteed AI-generated. 3) Output: Provide only the percentage likelihood of the image being AI-generated. Example Output: 85%"

# Encode the image file to base64
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                },
            ],
        }
    ],
)

print("The chance of this being AI-generated is: ")
print(completion.choices[0].message.content)

