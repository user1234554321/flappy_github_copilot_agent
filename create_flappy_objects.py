from PIL import Image, ImageDraw

# Create bird frame images
for i in range(3):
    bird_img = Image.new('RGBA', (34, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bird_img)
    draw.ellipse((0, 0, 24, 24), fill='yellow')
    draw.ellipse((8, 8, 12, 12), fill='black')
    draw.rectangle((24, 10, 34, 14), fill='yellow')
    bird_img.save(f'bird_frame_{i}.png')

# Create pipe image
pipe_img = Image.new('RGBA', (70, 500), (0, 0, 0, 0))
draw = ImageDraw.Draw(pipe_img)
draw.rectangle((0, 0, 70, 500), fill='green')
draw.rectangle((0, 0, 70, 50), fill='darkgreen')
pipe_img.save('pipe_detailed.png')

# Create background image
background_img = Image.new('RGBA', (400, 600), 'skyblue')
background_img.save('background_detailed.png')