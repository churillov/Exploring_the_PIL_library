import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

# read image and convert to RGB
image = Image.open("readonly/msi_recruitment.gif")
image = image.convert('RGB')

# initialize key constants and variables
R, G, B = 0, 1, 2
intensity = [0.1, 0.5, 0.9]
images = []
images_meta = []
banner_height = 70
banner_margin = 10
txt_color = 'rgb(255,255,255)'  # white

# build a list of 9 images, 3 for each color channel with the appropriate color intensity
for channel in [R, G, B]:

    # multiply each channel by appropriate color intensity factor
    for i_factor in intensity:
        # img_tmp = source # split the original image into 3 separate channels (images) with 1 for each color
        img_tmp = image.split()
        img_band = img_tmp[channel].point(lambda x: x*i_factor)  # multiply the channel color by the intensity factor
        img_tmp[channel].paste(img_band)  # replace the selected channel image with its color corrected version
        img_out = Image.merge(image.mode, img_tmp)  # merge all 3 channels back into one image
        images.append(img_out)  # add the updated image to the list
        images_meta.append('channel {} intensity {}'.format(channel, i_factor))  # update the metadata

# create a contact sheet of 3 rows with one row per color channel displaying
# an image with 3 different color intensities

first_image = images[0]
contact_sheet = PIL.Image.new(first_image.mode, (first_image.width * 3, first_image.height * 3 + banner_height * 3))
font = ImageFont.truetype("arial.ttf", 55)
x = 0
y = 0

# initialize the drawing context with the contact sheet as background
banner = ImageDraw.Draw(contact_sheet)

for i, img in enumerate(images):

    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y))

    # now draw the text and create a banner below the corresponding image
    banner.text((x, y + first_image.height + banner_margin), images_meta[i], fill=txt_color, font=font)

    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x = 0
        y = y+first_image.height + banner_height
    else:
        x = x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2), int(contact_sheet.height/2)))
contact_sheet.show()
