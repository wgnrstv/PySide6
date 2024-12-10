import time
import psutil
import requests
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    # Создаем сигнал, который передает список с данными о загрузке RCPU и RAM
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # Атрибут для управления задержкой

    def run(self) -> None:
        """
        Переопределенный метод для запуска потока
        """
        if self.delay is None:
            self.delay = 1  # Устанавливаем значение задержки по умолчанию

        while True:
            cpu_value = psutil.cpu_percent()  # Получаем загрузку CPU
            ram_value = psutil.virtual_memory().percent  # Получаем загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # Передаем данные в сигнал
            time.sleep(self.delay)  # Задержка перед следующей итерацией


class WeatherHandler(QtCore.QThread):
    # Создаем сигнал для передачи данных о погоде
    weatherDataReceived = QtCore.Signal(dict)

    # Создаем сигнал для ошибок
    weatherErrorOccurred = QtCore.Signal(str)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = True  # По умолчанию поток активен

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления данных о погоде

        :param delay: время задержки обновления
        """
        self.__delay = delay

    def stop(self) -> None:
        """
        Метод для остановки потока
        """
        self.__status = False

    def run(self) -> None:
        """
        Метод для выполнения запроса к API погоды
        """
        while self.__status:
            try:
                response = requests.get(self.__api_url, timeout=5)
                response.raise_for_status()  # Проверяем наличие ошибок HTTP
                data = response.json()  # Парсим JSON-ответ
                self.weatherDataReceived.emit(data)  # Отправляем данные через сигнал
            except requests.RequestException as e:
                self.weatherErrorOccurred.emit(str(e))  # Отправляем сообщение об ошибке
            time.sleep(self.__delay)  # Задержка перед следующим запросом
