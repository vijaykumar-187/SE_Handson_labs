import os
import pygame
from .player import Player
from .obstacle import Obstacle

# Game Engine

WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 40

        # Difficulty settings from Task 3
        self.difficulties = {
            "Easy": {
                "speed": 5,
                "spawn_interval": 85,
            },
            "Medium": {
                "speed": 6,
                "spawn_interval": 70,
            },
            "Hard": {
                "speed": 8,
                "spawn_interval": 55,
            },
        }

        # Default difficulty is Medium
        self.selected_difficulty = "Medium"

        # Task 1: speed settings
        self.speed = self.difficulties["Medium"]["speed"]
        self.speed_increase_per_frame = 0.003
        self.max_speed = 12

        self.player = Player(80, self.ground_y)

        # Default Medium spawn interval
        self.spawn_interval = self.difficulties["Medium"]["spawn_interval"]
        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        # Task 2 / Task 3 game states
        self.game_over = False
        self.show_difficulty_menu = False

        # Task 4: Sound effects are optional.
        # The game continues normally if audio is unavailable.
        self.sound_enabled = False
        self.jump_sound = None
        self.score_sound = None
        self.game_over_sound = None
        self._load_sounds()

    def _load_sounds(self):
        """Safely initialize the mixer and load Task 4 sounds."""
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            sounds_dir = os.path.join(
                os.path.dirname(__file__),
                "sounds",
            )

            self.jump_sound = pygame.mixer.Sound(
                os.path.join(sounds_dir, "jump.wav")
            )

            self.score_sound = pygame.mixer.Sound(
                os.path.join(sounds_dir, "score.wav")
            )

            self.game_over_sound = pygame.mixer.Sound(
                os.path.join(sounds_dir, "game_over.wav")
            )

            self.sound_enabled = True

        except (pygame.error, OSError):
            # Audio is optional.
            # The game must continue if audio initialization/loading fails.
            self.sound_enabled = False
            self.jump_sound = None
            self.score_sound = None
            self.game_over_sound = None

    def _play_sound(self, sound):
        """Play a sound safely when audio is available."""
        if not self.sound_enabled or sound is None:
            return

        try:
            sound.play()
        except pygame.error:
            # Never allow an audio failure to stop the game.
            pass

    def handle_event(self, event):
        # Handle closing the window normally.
        if event.type == pygame.QUIT:
            return

        # Task 3: Difficulty menu after Game Over.
        if self.game_over and self.show_difficulty_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.start_new_game("Easy")

                elif event.key == pygame.K_2:
                    self.start_new_game("Medium")

                elif event.key == pygame.K_3:
                    self.start_new_game("Hard")

                elif event.key in (
                    pygame.K_4,
                    pygame.K_ESCAPE,
                ):
                    pygame.event.post(
                        pygame.event.Event(pygame.QUIT)
                    )

            return

        # Normal gameplay input.
        if self.game_over:
            return

        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w,
        ):
            # Task 4: Jump sound.
            # Only play it when the player can actually jump.
            if self.player.on_ground:
                self.player.jump()
                self._play_sound(self.jump_sound)

    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    def start_new_game(self, difficulty):
        """Start a completely fresh game using the selected difficulty."""

        self.selected_difficulty = difficulty

        settings = self.difficulties[difficulty]

        # Reset player completely.
        self.player = Player(
            80,
            self.ground_y,
        )

        # Apply selected difficulty.
        self.speed = settings["speed"]
        self.spawn_interval = settings["spawn_interval"]

        # Reset game state.
        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0

        # Reset Game Over/menu state.
        self.game_over = False
        self.show_difficulty_menu = False

    def update(self):
        # Stop updating the game after Game Over.
        if self.game_over:
            return

        # Task 1:
        # Increase speed while respecting the maximum speed.
        self.speed = min(
            self.speed + self.speed_increase_per_frame,
            self.max_speed,
        )

        self.player.update()

        # Spawn obstacles according to the selected difficulty.
        self._spawn_timer += 1

        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0

            self.obstacles.append(
                Obstacle(
                    self.width,
                    self.ground_y,
                    self.speed,
                )
            )

        # Move obstacles and perform swept collision detection.
        for obstacle in self.obstacles:
            previous_x = obstacle.x

            obstacle.move()
            obstacle.speed = self.speed

            # Task 1:
            # Check the complete horizontal path travelled
            # by the obstacle during this frame.
            player_rect = self.player.rect()

            left = min(
                previous_x,
                obstacle.x,
            )

            right = max(
                previous_x + obstacle.width,
                obstacle.x + obstacle.width,
            )

            swept_rect = pygame.Rect(
                left,
                obstacle.y,
                right - left,
                obstacle.height,
            )

            if swept_rect.colliderect(player_rect):
                # Task 4: Game-over sound.
                # This is triggered exactly when Game Over begins.
                self._play_sound(self.game_over_sound)

                self.game_over = True
                self.show_difficulty_menu = True
                return

        # Existing scoring logic.
        for obstacle in self.obstacles:
            if (
                not obstacle.scored
                and obstacle.x + obstacle.width < self.player.x
            ):
                obstacle.scored = True
                self.score += 1

                # Task 4: Scoring sound.
                # This is triggered whenever +1 score is awarded.
                self._play_sound(self.score_sound)

        # Remove obstacles that have moved off-screen.
        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if not obstacle.off_screen()
        ]

        self.distance += self.speed

    def render(self, screen):
        # Draw ground.
        pygame.draw.line(
            screen,
            BROWN,
            (0, self.ground_y),
            (self.width, self.ground_y),
            4,
        )

        # Draw player.
        pygame.draw.rect(
            screen,
            WHITE,
            self.player.rect(),
        )

        # Draw obstacles.
        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                obstacle.rect(),
            )

        # Draw current score.
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            (0, 0, 0),
        )

        screen.blit(
            score_text,
            (10, 10),
        )

        # Task 2 + Task 3:
        # Game Over and difficulty selection screen.
        if self.game_over:
            # Dark transparent overlay.
            overlay = pygame.Surface(
                (self.width, self.height)
            )

            overlay.set_alpha(190)
            overlay.fill((0, 0, 0))

            screen.blit(
                overlay,
                (0, 0),
            )

            # Fonts.
            game_over_font = pygame.font.SysFont(
                "Arial",
                52,
                bold=True,
            )

            final_score_font = pygame.font.SysFont(
                "Arial",
                32,
                bold=True,
            )

            menu_font = pygame.font.SysFont(
                "Arial",
                25,
            )

            instruction_font = pygame.font.SysFont(
                "Arial",
                20,
            )

            # GAME OVER.
            game_over_text = game_over_font.render(
                "GAME OVER",
                True,
                WHITE,
            )

            game_over_rect = game_over_text.get_rect(
                center=(
                    self.width // 2,
                    70,
                )
            )

            screen.blit(
                game_over_text,
                game_over_rect,
            )

            # Final score.
            final_score_text = final_score_font.render(
                f"Final Score: {self.score}",
                True,
                WHITE,
            )

            final_score_rect = final_score_text.get_rect(
                center=(
                    self.width // 2,
                    125,
                )
            )

            screen.blit(
                final_score_text,
                final_score_rect,
            )

            # Difficulty menu title.
            menu_title = menu_font.render(
                "Choose Difficulty",
                True,
                WHITE,
            )

            menu_title_rect = menu_title.get_rect(
                center=(
                    self.width // 2,
                    175,
                )
            )

            screen.blit(
                menu_title,
                menu_title_rect,
            )

            # Easy.
            easy_text = menu_font.render(
                "1 - Easy",
                True,
                WHITE,
            )

            easy_rect = easy_text.get_rect(
                center=(
                    self.width // 2,
                    215,
                )
            )

            screen.blit(
                easy_text,
                easy_rect,
            )

            # Medium.
            medium_text = menu_font.render(
                "2 - Medium",
                True,
                WHITE,
            )

            medium_rect = medium_text.get_rect(
                center=(
                    self.width // 2,
                    250,
                )
            )

            screen.blit(
                medium_text,
                medium_rect,
            )

            # Hard.
            hard_text = menu_font.render(
                "3 - Hard",
                True,
                WHITE,
            )

            hard_rect = hard_text.get_rect(
                center=(
                    self.width // 2,
                    285,
                )
            )

            screen.blit(
                hard_text,
                hard_rect,
            )

            # Exit.
            exit_text = menu_font.render(
                "4 - Exit",
                True,
                WHITE,
            )

            exit_rect = exit_text.get_rect(
                center=(
                    self.width // 2,
                    320,
                )
            )

            screen.blit(
                exit_text,
                exit_rect,
            )

            # Keyboard instruction.
            instruction_text = instruction_font.render(
                "Press 1, 2, 3, or 4",
                True,
                WHITE,
            )

            instruction_rect = instruction_text.get_rect(
                center=(
                    self.width // 2,
                    365,
                )
            )

            screen.blit(
                instruction_text,
                instruction_rect,
            )