import pygame
class ENEMY:
    def __init__(self, enemy_type, x = 0, y = 0):
        self.x = x
        self.y = y
        self.enemy_rect = pygame.Rect(0,0,0,0)
        self.last_time_moved = 0
        self.last_hit_by = None
        
        # Ice/Slow effect properties
        self.is_slowed = False
        self.slow_intensity = 0.0  # 0.0 = no slow, 1.0 = completely frozen
        self.slow_duration = 0.0  # Duration in seconds
        self.base_movement_speed = 0  # Will be set after match statement
        self.frozen_time_left = 0.0  # Remaining freeze time in seconds
        
        # Fire/Burn effect properties
        self.is_burning = False
        self.burn_stacks = []  # List of active burn effects [(damage_per_sec, duration_left), ...]
        self.last_burn_tick = 0  # Last time burn damage was applied
        self.first_burn_tick = True  # Flag to track if this is the first burn tick

        match enemy_type:
            case 1:
                self.health = 1
                self.damage = 1
                self.movement_speed = 1.5
                self.color = (255, 25, 25)
                self.kill_reward = 1
            case 2:
                self.health = 2
                self.damage = 3
                self.movement_speed = 1.5
                self.color = (255, 109, 25)
                self.kill_reward = 2
            case 3:
                self.health = 3
                self.damage = 3
                self.movement_speed = 2
                self.color = (255, 167, 25)
                self.kill_reward = 5
            case 4:
                self.health = 5
                self.damage = 5
                self.movement_speed = 2
                self.color = (255, 232, 25)
                self.kill_reward = 5
            case 5:
                self.health = 7
                self.damage = 5
                self.movement_speed = 3
                self.color = (213, 255, 25)
                self.kill_reward = 5
            case 6:
                self.health = 10
                self.damage = 5
                self.movement_speed = 2
                self.color = (144, 255, 25)
                self.kill_reward = 6
            case 7:
                self.health = 15
                self.damage = 10
                self.movement_speed = 4
                self.color = (33, 255, 25)
                self.kill_reward = 10
            case 8:
                self.health = 3
                self.damage = 5
                self.movement_speed = 8
                self.color = (25, 255, 98)
                self.kill_reward = 5
            case 9:
                self.health = 25
                self.damage = 10
                self.movement_speed = 2
                self.color = (25, 255, 171)
                self.kill_reward = 15
            case 10:
                self.health = 75
                self.damage = 10
                self.movement_speed = 3
                self.color = (25, 255, 232)
                self.kill_reward = 15
            case 11:
                self.health = 100
                self.damage = 10
                self.movement_speed = 2.5
                self.color = (25, 232, 255)
                self.kill_reward = 15
            case 12:
                self.health = 250
                self.damage = 20
                self.movement_speed = 2
                self.color = (25, 198, 255)
                self.kill_reward = 15
            case 13:
                self.health = 500
                self.damage = 20
                self.movement_speed = 2
                self.color = (25, 151, 255)
                self.kill_reward = 15
            case 14:
                self.health = 1000
                self.damage = 20
                self.movement_speed = 5
                self.color = (25, 106, 255)
                self.kill_reward = 15
            case 15:
                self.health = 1500
                self.damage = 10
                self.movement_speed = 3
                self.color = (121, 25, 255)
                self.kill_reward = 15
            case 16:
                self.health = 2500
                self.damage = 10
                self.movement_speed = 4
                self.color = (178, 25, 255)
                self.kill_reward = 15
            case 17:
                self.health = 3000
                self.damage = 10
                self.movement_speed = 2
                self.color = (244, 25, 255)
                self.kill_reward = 15
            case 18:
                self.health = 3500
                self.damage = 15
                self.movement_speed = 1
                self.color = (255, 25, 129)
                self.kill_reward = 15
            case 19:
                self.health = 4000
                self.damage = 15
                self.movement_speed = 2
                self.color = (0, 0, 0)
                self.kill_reward = 15
            case 20:
                self.health = 5000
                self.damage = 50
                self.movement_speed = 1
                self.color = (255, 255, 255)
                self.kill_reward = 100
        self.current_health = self.health
        # Store the original movement speed for slow calculations
        self.base_movement_speed = self.movement_speed

    def apply_slow_effect(self, slow_intensity, duration):
        """Apply a slow effect to the enemy. Higher intensity = more slowing."""
        if slow_intensity > self.slow_intensity:  # Only apply if stronger than current slow
            self.slow_intensity = min(slow_intensity, 0.95)  # Cap at 95% slow (never completely frozen)
            self.slow_duration = duration
            self.is_slowed = True
            self.frozen_time_left = duration
            # Update movement speed based on slow intensity
            self.movement_speed = self.base_movement_speed * (1.0 - self.slow_intensity)

    def update_slow_effect(self, delta_time):
        """Update slow effect over time. Call this each frame."""
        if self.is_slowed:
            self.frozen_time_left -= delta_time
            if self.frozen_time_left <= 0:
                # Slow effect has worn off
                self.is_slowed = False
                self.slow_intensity = 0.0
                self.slow_duration = 0.0
                self.frozen_time_left = 0.0
                self.movement_speed = self.base_movement_speed
            else:
                # Gradually reduce slow effect intensity as it wears off
                remaining_ratio = self.frozen_time_left / self.slow_duration
                current_intensity = self.slow_intensity * remaining_ratio
                self.movement_speed = self.base_movement_speed * (1.0 - current_intensity)

    def apply_burn_effect(self, burn_damage, duration, can_stack=True):
        """Apply a burn effect to the enemy. Multiple burns can stack if allowed."""
        if can_stack:
            # Add new burn stack
            self.burn_stacks.append([burn_damage, duration])
            self.is_burning = True
        else:
            # Replace existing burn if new one is stronger
            if not self.burn_stacks or burn_damage > max(stack[0] for stack in self.burn_stacks):
                self.burn_stacks = [[burn_damage, duration]]
                self.is_burning = True
        
        # Set the burn tick timer to current time (first tick will be delayed by 0.3 seconds)
        if self.last_burn_tick == 0:
            self.last_burn_tick = pygame.time.get_ticks()
            self.first_burn_tick = True

    def update_burn_effect(self, delta_time, speed_multiplier=1.0):
        """Update burn effects over time and apply damage. Call this each frame."""
        if self.is_burning and self.burn_stacks:
            current_time = pygame.time.get_ticks()
            
            # Determine the tick interval: 300ms for first tick, 1000ms for subsequent ticks
            # Scale the interval by speed multiplier (faster ticks in 2x mode)
            base_first_interval = 300
            base_normal_interval = 1000
            tick_interval = (base_first_interval if self.first_burn_tick else base_normal_interval) / speed_multiplier
            
            # Apply burn damage based on the interval
            if current_time - self.last_burn_tick >= tick_interval:
                total_burn_damage = 0
                
                # Process all burn stacks
                stacks_to_remove = []
                for i, stack in enumerate(self.burn_stacks):
                    burn_damage, duration_left = stack
                    total_burn_damage += burn_damage
                    
                    # Reduce duration: 0.3 seconds for first tick, 1.0 second for subsequent ticks
                    # Scale duration reduction by speed multiplier (faster burn consumption in 2x mode)
                    base_duration_reduction = 0.3 if self.first_burn_tick else 1.0
                    duration_reduction = base_duration_reduction * speed_multiplier
                    stack[1] -= duration_reduction
                    
                    # Mark for removal if expired
                    if stack[1] <= 0:
                        stacks_to_remove.append(i)
                
                # Remove expired stacks (in reverse order to maintain indices)
                for i in reversed(stacks_to_remove):
                    self.burn_stacks.pop(i)
                
                # Apply total burn damage
                if total_burn_damage > 0:
                    self.current_health -= total_burn_damage
                
                # Update burning status
                if not self.burn_stacks:
                    self.is_burning = False
                
                # Update the flag after first tick
                if self.first_burn_tick:
                    self.first_burn_tick = False
                
                self.last_burn_tick = current_time
                
                # Return True if enemy died from burn damage
                return self.current_health <= 0
        
        return False  # No burn damage applied or enemy still alive

    def get_visual_effect_color(self):
        """Return a color tint for visual feedback on effects."""
        base_color = self.color
        
        # Apply burning effect (orange/red tint)
        if self.is_burning:
            fire_orange = (255, 100, 0)  # Bright orange color
            burn_intensity = min(len(self.burn_stacks) * 0.3, 0.7)  # Intensity based on number of burn stacks
            
            # Blend original color with fire orange
            r = int(base_color[0] * (1 - burn_intensity) + fire_orange[0] * burn_intensity)
            g = int(base_color[1] * (1 - burn_intensity) + fire_orange[1] * burn_intensity)
            b = int(base_color[2] * (1 - burn_intensity) + fire_orange[2] * burn_intensity)
            base_color = (r, g, b)
        
        # Apply slowing effect (ice blue tint) - this can combine with burning for mixed colors
        if self.is_slowed:
            ice_blue = (173, 216, 230)  # Light blue color
            slow_intensity = self.slow_intensity * 0.5  # Make ice effect less dominant
            
            # Blend current color (potentially already fire-tinted) with ice blue
            r = int(base_color[0] * (1 - slow_intensity) + ice_blue[0] * slow_intensity)
            g = int(base_color[1] * (1 - slow_intensity) + ice_blue[1] * slow_intensity)
            b = int(base_color[2] * (1 - slow_intensity) + ice_blue[2] * slow_intensity)
            base_color = (r, g, b)
        
        return base_color

def enemy_list_data():
    return {
        "0":{
            "0":{
                "ENEMY_TYPE":1,
                "AMOUNT": 15,
            },
        },
        "1":{
            "0":{
                "ENEMY_TYPE":1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "2": {
            "0": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 5,
            },
            "1": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 5,
            },
        },
        "3": {
            "0": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 5,
            },
            "2": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 20,
            },
        },
        "4": {
            "0": {
                "ENEMY_TYPE": 4,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 3,
            },
            "3": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 15,
            },
        },
        "5": {
            "0": {
                "ENEMY_TYPE": 4,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 4,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 20,
            },
        },
        "6": {
            "0": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 30,
            },
            "1": {
                "ENEMY_TYPE": 3,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 50,
            },
        },
        "7": {
            "0": {
                "ENEMY_TYPE": 6,
                "AMOUNT": 30,
            },
            "1": {
                "ENEMY_TYPE": 5,
                "AMOUNT": 40,
            },
            "2": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 20,
            },
        },
        "8": {
            "0": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 30,
            },
            "1": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 40,
            },
            "2": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 6,
                "AMOUNT": 30,
            },

        },
        "9": {
            "0": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 7,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 30,
            },
        },
        "10": {
            "0": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 10,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 30,
            },
        },
        "11": {
            "0": {
                "ENEMY_TYPE": 8,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 100,
            },
            "3": {
                "ENEMY_TYPE": 11,
                "AMOUNT": 10,
            },
        },
        "12": {
            "0": {
                "ENEMY_TYPE": 10,
                "AMOUNT": 50,
            },
            "1": {
                "ENEMY_TYPE": 9,
                "AMOUNT": 10,
            },
            "2": {
                "ENEMY_TYPE": 11,
                "AMOUNT": 20,
            },
            "3": {
                "ENEMY_TYPE": 12,
                "AMOUNT": 2,
            },
        },
        "13": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "14": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "15": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "16": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "17": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "18": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "19": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
        "20": {
            "0": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 10,
            },
            "1": {
                "ENEMY_TYPE": 2,
                "AMOUNT": 20,
            },
            "2": {
                "ENEMY_TYPE": 1,
                "AMOUNT": 5,
            },
        },
    }

def generate_list_from_data(wave_num):
    wave_list = []
    enemy_data = enemy_list_data()
    for wave_num_key, enemy_list in enemy_data.items():
        if str(wave_num) == wave_num_key:
            for enemy_batch_num, enemy_obj in enemy_list.items():
                temp_enemy_list = []
                for i in range(0, enemy_obj["AMOUNT"]):
                    temp_enemy_list.append(ENEMY(int(enemy_obj["ENEMY_TYPE"]),0,0,))
                wave_list.append(temp_enemy_list)
            break

    return wave_list