## Зачем этот репозиторий

Пишу диплом бакалавриата. Тема: "Разработка энергоэффективной системы
распознавания речи с использованием нейронных сетей для IoT-устройств".

Для создания энергоэффективной системы применяется технология edge devices - ...

## Система

Для прототипа системы я выбрал чип esp32-s3 от компании Espressif. Почему именно
его? Потому что:

- векторные инструкции для нейронок (SIMD - Single instruction, Multiple Data -
  за одну инструкцию можно сразу много чиселок перемножать => быстрее инференс)
- LX7 крутая быстрая архитектура, RISC-V хайп
- есть wifi, btle и основная периферия, что соответствует IoT-устройству
- есть несколько уровней энергосбережения - стандартный и глубокий сон. Можно
  отключать ЦПУ и ждать команды, чтобы потом просыпаться по какой-нибудь
  команде, аля "Алиса", выполнять свою задачу, и засыпать обратно. Так можно
  жить от одной батарейки без подзарядки продолжительное время.
- Есть ESP-DL фреймворк с уже натренированными модельками специально для этой
  архитектуры

## Прототип v1.0

```mermaid
---
config:
  layout: dagre
---
flowchart LR
 subgraph system1["Power Domain №1 (Измеряемая система)"]
    direction LR
        S3["S3 Zero<br>TFLite<br>sleep modes"]
        INA["INA219<br>измерение<br>I2C addr 0x40"]
        TP1["TP4056<br>защита"]
        BAT1["18650<br>~4V DC"]
  end
 subgraph system2["Power Domain №2 (Логгер)"]
    direction LR
        C3["C3 Mini<br>сбор данных<br>UART/WiFi/BT"]
        TP2["TP4056<br>защита"]
        BAT2["18650<br>~4V DC"]
  end
    BAT1 --> TP1
    TP1 --> INA
    INA --> S3
    BAT2 --> TP2
    TP2 --> C3
    INA <-- I2C master<br>slave &nbsp; &nbsp; &nbsp; &nbsp; --> C3
    C3 -- "USB-UART<br>WiFi<br>BTLE" --> PC["PC<br>анализ<br>plotting<br>real-time"]
    C3 -. I2C/SPI<br>опционально .-> DISPLAY["oled/lcd/tft<br>display"]

     BAT1:::powerDomain
     TP1:::powerDomain
     INA:::sensor
     S3:::powerDomain
     BAT2:::logger
     TP2:::logger
     C3:::logger
     PC:::logger
    classDef powerDomain fill:#e1f5ff,stroke:#0066cc,stroke-width:2px
    classDef sensor fill:#fff4e1,stroke:#ff9800,stroke-width:2px
    classDef logger fill:#f0fff0,stroke:#4caf50,stroke-width:2px
```
