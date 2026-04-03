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

- [x] research: rtc gpio capabilities, pin power strengths
- [x] decision: mic power control - 1. mosfet / `2. rtc gpio` / 3. mosfet + rtc
      gpio
  - note: sadly ordered mosfets are redundant because we have rtc gpio which
    already has them
- [x] research: does rtc gpio output work in deep sleep?
  - note: we have 20-40ma for each rtc io pin, ~400ma max for all
- [x] solder: add red LED to any gpio supporting RTC IO matrix
  - note: chose `Sourcing` scheme, because no leaks when "0" (gpio -> led ->
    resistor -> gnd), and also it's simpler to control. For current CMOS schemes
    we have 20ma for both sinking and sourcing schemes, so it doesn't matter.
  - `Sinking` scheme can have small leaks when we have small gnd leak (3.3v ->
    led -> resistor -> gpio)
- [x] code(s3): go to deep sleep, light green LED using ULP RISC-V
- [x] ulp vad: premade module
  - [x] hw: calibrate sound module treshold via multimeter (~2v on in+)
  - [x] verify: Sound module works (active low logic, led blinking on sound)
  - [x] solder: add ready-to-go sound-detection module to rtc gpio
- [x] code(s3): add ext0 on sound-detection module OUT rtc gpio, wakeup on it
- [ ] docs: record a video with the system going into/out of deepsleep, with
      power consumption drops
- [ ] code(s3): do inference right away after wakeup
- [x] verify: measure power consumption in deep sleep (ina219 & multimeter)
  - note: got 24ma in deep sleep wtf. should be 10uA. ina219 not accurate enough
- [x] solder: mount ina228 instead of ina219 for better accuracy
- [x] code(c3): setup ina228
- [x] verify: measure power consumption in deep sleep (ina228)
  - note: got 0.5ma in deep sleep. should be like 10uA.
- [x] ?: red rid of current leaks in deep sleep
  - note: too much work. esp32 s3 zero is just shit, was not meant for ULP
- [x] verify: measure voice detection sensor power consumptionh (ina228)
  - note: got 1.2ma on high out (led off), ~4.8ma on low out (led light)
  - note: probably soldering off the led will reduce the power consumption, but
    this ky-037 module is also not meant for ULP. it's comparator is heavy on
    power, and schematics could be better. there are VAD mics that use 10mkA in
    the wild.
- [ ] verify: check keyword detection

- [x] decision: WILL WE DO OUR OWN DS-CNN OR FUCK NO?
  - note: we will 100% need to do some kind of ds-cnn or whatever for practise
    to detect our own commands
- [ ] research: how we need to do, what we need to do. how to do fastest,
      simplest, most efficient, and for it just to work properly
- [ ] code: train this nn, test on datasets, implement on s3
- [ ] write: full practise report

- [ ] code(c3): add power (in w) to measurnments
- [ ] code(c3): python script to read UART CSV and compose graph
- [ ] code&research: sink s3 into deep sleep mode, measure power consumption
- [ ] research: find redundant power consumption sources in deep sleep, minimise
- [ ] measure: active / light sleep / deep sleep / deep sleep + MOSFET
- [ ] docs: write chapter 3.3, add tables, graphs
- [ ] docs: add assembly process photos
- [ ] docs: create full electrical circuit scheme (LaTeX / draw.io / ?)
- [ ] docs: FSM diagram
- [ ] docs: perfect uml diagrams
- [ ] docs: add final test bench photos
- [ ] docs: write full component prices e.t.c., compose ordering list
- [ ] docs: write technical requirements, show bykovskiy

### ULP VAD (Voice Activity Detection)

- [x] research: ULP VAD architectures & components
- [x] decision: Electret capsule + Ultra-low-power Comparator (MCP6541/LMV331)
- [x] order: ready-to-go sound-detection based on LM393
  - note: this is the module we complete the prac with
- [ ] order: MCP6541T-I/OT (Ozon/ЧипИДип) + SOT23-DIP adapters
  - note: this is the module for `thesis`!
- [ ] order: Electret capsules (EM6027, HMO0603)
  - note: this is the module for `thesis`!
- [ ] order: High-ohm resistors (470k, 1M) + 1M Potentiometers
  - note: this is the module for `thesis`!
- [ ] lab: Assemble "Practice" version (LM393 module)
- [ ] lab: Measure "Practice" idle current (target: compare vs baseline)
- [ ] code(s3): Setup ext0 wakeup on RTC_GPIO from Comparator Output
- [ ] lab: Assemble "Thesis" version (MCP6541 + 1M resistors)
  - [ ] add?: positive feedback resistor for Hysteresis
  - [ ] add?: filtering capacitor on Vref
- [ ] lab: Measure "Thesis" idle current (target: < 100uA total)
- [ ] verify: calibrate threshold to ignore background noise but catch "Hey"
- [ ] docs: Create comparison table: LM393 (Practice) vs MCP6541 (Thesis)

## robot application

- [x] research: need small power source with protection
- [x] order: 250mah & 430mah versions of Li-Pol GoPower LP502030 PK1 3.7V
- [x] research: smallest lipo chargers
- [x] order: small lipo chargers
- [x] assemble: 2 versions of lipo + 2 lipo chargers.
- [x] verify: both lipo+charger combinations charge&function
- [ ] assemble: once testing ready, assemble inmp441 & ULP VAD components
- [ ] code: (uart?) protocol communication for directional commands
      (forwards/backwards/left/right)
