import pygame
import pygame_gui
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

title_font = pygame.font.SysFont("Arial", 64)
button_font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 16)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_RADIUS = 25
BUTTON_MARGIN = 20
BACK_WIDTH = 100
BACK_HEIGHT = 50
PLANT_WIDTH = 30
PLANT_HEIGHT = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Pygame Example")

clock = pygame.time.Clock()

page = 0
theme = "light"
notifications = True
button_colors = [RED, RED, RED, RED]

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
theme_picker = pygame_gui.elements.UIDropDownMenu(options_list=["light", "dark"], starting_option=theme, relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100), (200, 50)), manager=manager)
notification_toggle = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (200, 50)), text="Notifications: ON", manager=manager)

color_pickers = []
for i in range(4):
    color_picker = pygame_gui.elements.UIColourPicker(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + (i + 1) * 100), (200, 100)), manager=manager)
    color_picker.set_colours([RED, RED, RED, RED])
    color_pickers.append(color_picker)

garden_width = 0
garden_height = 0
garden_unit = ""
width_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100), (100, 50)), manager=manager)
height_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (100, 50)), manager=manager)
width_unit = pygame_gui.elements.UIDropDownMenu(options_list=["Feet", "Inches", "Meters", "Centimeters"], starting_option="Feet", relative_rect=pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100), (100, 50)), manager=manager)
height_unit = pygame_gui.elements.UIDropDownMenu(options_list=["Feet", "Inches", "Meters", "Centimeters"], starting_option="Feet", relative_rect=pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (100, 50)), manager=manager)
submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100), (200, 50)), text="Submit", manager=manager)
garden_rect = pygame.Rect(0, 0, 0, 0)
plant_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 - 100), (200, 50)), manager=manager)
add_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2), (200, 50)), text="Add", manager=manager)
plants = []
selected_plants = []

diseases = ["Powdery Mildew", "Leaf Spot", "Rust", "Anthracnose", "Blight"]
disease_descriptions = {
    "Powdery Mildew": "A fungal disease that causes white or gray patches on the leaves, stems, and flowers of plants. It can reduce photosynthesis, growth, and yield. To prevent or treat it, avoid overhead watering, increase air circulation, remove infected parts, and apply fungicides.",
    "Leaf Spot": "A fungal or bacterial disease that causes brown, black, or yellow spots on the leaves of plants. It can reduce photosynthesis, growth, and yield. To prevent or treat it, avoid overhead watering, remove infected leaves, and apply fungicides or bactericides.",
    "Rust": "A fungal disease that causes orange, yellow, or brown pustules on the leaves and stems of plants. It can reduce photosynthesis, growth, and yield. To prevent or treat it, avoid overhead watering, remove infected parts, and apply fungicides.",
    "Anthracnose": "A fungal disease that causes dark, sunken lesions on the leaves, stems, and fruits of plants. It can cause wilting, defoliation, and fruit rot. To prevent or treat it, avoid overhead watering, prune infected branches, and apply fungicides.",
    "Blight": "A fungal or bacterial disease that causes rapid and extensive browning and death of plant tissues. It can cause wilting, defoliation, and fruit rot. To prevent or treat it, avoid overhead watering, remove infected parts, and apply fungicides or bactericides."
}
disease_scan = None
disease_text = None

moisture_levels = ["0% - 10%", "10% - 30%", "30% - 60%", "60% - 100%"]
moisture_scan = None
moisture_text = None

nutrients = ["Phosphorus", "Potassium", "Calcium", "Magnesium", "Sulfur", "Sodium", "Manganese", "Nickel", "Zinc", "Copper", "Boron"]
nutrient_scan = None
nutrient_text = None

sunlight_levels = ["Sunlight levels are good!", "Sunlight levels are bad.", "Sunlight levels are perfect."]
sunlight_scan = None
sunlight_text = None

running = True
while running:

    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH = event.w
            SCREEN_HEIGHT = event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            manager.set_window_resolution((SCREEN_WIDTH, SCREEN_HEIGHT))
            theme_picker.set_position((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
            notification_toggle.set_position((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            for i in range(4):
                color_pickers[i].set_position((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + (i + 1) * 100))
            width_input.set_position((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
            height_input.set_position((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            width_unit.set_position((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            height_unit.set_position((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            submit_button.set_position((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100))
            plant_input.set_position((SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2 - 100))
            add_button.set_position((SCREEN_WIDTH // 4 - 100, SCREEN_HEIGHT // 2))

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if page == 0:
                for i in range(6):
                    button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
                    button_y = SCREEN_HEIGHT // 2 - (3 - i) * (BUTTON_HEIGHT + BUTTON_MARGIN)
                    if (mouse_x > button_x - BUTTON_RADIUS and mouse_x < button_x + BUTTON_WIDTH + BUTTON_RADIUS and
                        mouse_y > button_y and mouse_y < button_y + BUTTON_HEIGHT):
                        page = i + 1
                        if page == 1:
                            width_input.enable()
                            height_input.enable()
                            width_unit.enable()
                            height_unit.enable()
                            submit_button.enable()
                        else:
                            width_input.disable()
                            height_input.disable()
                            width_unit.disable()
                            height_unit.disable()
                            submit_button.disable()
                        if page == 6:
                            theme_picker.enable()
                            notification_toggle.enable()
                            for i in range(4):
                                color_pickers[i].enable()
                        else:
                            theme_picker.disable()
                            notification_toggle.disable()
                            for i in range(4):
                                color_pickers[i].disable()
                        if page == 2:
                            disease_scan = random.choice(diseases)
                            disease_text = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100), (400, 200)), html_message=f"<b>{disease_scan}</b>: {disease_descriptions[disease_scan]}", manager=manager, window_title="Disease Test")
                            scan_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200), (200, 50)), text="SCAN", manager=manager)
                            scan_button.disable()
                            pygame.time.set_timer(pygame.USEREVENT, 5000) # wait for 5 seconds
                            for event in pygame.event.get():
                                if event.type == pygame.USEREVENT:
                                    scan_button.enable()
                                    disease_text.kill() # close the text box
                                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                                    if event.ui_element == scan_button:
                                        disease_scan = random.choice(diseases)
                                        disease_text = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100), (400, 200)), html_message=f"<b>{disease_scan}</b>: {disease_descriptions[disease_scan]}", manager=manager, window_title="Disease Test")
                                        scan_button.disable()
                                        pygame.time.set_timer(pygame.USEREVENT, 5000) # wait for 5 seconds

                        if page == 3:
                            moisture_scan = random.choice(moisture_levels)
                            moisture_text = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100), (400, 200)), html_message=f"<b>Moisture Level</b>: {moisture_scan}", manager=manager, window_title="Soil Moisture Test")
                            if moisture_scan in ["30% - 60%", "60% - 100%"]:
                                moisture_text.set_text(moisture_text.get_text() + "\nMoisture is good!")
                            scan_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200), (200, 50)), text="SCAN", manager=manager)
                            scan_button.disable()
                            pygame.time.set_timer(pygame.USEREVENT, 5000) # wait for 5 seconds
                            for event in pygame.event.get():
                                if event.type == pygame.USEREVENT:
                                    scan_button.enable()
                                    moisture_text.kill() # close the text box
                                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                                    if event.ui_element == scan_button:
                                        moisture_scan = random.choice(moisture_levels)
                                        moisture_text = pygame_gui.windows.UIMessageWindow(rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100), (400, 200)), html_message=f"<b>Moisture Level</b>: {moisture_scan}", manager=manager, window_title="Soil Moisture Test")
                                        if moisture_scan in ["30% - 60%", "60% - 100%"]:
                                            moisture_text.set_text(moisture_text.get_text() + "\nMoisture is good!")
                                        scan_button.disable()
                                        pygame.time.set_timer(pygame.USEREVENT, 5000) # wait for 5 seconds

                        if page == 4:
                            nutrient_scan = {}
                            for nutrient in nutrients:
                                nutrient_scan[nutrient] = random.randint(0, 100)
                            nutrient_text = pygame_gui.windows.UIMessageWindow(
                                rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100), (400, 200)),
                                html_message="<b>Soil Nutrient Test</b>", manager=manager, window_title="Soil Nutrient Test"
                            )
                            nutrient_table = pygame_gui.elements.UITable(
                                relative_rect=pygame.Rect((0, 50), (400, 150)), manager=manager, container=nutrient_text,
                                column_headings=["Nutrient", "Percentage"]
                            )
                            for nutrient, percentage in nutrient_scan.items():
                                nutrient_table.add_row([nutrient, f"{percentage}%"])
                            scan_button = pygame_gui.elements.UIButton(
                                relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 200), (200, 50)),
                                text="SCAN", manager=manager
                            )
                            scan_button.disable()
                            pygame.time.set_timer(pygame.USEREVENT, 5000)  # wait for 5 seconds
                            for event in pygame.event.get():
                                if event.type == pygame.USEREVENT:
                                    scan_button.enable()
                                    nutrient_text.kill()  # close the text box
                                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                                    if event.ui_element == scan_button:
                                        nutrient_scan = {}
                                        for nutrient in nutrients:
                                            nutrient_scan[nutrient] = random.randint(0, 100)
                                        nutrient_text = pygame_gui.windows.UIMessageWindow(
                                            rect=pygame.Rect((SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100), (400, 200)),
                                            html_message="<b>Soil Nutrient Test</b>", manager=manager, window_title="Soil Nutrient Test"
                                        )
                                        nutrient_table = pygame_gui.elements.UITable(
                                            relative_rect=pygame.Rect((0, 50), (400, 150)), manager=manager, container=nutrient_text,
                                            column_headings=["Nutrient", "Percentage"]
                                        )
                                        for nutrient, percentage in nutrient_scan.items():
                                            nutrient_table.add_row([nutrient, f"{percentage}%"])
                                        scan_button.disable()
                                        pygame.time.set_timer(pygame.USEREVENT, 5000)  # wait for 5 seconds

                        # Continue with other pages and event handling here...

                        pygame.display.flip()
                        clock.tick(60)

                        pygame.quit()
                                       
