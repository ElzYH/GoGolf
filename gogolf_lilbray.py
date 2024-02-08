import pygame
import os
import pygame_textinput
current_directory = os.getcwd()

class Text:
    def __init__(self):
        """Creates and display text with differnt fonts and sizes"""
        self.__text = ""
        self.__colour = ""
        self.__font = None
        self.__x = -1
        self.__y = -1

    def set_text(self, value):
        self.__text = value

    def set_colour(self, value):
        self.__colour = value

    def set_font(self, value, size):
        self.__font = pygame.freetype.Font(value, size)

    def set_x(self, value):
        self.__x = value

    def set_y(self, value):
        self.__y = value

    def set_font(self, font, font_size):
        self.__font = pygame.freetype.Font(os.path.join(current_directory,font), font_size)

    def set_all(self , text, colour, font, font_size, x, y):
        self.set_colour(colour)
        self.set_text(text)
        self.set_font(font, font_size)
        self.set_x(x)
        self.set_y(y)

    def draw_text(self, screen):
        text_surface, rect = self.__font.render(self.__text, pygame.Color(self.__colour))
        screen.blit(text_surface, (self.__x, self.__y))




class Button():
    """Creates Buttons that change image when the user mouse postion is over the button"""
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.image_hi = self.brighten_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.hold = False

    def brighten_image(self):
        # Convert image to a copy
        image_copy = self.image.copy()
        brightness_factor = 1.5

        # Iterate through pixels
        for x in range(image_copy.get_width()):
            for y in range(image_copy.get_height()):
                # Get the color of the pixel
                colour = image_copy.get_at((x, y))

                # Brighten RGB channels while leaving alpha channel unchanged
                new_colour = (
                    min(int(colour.r * brightness_factor), 255),
                    min(int(colour.g * brightness_factor), 255),
                    min(int(colour.b * brightness_factor), 255),
                    colour.a
                )

                # Set the new color to the pixel
                image_copy.set_at((x, y), new_colour)

        return image_copy


    def draw(self, screen):
        """Returns action and changes self.clicked if the user press the mouse ontop of the image"""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.hold = True

        if pygame.mouse.get_pressed()[0] == 0 and self.hold:
            self.clicked = True
            action = True
            self.hold = False
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        if self.rect.collidepoint(pos):
            screen.blit(self.image_hi, (self.rect.x,self.rect.y))

        else:
            screen.blit(self.image, (self.rect.x,self.rect.y))

        return action


class Enter_Text:
    """Text that the user can type into and can be saved"""
    def __init__(self,x,y,font,font_size,anti,text_manger):
        self.font = pygame.font.SysFont(font,font_size)
        self.anti = anti
        self.cords = x, y
        self.textinput = pygame_textinput.TextInputVisualizer(manager=text_manger,font_object=self.font)
        self.textinput.antialias = self.anti
        self.name = ""

    def draw(self,events,screen,rect_x,rect_y,rect_w,rect_h):
        """Draws a box for the user to type in and to contrast with the background"""
        self.textinput.update(events)
        input_rect = pygame.Rect(rect_x,rect_y,rect_w,rect_h)
        colour = pygame.Color("#F5FEFD")
        pygame.draw.rect(screen,colour ,input_rect)
        screen.blit(self.textinput.surface, (self.cords))

    def enter(self,events):
        """If Enter button is clicked it would save the text input"""
        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            self.name = str(self.textinput.value)


    def access(self):
        """Returns the user username"""
        return self.name 

    def clear_text(self):
        """Clears the Current text"""
        self.name = ""
        self.textinput.value = ""


class queue:
  """Queue data structure"""
  def __init__(self, capacity):
    self.__capacity = capacity
    self.__array = [None]*capacity
    self.__fpointer = 0
    self.__rpointer = 0

  def enqueue(self,item):
    if self.__rpointer == self.__capacity:
      if self.__fpointer == 0:
        print("Queue is full")
        return
      else:
        for i in range(self.__fpointer,self.__rpointer):
          self.__array[i - self.__fpointer] = self.__array[i]
        self.__rpointer -= self.__fpointer
        self.__fpointer = 0
    self.__array[self.__rpointer] = item
    self.__rpointer += 1

  def dequeue(self):
    if self.__fpointer == self.__rpointer:
      print("Empty Queue")
    else:
      self.__fpointer += 1
      return self.__array[self.__fpointer - 1]



def merge_sort(list1):
  if len(list1) == 1:
    return list1
  left_list = list1[:len(list1)//2]
  right_list = list1[len(list1)//2:]
  left_list = merge_sort(left_list)
  right_list = merge_sort(right_list)
  results = []
  while len(left_list) > 0 and len(right_list) > 0:
    if left_list[0] < right_list[0]:
      results.append(left_list.pop(0))
    else:
      results.append(right_list.pop(0))
  results.extend(left_list)
  results.extend(right_list)
  return results 



class stack:
  def __init__(self,capactiy):
    self.__capacity = capactiy
    self.__array = [None]*capactiy
    self.__pointer = 0


  def push(self,item):
    if self.__pointer < self.__capacity:
      self.__array[self.__pointer] = item
      self.__pointer += 1
    else:
      print('stack overflow')

  def pop(self):
    if self.__pointer == 0:
      print('stack undeflow')
    else:
      self.__pointer -= 1
      return self.__array[self.__pointer]


  #Create a Superencipherment cipher (cipher that encrypted twice)
  #Change letters to ASCII to binary, apply xor, convert back to denary, ceaser cipher of one of 
  #5 keys (either 5, 28, 26, 66, 92)


def convert_binary(value, length):
    binary_password = ["" for i in range(length)]
    
    #changes it to binary
    for i in range(length):
        while value[i]:
            if value[i] % 2 == 0:
                binary_password[i] = "0" + binary_password[i]
            else:
                binary_password[i] = "1" + binary_password[i]
            value[i] = value[i] //2
    
    return binary_password


def xor_cipher(value, xor_key):
    encrypted_values = []

    for byte in value:
        encrypted_byte = ""
        for bit_index in range(len(byte)):
            # Perform XOR operation on each bit
            if byte[bit_index] == xor_key[bit_index]:
                encrypted_byte += "0"
                
            else:
                encrypted_byte += "1"
        encrypted_values.append(encrypted_byte)

    return encrypted_values



def binary_denary_converter(value):
    ascii_encrypted = []

    for byte in value:
        ascii_value = 0
        # Start with the highest power of 2
        power = len(byte) - 1
        for bit in byte:
            # For each bit in the byte, calculate its decimal value and add it to the total
            if bit == "1":
                ascii_value += 2 ** power
            power -= 1  # Move to the next lower power of 2
        ascii_encrypted.append(ascii_value)

    return ascii_encrypted


def ceaser_cipher(string, key):  
    second_level = []

    for value in string:
        decrypted_value = value - key
        if decrypted_value <= 0:
            temp = 1110000 + decrypted_value
        else:
            temp = decrypted_value
        second_level.append(chr(temp))
    return second_level


def xor_cipher(value, xor_key):
    encrypted_values = []

    for byte in value:
        encrypted_byte = ""
        for bit_index in range(len(byte)):
            # Perform XOR operation on each bit
            if byte[bit_index] == xor_key[bit_index]:
                encrypted_byte += "0"
                
            else:
                encrypted_byte += "1"
        encrypted_values.append(encrypted_byte)

    return encrypted_values

def xor_cipher_DE(value, xor_key):
    values = []
    for key in range(len(value)):
        values.append("".join(xor_cipher(value[key], xor_key[key])))
   
    return values



def encrypter(password):
    """Encrypts data using xor key and ceaser cipher """

    ascii_password = [ord(letter) for letter in password] #Changes it to ascii

    binary_password = convert_binary(ascii_password, len(ascii_password))

    xor_key = "10101011" #AB

    #Applys xor key to all binary values
    first_level =  xor_cipher(binary_password, xor_key)

    #converts binary to denary 
    ascii_encrypted = binary_denary_converter(first_level)


    key = -5 #Ceaser cipher key 

    #Applies Ceaser Cipher to xor encrypted ascii values
    second_level = ceaser_cipher(ascii_encrypted, key) 

    #Turns it back into a sting
    second_level = "".join(second_level)    

    return second_level

    




#encrypted password applied with xor from a plaintext that converted to binary of user
#typed password

#so only need xor version of password with xor with non xor version.

# def dencrypter(en_password, password):
#     #decrypt
#     xor_key_setter = "10101011"

#     password = [ord(letter) for letter in password]
#     password = convert_binary(password, len(password))
#     xor_key = xor_cipher(password, xor_key_setter)
    

#     print(xor_key)
    
#     key = 5
#     print(f"\nDecrypt: ")
#     print(f"Encrypted password: {en_password}")
#     print(f"denary {[ord(i) for i in en_password]}")

#     second_level = ceaser_cipher([ord(i) for i in en_password], abs(key))
    
#     print(f"after ceaser cipher {second_level}")

#     password_denary = [ord(i) for i in second_level]
#     print(f"converted to denary {password_denary}")

#     password_bianry = convert_binary(password_denary, len(password_denary))
#     print(f"convert to binary before xor: {password_bianry}")


#     password_bianry = xor_cipher_DE(password,  xor_key)
#     print(f"After xor {password_bianry}")
#     password_denary = binary_denary_converter(password_bianry)
#     print(f"After converted to denary {password_denary}")
#     print(f"After converted to string list {[chr(i) for i in password_denary]}")
#     print(f"With join : {"".join([chr(i) for i in password_denary])}")
#     return "".join([chr(i) for i in password_denary])




# encrypter("steve")
# dencrypter("+&5(5", "mike")