# ProjektMiniaturowegoOscyloskopuCyfrowego
Jest to repozytorium zawierające wyniki mojej pracy dyplomowej. Miniaturowy oscyloskop cyfrowy został w pełni zaprojektowany, skonstruowany oraz oprogramowany.
Został on oparty na mikrokontroleach RPI Zero 2W oraz ESP32-WROOM32D. Dane zbierane są przy pomocy przetwornika ADC w ESP32, przesyłane przy pomocy interfejsu komunikacyjnego UART oraz wizualizowane na podpiętym do RPI wyświetlaczu dzięki uruchomionej aplikacji napisanej w pythonie z pomocą frameworka PyQT5.

Do prawidłowego działania należy zainstalować na RPI system operacyjny Raspberry OS oraz pobrać biblioteki potrzebne do działania oprogramowania. Następnie wgrać pliki: app.py, connectionByUART.py, engine.py oraz windowCreator.py.
Plik dla mikrokontrolera ESP32 to esp32V3.5.ino.
