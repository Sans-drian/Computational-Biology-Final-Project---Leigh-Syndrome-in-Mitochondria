import pygame
import sys
import random
import time

# Constants
MAINWIDTH, MAINHEIGHT = 1300, 600
SIMWIDTH, SIMHEIGHT = 1000, 600
FPS = 45  # Lower FPS for a slower simulation (default: 45)
MITOCHONDRIA_RADIUS = 5
MITOCHONDRIA_COUNT = {
    'normal': 1000,  # Number of normal mitochondria cells
    'leigh_syndrome': 0  # Initial number of mitochondria cells with Leigh Syndrome
}
MITOCHONDRIA_COLOR = (34, 177, 76)  # Green color
LEIGH_SYNDROME_COLOR = (255, 0, 0)  # Red color
BACKGROUND_COLOR = (255, 255, 255)
WARNING_COLOR = (255, 0, 0)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 24
OXIDATIVE_STRESS_THRESHOLD = 70  # Adjust this threshold as needed
INFECTION_RATE = 0.005  # Adjust the infection rate (lower value for slower spread)
MAX_OXIDATIVE_STRESS = 95  # Adjust the maximum oxidative stress for stopping condition

# Classes
class MitochondriaCell(pygame.sprite.Sprite):
    def __init__(self, x, y, syndrome=False):
        super().__init__()
        self.syndrome = syndrome
        if self.syndrome:
            self.image = pygame.Surface((MITOCHONDRIA_RADIUS * 2, MITOCHONDRIA_RADIUS * 2), pygame.SRCALPHA)
            self.image.fill(LEIGH_SYNDROME_COLOR)
        else:
            self.image = pygame.Surface((MITOCHONDRIA_RADIUS * 2, MITOCHONDRIA_RADIUS * 2), pygame.SRCALPHA)
            self.image.fill(MITOCHONDRIA_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.energy_production = 100  # Arbitrary initial energy production level
        self.antioxidant_capacity = 100  # Arbitrary initial antioxidant capacity
        self.oxidative_stress = 0  # Arbitrary initial oxidative stress level

    def mutate(self):
        # Implement mutation here
        mutation_rate = 0.1  # Adjust the mutation rate as needed

        if random.random() < mutation_rate:
            self.energy_production += random.randint(-10, 10)
            self.antioxidant_capacity += random.randint(-5, 5)

            # Ensure values are within reasonable bounds
            self.energy_production = max(0, self.energy_production)
            self.antioxidant_capacity = max(0, self.antioxidant_capacity)

    def update(self):
        self.mutate()  # Apply mutation before updating other properties

        if not self.syndrome:
            # Introduce Leigh Syndrome based on the infection rate
            if random.random() < INFECTION_RATE:
                self.syndrome = True
                self.image.fill(LEIGH_SYNDROME_COLOR)
        else:
            # Implement Leigh Syndrome effects on mitochondrial behavior
            # For example, decrease energy production, increase oxidative stress, etc.
            energy_reduction = random.randint(0, min(self.energy_production, 2))
            self.energy_production -= energy_reduction
            self.oxidative_stress += energy_reduction  # Using energy reduction as a proxy for increased oxidative stress

            # Adjust antioxidant capacity in response to oxidative stress
            self.antioxidant_capacity -= random.randint(0, 5)
            self.antioxidant_capacity = max(0, self.antioxidant_capacity)

            # Calculate net oxidative stress considering antioxidant capacity
            net_oxidative_stress = max(0, self.oxidative_stress - self.antioxidant_capacity)

            # Adjust the color based on net oxidative stress
            red_component = min(255, 2 * net_oxidative_stress)
            self.image.fill((255, red_component, red_component))
        
        # Add movement to the cells
        self.rect.x += random.randint(-1, 1)
        self.rect.y += random.randint(-1, 1)

        # Keep the cells within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, MAINWIDTH - MITOCHONDRIA_RADIUS * 2))
        self.rect.y = max(0, min(self.rect.y, MAINHEIGHT - MITOCHONDRIA_RADIUS * 2))

def calculate_average_values(mitochondria_cells):
    total_oxidative_stress = sum(max(0, cell.oxidative_stress - cell.antioxidant_capacity) for cell in mitochondria_cells)
    
    if not mitochondria_cells:
        return 100, 0  # Default values when there are no cells
    
    average_energy = sum(cell.energy_production for cell in mitochondria_cells) / len(mitochondria_cells)
    average_oxidative_stress = total_oxidative_stress / len(mitochondria_cells)

    return average_energy, average_oxidative_stress

def draw_legends(screen, font, average_energy, average_oxidative_stress):
    # Draw legends for average energy production and oxidative stress
    energy_text = font.render(f'Average Energy Production: {average_energy:.2f}', True, FONT_COLOR)
    oxidative_stress_text = font.render(f'Average Oxidative Stress: {average_oxidative_stress:.2f}', True, FONT_COLOR)

    screen.blit(energy_text, (10, 10))
    screen.blit(oxidative_stress_text, (10, 40))

def draw_bars(screen, average_energy, average_oxidative_stress):
    # Draw bars to represent average energy production and oxidative stress
    energy_bar_length = min(average_energy, 100)
    oxidative_stress_bar_length = min(average_oxidative_stress, 100)

    pygame.draw.rect(screen, MITOCHONDRIA_COLOR, (10, 70, energy_bar_length * 3, 20))
    pygame.draw.rect(screen, LEIGH_SYNDROME_COLOR, (10, 100, oxidative_stress_bar_length * 3, 20))

def draw_warning(screen, font, average_oxidative_stress):
    # Draw a warning message when oxidative stress exceeds the threshold
    if average_oxidative_stress > OXIDATIVE_STRESS_THRESHOLD:
        warning_text = font.render('Warning: High Oxidative Stress!', True, WARNING_COLOR)
        screen.blit(warning_text, (MAINWIDTH // 2 - 150, MAINHEIGHT - 50))

def draw_endText(screen, font, simulation_running):
    # Draw the info text when the simulation has stopped running
    if simulation_running == False:
        stopSimText = font.render("Simulation stopped due", True, FONT_COLOR)
        screen.blit(stopSimText, (1010, 30))
        stopSimText2 = font.render("to high oxidative stress.", True, FONT_COLOR)
        screen.blit(stopSimText2, (1010, 60))  

        endWarning = font.render("Program will go back to", True, FONT_COLOR)
        screen.blit(endWarning, (1010, 500)) 
        endWarning2 = font.render("the main menu in 10 sec.", True, FONT_COLOR)
        screen.blit(endWarning2, (1010, 550))  


def display_aboutSyndrome_screen(screen):
    # Drawing the About Leigh Syndrome info screen
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)
    about_running = True

    # Render text
    while about_running:
        screen.fill(BACKGROUND_COLOR)
        
        about_text = [
            "About Leigh Syndrome:",
            "",
            "Leigh syndrome is a severe neurological disorder",
            "that typically appears in infancy or early childhood.",
            "It's characterized by progressive loss of mental",
            "and movement abilities, caused by a dysfunction",
            "in mitochondrial energy production.",
            "",
            "There is currently no cure for Leigh syndrome.",
            "",
            "Press 'Back' to return to the main menu."
        ]

        for i, line in enumerate(about_text):
            line_rendered = font.render(line, True, FONT_COLOR)
            screen.blit(line_rendered, (50, 50 + i * 30))

        # Back Button
        back_button = pygame.Rect(50, 520, 100, 50)
        pygame.draw.rect(screen, (230, 69, 69), back_button, border_radius=4)
        back_text = font.render("Back", True, FONT_COLOR)
        screen.blit(back_text, (70, 533))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    return

        pygame.display.flip()

def display_aboutSim_screen(screen):
    # Drawing the About Simulation info screen
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)
    about_running = True

    # Render text
    while about_running:
        screen.fill(BACKGROUND_COLOR)
        
        about_text = [
            "About The Simulation:",
            "",
            "The simulation initializes normal and Leigh syndrome, ",
            "representing individual cells with properties such as ",
            "energy production and syndrome status, undergoing random ",
            "mutations and possible infection. The simulation continuously",
            "updates the state of mitochondria, terminating if energy",
            "production becomes too low or oxidative stress too high.",
            "Visuals include mitochondria, legends, bars, counts, and warnings,",
            "with the latter triggered if the average oxidative stress surpasses",
            "a threshold. User interaction involves terminating the simulation",
            "by closing the window or pressing 'Q'.",
            "",
            "",
            "Press 'Back' to return to the main menu."
        ]

        for i, line in enumerate(about_text):
            line_rendered = font.render(line, True, FONT_COLOR)
            screen.blit(line_rendered, (50, 50 + i * 30))

        # Back button
        back_button = pygame.Rect(50, 520, 100, 50)
        pygame.draw.rect(screen, (230, 69, 69), back_button, border_radius=4)
        back_text = font.render("Back", True, FONT_COLOR)
        screen.blit(back_text, (70, 533))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_pos):
                    main_menu(screen)

        pygame.display.flip()


def simulation_screen(screen):
    # Drawing the main simulation screen
    pygame.init()
    screen = pygame.display.set_mode((MAINWIDTH, MAINHEIGHT))
    pygame.display.set_caption("Mitochondria Simulation")
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)

    all_sprites = pygame.sprite.Group()
    
    # Create normal mitochondria cells
    for _ in range(MITOCHONDRIA_COUNT['normal']):
        cell = MitochondriaCell(random.randint(0, SIMWIDTH), random.randint(0, SIMHEIGHT))
        all_sprites.add(cell)
    
    # Create mitochondria cells with Leigh Syndrome
    for _ in range(MITOCHONDRIA_COUNT['leigh_syndrome']):
        cell = MitochondriaCell(random.randint(0, SIMWIDTH), random.randint(0, SIMHEIGHT), syndrome=True)
        all_sprites.add(cell)

    clock = pygame.time.Clock()
    simulation_running = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()  

        if not simulation_running:
            time.sleep(10)
            break  # Skip updating the simulation if it's not running

        all_sprites.update()

        # Check if oxidative stress exceeds the threshold for warning
        average_energy, average_oxidative_stress = calculate_average_values(all_sprites.sprites())
        warning_displayed = average_oxidative_stress > OXIDATIVE_STRESS_THRESHOLD

        # Print info in terminal
        if average_energy <= 0:
            print("Simulation stopped due to low energy production.")
            simulation_running = False

        if average_oxidative_stress >= MAX_OXIDATIVE_STRESS:
            print("Simulation stopped due to high oxidative stress.")
            simulation_running = False

        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)

        # Render texts
        draw_legends(screen, font, average_energy, average_oxidative_stress)
        draw_bars(screen, average_energy, average_oxidative_stress)

        draw_warning(screen, font, average_oxidative_stress)

        draw_endText(screen, font, simulation_running)

        pygame.display.flip()
        clock.tick(FPS)


def main_menu(screen):
    # Draw the main menu screen
    font = pygame.font.Font(pygame.font.get_default_font(), FONT_SIZE)
    menu_running = True

    while menu_running:
        screen.fill(BACKGROUND_COLOR)
        
        # Render buttons
        title_text = font.render("Leigh Syndrome Simulation", True, FONT_COLOR)
        screen.blit(title_text, (500, 80))

        simulation_button = pygame.Rect(585, 150, 150, 50)
        pygame.draw.rect(screen, (38, 199, 81), simulation_button, border_radius=4)
        simulation_text = font.render("Simulation", True, FONT_COLOR)
        screen.blit(simulation_text, (595, 160))

        about_leigh_syndrome_button = pygame.Rect(510, 240, 300, 50)
        pygame.draw.rect(screen, (201, 105, 224), about_leigh_syndrome_button, border_radius=4)
        about_leigh_syndrome_text = font.render("About Leigh Syndrome", True, FONT_COLOR)
        screen.blit(about_leigh_syndrome_text, (522, 253))

        about_simulation_button = pygame.Rect(535, 330, 250, 50)
        pygame.draw.rect(screen, (201, 105, 224), about_simulation_button, border_radius=4)
        about_simulation_text = font.render("About Simulation", True, FONT_COLOR)
        screen.blit(about_simulation_text, (559, 344))

        exit_button = pygame.Rect(610, 430, 100, 50)
        pygame.draw.rect(screen, (230, 69, 69), exit_button, border_radius=4)
        exit_text = font.render("Exit", True, FONT_COLOR)
        screen.blit(exit_text, (635, 443))

        # Button press handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if about_leigh_syndrome_button.collidepoint(mouse_pos):
                    display_aboutSyndrome_screen(screen)

                elif about_simulation_button.collidepoint(mouse_pos):
                    display_aboutSim_screen(screen)

                elif simulation_button.collidepoint(mouse_pos):
                    simulation_screen(screen)
                    
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


def main():
    # Main Function
    pygame.init()
    screen = pygame.display.set_mode((MAINWIDTH, MAINHEIGHT))
    pygame.display.set_caption("Mitochondria Simulation by Avariq, Sandrian, and Carmen")

    main_menu(screen)  # Display the main menu initially

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()