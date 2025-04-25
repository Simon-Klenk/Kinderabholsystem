# Copyright (c) 2025 Simon Klenk
# This software is licensed under the MIT License.
# See the LICENSE file in the project directory for the full license text.

from machine import Pin, I2C
import time
import framebuf
import uasyncio

class DisplayInitializationError(Exception):
    """Custom exception for display initialization errors."""
    pass

class FramebufferScalingError(Exception):
    """Custom exception for framebuffer scaling errors."""
    pass

class DisplayOperationError(Exception):
    """Custom exception for display operation errors."""
    pass

class Display:
    """
    A class for managing an SH1106 OLED display using I2C communication.

    Attributes:
        width (int): The width of the display in pixels.
        height (int): The height of the display in pixels.
        show_text (bool): Flag indicating whether text should be displayed.
        new_text (bool): Flag to indicate if a new text update is required.
        text (str): The text to display on the screen.
        i2c (I2C): The I2C communication object for the display.
        display (object): The SH1106 display object.
    
    Methods:
        scale_framebuf(fb_source, width_source, height_source, width_dest, height_dest):
            Scales a source framebuffer to the target dimensions.
        print_oled():
            Displays text on the OLED, with scaling and optional scrolling.
    """
    def __init__(self, show_text, new_text, text, width=128, height=64, sda_pin=16, scl_pin=17, rotate=180):
        """
        Initializes the Display object and sets up the SH1106 OLED display.

        Args:
            show_text (bool): Initial state for displaying text.
            new_text (bool): Initial state for updating the text.
            text (str): The text to display.
            width (int, optional): Display width in pixels. Defaults to 128.
            height (int, optional): Display height in pixels. Defaults to 64.
            sda_pin (int, optional): Pin number for the I2C SDA line. Defaults to 16.
            scl_pin (int, optional): Pin number for the I2C SCL line. Defaults to 17.
            rotate (int, optional): Display rotation angle. Defaults to 180.

        Raises:
            DisplayInitializationError: If there is an error initializing the display.
        """
        self.width = width
        self.height = height
        self.show_text = show_text
        self.new_text = new_text
        self.text = text
        try:
            import sh1106
            self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
            self.display = sh1106.SH1106_I2C(self.width, self.height, self.i2c, rotate=rotate)
            self.display.fill(0)
            self.display.show()
            self.display.poweroff()
        except Exception as e:
            raise DisplayInitializationError(f"Error initializing the display: {e}")

    def scale_framebuf(self, fb_source, width_source, height_source, width_dest, height_dest):
        """
        Scales a source framebuffer to a destination size.

        Args:
            fb_source (FrameBuffer): The source framebuffer.
            width_source (int): The width of the source framebuffer.
            height_source (int): The height of the source framebuffer.
            width_dest (int): The width of the destination framebuffer.
            height_dest (int): The height of the destination framebuffer.

        Returns:
            FrameBuffer: The scaled framebuffer.

        Raises:
            FramebufferScalingError: If there is an error during scaling.
        """
        try:
            fb_dest = framebuf.FrameBuffer(bytearray(width_dest * height_dest // 8), width_dest, height_dest, framebuf.MONO_HLSB)  
            x_ratio = width_source / width_dest
            y_ratio = height_source / height_dest

            for y in range(height_dest):
                for x in range(width_dest):
                    px = int(x * x_ratio)
                    py = int(y * y_ratio)
                    color = fb_source.pixel(px, py)
                    fb_dest.pixel(x, y, color)

            return fb_dest
        except Exception as e:
            raise FramebufferScalingError(f"Error while scaling framebuffer: {e}")
    
    async def print_oled(self):
        """
        Displays text on the OLED screen. If the text exceeds the display width, it will scroll.

        This method handles scaling, optional scrolling for longer text, and display updates.

        Raises:
            DisplayOperationError: If there is an error during display operations.
        """
        while True:
            while self.show_text:
                if not self.display:
                    raise DisplayOperationError("Display was not properly initialized!")
                self.display.poweron()
                try:
                    # Scaling factors for text dimensions
                    letter_scale_factor_width = 2.25
                    letter_scale_factor_height = 8

                    # Calculate dimensions and pad text if needed
                    width_length_old_pixel = len(self.text) * letter_scale_factor_width * 8
                    new_text = self.text
                    padding_length = 8 - (len(new_text) % 8)
                    if len(new_text) % 8 != 0:
                        new_text += " " * padding_length

                    text_length = len(new_text)
                    text_width_pixel = text_length * 8
                    scaled_text_width_pixel = int(text_width_pixel * letter_scale_factor_width)
                    scaled_text_height_pixel = int(8 * letter_scale_factor_height)
                    
                    # Create original and scaled framebuffers
                    fb_original = framebuf.FrameBuffer(bytearray(text_width_pixel), text_width_pixel, 8, framebuf.MONO_HLSB)
                    fb_original.text(new_text, 0, 0, 1)
                    fb_scaled = self.scale_framebuf(fb_original, text_width_pixel, 8, scaled_text_width_pixel, scaled_text_height_pixel)
                    
                    while not self.new_text:
                        if width_length_old_pixel > self.width - 10:
                            # Scroll text if it exceeds display width
                            for x_offset in range(0, scaled_text_width_pixel - 95, 2):
                                if self.new_text:
                                    break
                                self.display.blit(fb_scaled, -x_offset, 0)
                                self.display.show()
                                if x_offset == 0:
                                    await uasyncio.sleep(0.8)
                                await uasyncio.sleep(0.01)
                        else:
                            # Display static text if it fits
                            self.display.blit(fb_scaled, 0, 0)
                            self.display.show()
                            await uasyncio.sleep(1)
    
                    self.new_text = False
                except Exception as e:
                    self.display.fill(0)
                    self.display.show()
                    self.display.poweroff()
                    raise DisplayOperationError(f"Error displaying text: {e}")
        
            await uasyncio.sleep(1)
            self.display.fill(0)
            self.display.show()
            self.display.poweroff()
        await uasyncio.sleep(1)
