"""
by Alan, creado el 22/1/2022 finalizado el 24/2/22 --Codigo de prueba para interrupciones,
modos con boton para un led, manejo de LCD y Menu.
Corregir ecceso de recursion alternativo...
"""
#-----------IMPORTACION_DE_LIBRERIAS-----------#
from machine import Pin, I2C , ADC
import utime
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from time import sleep

#-----------VARIABLES_GLOBALES-----------#
contador = 0            # Conteo de pulsaciones-0
contador1 = 0           # Conteo de pulsaciones-1
contador2 = 0           # Conteo de pulsaciones-2
contador2_1 = 0         # Conteo de pulsaciones-2_1
contador3 = 0           # Conteo de pulsaciones-3
interup = 0             # conteo de interupciones
Menu_val = 0            # Variable de cambio de Menu
val = 0                 # Variable de variacion en Menu
val1 = 0                # Variable de variacion en Menu 1
val2 = 0                # Variable de variacion en Menu 2
val2_1 = 0              # Variable de variacion en Menu 2_1
val3 = 0                # Variable de variacion en Menu 3

#-----------ENCODER-----------#
CLK = Pin(11, Pin.IN, Pin.PULL_UP)
DT = Pin(12, Pin.IN, Pin.PULL_UP)
SW = Pin(13, Pin.IN, Pin.PULL_UP)
btn = Pin(5, Pin.IN, Pin.PULL_DOWN)

A = CLK
B = DT

#-----------Dispositivos_de_salida-----------#
mot_dc = Pin(16, Pin.OUT)
mot_ac = Pin(17, Pin.OUT)
led = Pin(25, Pin.OUT)

#-----------LETRAS_CUSTOM-----------#
grados = [0x18,
  0x18,
  0x06,
  0x09,
  0x08,
  0x08,
  0x09,
  0x06]

c = [0x0E,
  0x11,
  0x11,
  0x10,
  0x10,
  0x11,
  0x11,
  0x0E]

s = [0x0E,
  0x11,
  0x10,
  0x10,
  0x0E,
  0x01,
  0x11,
  0x0E]

a = [0x0E,
  0x11,
  0x11,
  0x15,
  0x1F,
  0x15,
  0x11,
  0x1B]

#-----------LCD_CONFIG-----------#
I2C_ADDR = 0x27
I2C_ROWS = 2
I2C_COLS = 16

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_ROWS, I2C_COLS)

#-----------MENU'S-----------#
MENU = ["Modos ","Led   ","Motor ","Idioma ","Config "]    # Menu Principal
SUB_M1 = ["Led-ON  ","Led-OFF  ","Atras  "]                 # Sub-Menu de led
SUB_M2 = ["DC   ","AC   ","Atras   "]                            # Sub-Menu de Motores
SUB_M2_1 = ["Mot-ON  ","Mot-OFF  ","Atras  "]               # Sub-Menu de mot DC/AC
menu_prin = ["Menu Principal"]                             # TXT Menu principal

#-----------FUNCIONES-----------#
# Letras Custom
def lcd_str(mensaje, col, row):
    lcd.move_to(col,row)
    lcd.putstr (mensaje)
    
# Parpadeo LCD Inicio
def lcd_inicio():
    lcd.backlight_off()
    utime.sleep_ms(500)
    lcd.backlight_on()
    utime.sleep_ms(500)
    lcd.backlight_off()
    utime.sleep_ms(500)
    lcd.backlight_on()
    utime.sleep_ms(500)
    lcd_str("NM-02E", 4, 0)
    utime.sleep_ms(1000)
    lcd_str("CSA_TEC", 9, 1)
    utime.sleep_ms(1000)
    lcd_str("V1.0", 0, 1)
    utime.sleep_ms(1000)
    
# Caracteres Personalizados
def Custom_char():
    lcd.custom_char(1, bytearray(c))
    lcd.custom_char(2, bytearray(s))
    lcd.custom_char(3, bytearray(a))

# Menu Principal
def Menu_principal():
    # Primero hacemos un control de errores si no pasa nada el codigo se ejecuta normalmente
    try:
        lcd.clear()
        global Menu_val
        global val
        global contador
        global MENU
        global Menu_prin
        lastState = A.value()   # Ultimo estado sera igual a lo que lea en el pin A
        while Menu_val == 0:
            estado = A.value()
        
            if estado != lastState:
                if B.value() != estado:
                    contador -= 1
                    val = contador
                    utime.sleep_ms(100)
                else:
                    contador += 1
                    val = contador
                    utime.sleep_ms(100)
            lastState = estado


            # Variamos la funcion en un maximo de 4, esto nos sirve para movernos en el Menu
            if val > 4:
                contador = 0
                val = 0
            elif val < 0:
                contador = 0
                val = 0
            
            # Verificamos si fue pulsado en donde estamos parados
            if btn.value() and val == 1:
                Menu_val = 1
                print("\nEstado del menu {}".format(Menu_val))
                Sub_Menu_led()
            elif btn.value() and val == 2:
                Menu_val = 2
                print("\nEstado del menu {}".format(Menu_val))
                Sub_Menu_mot()

            #-----------INICIO_DE_LCD-----------#
            utime.sleep_ms(20)
            lcd_str(menu_prin[0],1 ,0)
            lcd_str(">" ,1 ,1)
            lcd_str("<" ,14 ,1)
            lcd_str(MENU[val],5 ,1)  
            print(contador)

        print("\nEstado del menu {}".format(Menu_val))
    # Exepto que tengamos un error de Recursion superado en este caso se ejecuta lo siguiente
    except RuntimeError:
        print("ERROR DE RECURSION SUPERADO, RESETEANDO...")
        Menu_val = 0
        Menu_principal()
    except TypeError:
        print("ERROR DE RECURSION SUPERADO, RESETEANDO...")
        Menu_val = 0
        Menu_principal()
        
# Sub Menu de Led
def Sub_Menu_led():
    try:
        lcd.clear()
        global Menu_val
        global val1
        global contador1
        lastState = A.value()   # Ultimo estado sera igual a lo que lea en el pin A
        Menu_val = 1
        while Menu_val == 1:
            estado = A.value()
        
            if estado != lastState:
                if B.value() != estado:
                    contador1 -= 1
                    val1 = contador1
                    utime.sleep_ms(100)
                else:
                    contador1 += 1
                    val1 = contador1
                    utime.sleep_ms(100)
            lastState = estado

            if val1 > 2:
                contador1 = 0
                val1 = 0
            elif val1 < 0:
                contador1 = 0
                val1 = 0
            
            # Estados con boton
            if btn.value() and val1 == 0:
                led.value(1)
            elif btn.value() and val1 == 1:
                led.value(0)
            elif btn.value() and val1 == 2:  # Aqui rompemos el ciclo y volvemos al Menu Pincipal
                Menu_val = 0
                Menu_principal()

            utime.sleep_ms(20)
            lcd_str("   ", 0, 0)
            lcd_str("    ", 11, 0)
            lcd_str("Sub Menu",3 ,0)
            lcd_str(">" ,1 ,1)
            lcd_str("<" ,14 ,1)
            lcd_str(SUB_M1[val1],4 ,1)
            print(contador1)

        print("\nEstado del menu {}".format(Menu_val))
    except TypeError:
        print("ERROR DE RECURSION SUPERADO, RESETEANDO...")
        Menu_val = 0
        Menu_principal()

# Sub Menu de motor
def Sub_Menu_mot():
    try:
        lcd.clear()
        global Menu_val
        global val2
        global contador2
        lastState = A.value()   # Ultimo estado sera igual a lo que lea en el pin A
        Menu_val = 2
        while Menu_val == 2:
            estado = A.value()
        
            if estado != lastState:
                if B.value() != estado:
                    contador2 -= 1
                    val2 = contador2
                    utime.sleep_ms(100)
                else:
                    contador2 += 1
                    val2 = contador2
                    utime.sleep_ms(100)
            lastState = estado

            if val2 > 2:
                contador2 = 0
                val2 = 0
            elif val2 < 0:
                contador2 = 0
                val2 = 0
            
            # Estados con boton
            if btn.value() and val2 == 0:
                # Entramos en motor DC
                Menu_val = 3
                Mot_DC()
            if btn.value() and val2 == 1:
                # Entramos en motor AC
                Menu_val = 4
                Mot_AC()
            elif btn.value() and val2 == 2:  # Aqui rompemos el ciclo y volvemos al Menu Pincipal
                Menu_val = 0
                Menu_principal()

            utime.sleep_ms(10)
            lcd_str("Menu-Motores  ",1 ,0)
            lcd_str(">" ,1 ,1)
            lcd_str("<" ,14 ,1)
            lcd_str(SUB_M2[val2],4 ,1)
            print(contador2)

        print("\nEstado del menu {}".format(Menu_val))
    
    except TypeError:
        print("ERROR DE RECURSION SUPERADO EN MOTOR, RESETEANDO...")
        Menu_val = 0
        Menu_principal()

# Sub Menu para opciones en Motores DC
def Mot_DC():
    try:
        lcd.clear()
        global Menu_val
        global val2_1
        global contador2_1
        lastState = A.value()   # Ultimo estado sera igual a lo que lea en el pin A
        Menu_val = 3
        while Menu_val == 3:
            estado = A.value()
        
            if estado != lastState:
                if B.value() != estado:
                    contador2_1 -= 1
                    val2_1 = contador2_1
                    utime.sleep_ms(100)
                else:
                    contador2_1 += 1
                    val2_1 = contador2_1
                    utime.sleep_ms(100)
            lastState = estado

            if val2_1 > 2:
                contador2_1 = 0
                val2_1 = 0
            elif val2_1 < 0:
                contador2_1 = 0
                val2_1 = 0
            
            # Estados con boton
            if btn.value() and val2_1 == 0:
                mot_dc.value(1)
            elif btn.value() and val2_1 == 1:
                mot_dc.value(0)
            elif btn.value() and val2_1 == 2:  # Aqui rompemos el ciclo y volvemos al Menu Pincipal
                Menu_val = 2
                Sub_Menu_mot()

            utime.sleep_ms(10)
            lcd_str("Control Motor DC  ",0 ,0)
            lcd_str(">" ,1 ,1)
            lcd_str("<" ,14 ,1)
            lcd_str(SUB_M2_1[val2_1],4 ,1)
            print(contador2_1)

        print("\nEstado del menu {}".format(Menu_val))
    
    except TypeError:
        print("ERROR DE RECURSION SUPERADO EN MOTOR, RESETEANDO...")
        Menu_val = 3
        Mot_DC()

# Sub Menu para opciones en Motores AC
def Mot_AC():
    try:
        lcd.clear()
        global Menu_val
        global val3
        global contador3
        lastState = A.value()   # Ultimo estado sera igual a lo que lea en el pin A
        Menu_val = 4
        while Menu_val == 4:
            estado = A.value()
        
            if estado != lastState:
                if B.value() != estado:
                    contador3 -= 1
                    val3 = contador3
                    utime.sleep_ms(100)
                else:
                    contador3 += 1
                    val3 = contador3
                    utime.sleep_ms(100)
            lastState = estado

            if val3 > 2:
                contador3 = 0
                val3 = 0
            elif val3 < 0:
                contador3 = 0
                val3 = 0
            
            # Estados con boton
            if btn.value() and val3 == 0:
                mot_ac.value(1)
            elif btn.value() and val3 == 1:
                mot_ac.value(0)
            elif btn.value() and val3 == 2:  # Aqui rompemos el ciclo y volvemos al Menu Pincipal
                Menu_val = 2
                Sub_Menu_mot()

            utime.sleep_ms(10)
            lcd_str("Control Motor AC  ",0 ,0)
            lcd_str(">" ,1 ,1)
            lcd_str("<" ,14 ,1)
            lcd_str(SUB_M2_1[val3],4 ,1)
            print(contador3)

        print("\nEstado del menu {}".format(Menu_val))
    
    except TypeError:
        print("ERROR DE RECURSION SUPERADO EN MOTOR, RESETEANDO...")
        Menu_val = 4
        Mot_AC()

# Funcion Principal
def main():
    lastState = A.value() # Ultimo estado sera igual a lo que lea en el pin A
    Custom_char()
    lcd_inicio()
    Menu_principal()    # Si Menu_val es igual a 0 se ejecuta esta funcion.
    
if __name__ == "__main__":
    main()
