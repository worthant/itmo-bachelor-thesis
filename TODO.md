# TODO

## practise

- [x] research: keyword voice detection architectures, energy efficent &
      optimisation methods & approaches, availability, costs
- [x] research: mic types - precision vs enery efficiency
- [x] research: power measurement approaches, methods, sensors; costs,
      availability
- [x] research: cheap available excessive power source for test bench
- [x] research: charger for 18650 power source
- [x] order: inmp441, esp32 s3 zero, ina219, esp32 c3, 2x18650, 2xtp4056, 2xLED,
      pin headers, soldering boards, m4 stands, plexiglass
- [x] research: i2s pipelines, i2s api
- [x] code: setup MEMS i2s mic
- [x] research: partitioning, esp memory layout
- [x] code(s3): make partitions for 1 wakenet model
- [x] code(s3): setup 1 wakenet model, get "Hi, Esp" wakeup word to work
- [x] code(s3): make partitions for 4 wakenet models
- [x] code(s3): setup 4 weakeup models, make them work
- [x] code(s3): blink WS2812B onboard RGB led for each detected wakeup word
- [x] docs: draft practise report
- [x] research: Ohms law, Ohms law for a complete circuit, internal 18650's
      resistance
- [x] research: wires internal resistance, Kirhgof's law, prove board electrical
      circuit
- [x] code(c3): i2c bus, INA219 i2c sensor, logging task, get raw data
- [x] verify: ina219 raw data compared to multimeter on 5v-gnd pins on s3 zero
- [x] verify: a lot of internal resistance, unbalanced gnd potentials, bad
      jumper wires quality
- [x] solder: weak joints & all GND to star patten; thick wires
- [x] research: how to do ULP VAD architecture
- [x] read docs: ulp types, sleep modes, electrical characteristics
- [x] research: ulp fsm vs ulp risc-v; rtc gpio, ulp wakeup
- [x] research: mosfet types - schematics, p/n channels, sockets, availability
- [x] order: p-channel ao3401 mosfet & add datasheet to repo
- [x] research: analog mic types, availability, precision
- [x] order: max9814

- [ ] code: add power (in w) to measurnments
- [ ] code: python script to read UART CSV and compose graph
- [ ] code&research: sink s3 into deep sleep mode, measure power consumption
- [ ] research: find redundant power consumption sources in deep sleep, minimise
- [ ] solder: max9814 & pin headers, connect accordingly
- [ ] code: ULP RISC-V - read adc, setup threshold, wakeup main cpu
- [ ] decision: mic power control - 1. mosfet / 2. rtc gpio / 3. mosfet + rtc
      gpio
- [ ] (decide) solder: ao3401, connect to rtc gpio
- [ ] measure: active / light sleep / deep sleep / deep sleep + MOSFET
- [ ] docs: write chapter 3.3, add tables, graphs

- [ ] docs: add assembly process photos
- [ ] docs: create full electrical circuit scheme (LaTeX / draw.io / ?)
- [ ] docs: FSM diagram
- [ ] docs: perfect uml diagrams
- [ ] docs: add final test bench photos
- [ ] docs: write full component prices e.t.c., compose ordering list
- [ ] docs: write technical requirements, show bykovskiy

- [ ] decision: WILL WE DO OUR OWN DS-CNN OR FUCK NO?

## robot application

- [x] research: need small power source with protection
- [x] order: 250mah & 430mah versions of Li-Pol GoPower LP502030 PK1 3.7V
- [x] research: smallest lipo chargers
- [x] order:
