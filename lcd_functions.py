import I2C_LCD_driver
import time

lcd = I2C_LCD_driver.lcd()

def mostrar_ips_en_lcd(ips):
    lcd.lcd_clear()
    if not ips:
        lcd.lcd_display_string("No devices found", 1)
        return

    # La pantalla tiene solo 2 líneas de 16 caracteres
    # Mostramos la primera y segunda IP o parte de ellas
    lcd.lcd_display_string(ips[0][:16], 1)  # Primera línea 
    if len(ips) > 1:
        lcd.lcd_display_string(ips[1][:16], 2)  # Segunda línea

    # Para más IPs puedes alternar la pantalla con un ciclo o mostrar resumen