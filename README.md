# ProjektMiniaturowegoOscyloskopuCyfrowego
Jest to repozytorium zawierające wyniki mojej pracy dyplomowej. Miniaturowy oscyloskop cyfrowy został w pełni zaprojektowany, skonstruowany oraz oprogramowany.
Został on oparty na mikrokontroleach RPI Zero 2W oraz ESP32-WROOM32D. Dane zbierane są przy pomocy przetwornika ADC w ESP32, przesyłane przy pomocy interfejsu komunikacyjnego UART oraz wizualizowane na podpiętym do RPI wyświetlaczu dzięki uruchomionej aplikacji napisanej w pythonie z pomocą frameworka PyQT5.

![image](https://github.com/KrystianWolin/ProjektMiniaturowegoOscyloskopuCyfrowego/assets/129780873/d39c46fa-488c-4425-9149-8a52e7b3e9d0)

![image](https://github.com/KrystianWolin/ProjektMiniaturowegoOscyloskopuCyfrowego/assets/129780873/1bdfa756-e4da-4c3d-86ac-ee3cf6052aa3)

Do prawidłowego działania należy zainstalować na RPI system operacyjny Raspberry OS oraz pobrać biblioteki potrzebne do działania oprogramowania. Następnie wgrać pliki: app.py, connectionByUART.py, engine.py oraz windowCreator.py (oprogramowanie uruchamiamy z app.py).
Plik dla mikrokontrolera ESP32 to esp32V3.5.ino.
