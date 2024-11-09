import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Function to download the image
def get_img_src(image_url, driver):
    # Open the Facebook post
    driver.get(image_url)
    print(driver.title)
    #time.sleep(20)  # Allow some time for the page to load completely
    #driver.save_screenshot("screenshot1.png")

    # Find the image element (adjust the XPath as per the actual structure)
    try:
        button_selector = "//div[@aria-label='Close' and @role='button']"
        close_button = driver.find_element(By.XPATH, button_selector)
        close_button.click()
        #print("Clicked the 'X' button!")
        #time.sleep(10)

        #driver.save_screenshot("screenshot2.png")
        img_xpath = "//div[@class='x10l6tqk x13vifvy']//img"
        image_element = driver.find_element(By.XPATH, img_xpath)  # Use part of the URL to find the image
        image_src = image_element.get_attribute("src")
        return image_src
    except Exception as e:
        print("Error:", e)

# # Set up Chrome options
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
#
# # Specify the path to your chromedriver binary using Service
# service = Service(executable_path="/usr/local/bin/chromedriver")
#
# # Initialize the driver with the Service object and options
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#webdriver.Chrome(service=service, options=chrome_options)

#print(get_img_src("https://www.facebook.com/share/p/18199rnFD5/"))

# Close the browser
# driver.quit()
