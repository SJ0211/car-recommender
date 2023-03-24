import openai
import os
import tkinter as tk
from tkinter import ttk
import requests
import json
from PIL import Image, ImageTk, ImageDraw, ImageFont
from urllib.request import urlopen
from io import BytesIO
import cv2


# set start = True for the loop that runs only once
start = True
# openai key
openai.api_key = "api key here"

#Function that returns url of image searched, using unslplash api
def SearchImage(Carname1, Carname2, Carname3, Carname4, Carname5):

    def search(name):

        url = "https://api.unsplash.com/search/photos"

        # api key
        access_key = "api key here"

        query = name # search keyword (car's name here)
        per_page = 1

        headers = {
            "Authorization": f"Client-ID {access_key}"
        }

        # set the parameters for the API request
        params = {
            "query": query,
            "per_page": per_page,
            "collections": "298935"  # ID for the "Cars" collection on Unsplash
        }

        response = requests.get(url, headers=headers, params=params)
        data = json.loads(response.text)

        # get the URL of the first image returned
        image_url = data["results"][0]["urls"]["regular"]

        #call getimage function
        image = getImage(image_url)
        return image

    # do it for all 5 names and return u

    image1 = search(Carname1)
    image2 = search(Carname2)
    image3 = search(Carname3)
    image4 = search(Carname4)
    image5 = search(Carname5)

    print(image1, image2, image3, image4, image5)
    return image1, image2, image3, image4, image5

# image that turns url into tkinter image, crop it and resize while not making it look like a pancake
def getImage(url):
    global new_height, new_width, new_size
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    # Get original dimensions and aspect ratio
    width, height = image.size
    aspect_ratio = 5 / 3  # 5:3 aspect ratio

    # Calculate new dimensions for resizing
    if width / height > aspect_ratio:
        new_height = int(width / aspect_ratio)
        new_size = (width, new_height)
        new_width = width
    else:
        new_width = int(height * aspect_ratio)
        new_height = height
        new_size = (new_width, height)

    # Resize image to fit within new dimensions
    image = image.resize(new_size)

    # Crop image to exact dimensions
    width, height = image.size
    x = (width - new_width) // 2
    y = (height - new_height) // 2
    cropped_image = image.crop((x, y, x + new_width, y + new_height))

    resized_image = cropped_image.resize((150, 90))
    image = ImageTk.PhotoImage(resized_image)

    return image    #return tkinter image that is 150*90

# Main loop, basically
def GUI():
    global start
    global image1, image2, image3, image4, image5

    # prepare info for ASKgpt ftn
    def ask():
        global image1, image2, image3, image4, image5
        global start

        Budget = slider1.get()*1000
        Purpose = Purposeinput.get()
        Fuel = slider2.get()
        Sports = slider3.get()
        Comfort = slider4.get()
        Country = Countryinput.get()

        #ask and get output
        recommendation, image1, image2, image3, image4, image5 = AskGPT(Budget, Purpose, Fuel, Sports, Comfort, Country)

        #change gui
        output_text.delete("1.0", "end")  # clear existing text
        output_text.insert("1.0", recommendation)
        Car1.configure(image=image1)
        Car1.image = image1
        Car2.configure(image=image2)
        Car2.image = image2
        Car3.configure(image=image3)
        Car3.image = image3
        Car4.configure(image=image4)
        Car4.image = image4
        Car5.configure(image=image5)
        Car5.image = image5
        start = False



    # Create the Tkinter application
    app = tk.Tk()
    app.title("Car Recommender")

    app.lift()
    app.attributes("-topmost", True)
    app.after_idle(app.attributes, "-topmost", False)

    # Create the sliders
    slider1 = tk.Scale(app, from_=1, to=500, orient=tk.HORIZONTAL, label="Budget ($K)", length = 200)
    slider2 = tk.Scale(app, from_=1, to=5, orient=tk.HORIZONTAL, label="Fuel Economy")
    slider3 = tk.Scale(app, from_=1, to=5, orient=tk.HORIZONTAL, label="Performance")
    slider4 = tk.Scale(app, from_=1, to=5, orient=tk.HORIZONTAL, label="Comfortness")


    # Create the input text box
    Purposeinput = tk.Entry(app, width=30)
    Countryinput = tk.Entry(app, width=30)

    #run once at the beginning
    if start == True:
        width, height = 150, 90
        image = Image.new('RGB', (width, height), color='white')

        draw = ImageDraw.Draw(image)

        font = ImageFont.truetype('arial.ttf', size=15)

        text = "No Image Available"
        text_width, text_height = draw.textsize(text, font)

        x = (width - text_width) // 2
        y = (height - text_height) // 2

        draw.text((x, y), text, fill='black', font=font)
        image = image.resize((150, 90))
        image = ImageTk.PhotoImage(image)
        Car1 = tk.Label(app, image=image)
        Car2 = tk.Label(app, image=image)
        Car3 = tk.Label(app, image=image)
        Car4 = tk.Label(app, image=image)
        Car5 = tk.Label(app, image=image)
    else:
        pass


    # Create a button
    button = tk.Button(app, text="ASK AI!", command=ask)

    # Create the output text box
    output_text = tk.Text(app, width=40, height=15)

    # Create a label for the input text box
    Purposeinput_label = tk.Label(app, text="Purpose:")
    Countryinput_label = tk.Label(app, text="Country of residence:")

    # Create a label for the output text box
    output_label = tk.Label(app, text="Output:")

    # Add the sliders to the application
    slider1.grid(padx=10, pady=5, row=0, column=0)
    slider2.grid(padx=10, pady=5, row=1, column=0)
    slider3.grid(padx=10, pady=5, row=2, column=0)
    slider4.grid(padx=10, pady=5, row=3, column=0)

    # Add the input label and text box to the application
    Purposeinput_label.grid(pady=5, row=4, column=0)
    Purposeinput.grid(pady=5, row=5, column=0)

    Countryinput_label.grid(pady=5, row=6, column=0)
    Countryinput.grid(pady=5, row=7, column=0)

    button.grid(row=0, column=2)

    # Add the output label and text box to the application
    output_label.grid(pady=5, row=1, column=2)
    output_text.grid(pady=5, row=2, column=2, rowspan=4)


    Car1.grid(row=0, column=1, rowspan=2)
    Car2.grid(row=1, column=1, rowspan=3)
    Car3.grid(row=3, column=1, rowspan=2)
    Car4.grid(row=5, column=1, rowspan=2)
    Car5.grid(row=7, column=1, rowspan=2)

    # Start the Tkinter event loop
    app.mainloop()

# asking chatgpt with prompt
def AskGPT(Budget, Purpose, Fuel, Sports, Comfort, Country):

    print(Budget, Purpose, Fuel, Sports, Comfort, Country)
    if Fuel == 5:
        FuelText = "high fuel economy"
    elif Fuel == 4:
        FuelText = "Good fuel economy"
    elif Fuel == 3:
        FuelText = "Average fuel economy"
    elif Fuel == 2:
        FuelText = "Acceptable fuel economy"
    else:
        FuelText = "Efficiency doesn't matter"

    if Sports == 5:
        SportsText = "High Performance"
    elif Sports == 4:
        SportsText = "Fairly high performance"
    elif Sports == 3:
        SportsText = "Average performance"
    elif Sports == 2:
        SportsText = "Acceptable performance"
    else:
        SportsText = "performance doesn't matter"




    prompt = (f"Recommend cars to buy that satisfies the conditions below:\n"
              f"1. Price Range: ${str(Budget)} +- {str(0.1*Budget)} \n"
              f"2. Purpose: {Purpose}\n"
              f"3. {FuelText}"
              f"4. {SportsText}\n"
              f"5. Will buy/use in: {Country}\n"
              f"The purpose of the car will be: {Purpose}\n"
              f"recommendation 5 options of car that is available (DO NOT RECOMMEND A CAR THAT IS OUT OF PRICE RANGE or add explanation. answer in this format: #. Carname: Price range):"
              f"")
    model = "text-davinci-003"
    temperature = 0.5
    max_tokens = 100

    # ask openai
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Extract the generated text from the API response
    recommendation = response.choices[0].text.strip()

    print(recommendation)

    items = recommendation.splitlines()
    Carname1 = items[0].strip().split(":")[0].split(" ", 1)[1]
    Carname2 = items[1].strip().split(":")[0].split(" ", 1)[1]
    Carname3 = items[2].strip().split(":")[0].split(" ", 1)[1]
    Carname4 = items[3].strip().split(":")[0].split(" ", 1)[1]
    Carname5 = items[4].strip().split(":")[0].split(" ", 1)[1]

    #return images (searchimage finds image for carname and optimise (form, size) it for tkinter, see above
    Image1, Image2, Image3, Image4, Image5 = SearchImage(Carname1, Carname2, Carname3, Carname4, Carname5)


    return recommendation, Image1, Image2, Image3, Image4, Image5

#run main ftn
GUI()