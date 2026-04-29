# STM32F7 USB-ADC Multiplexer Board

## Purpose

This board provides ten isolated, differential analog acquisition channels,
multiplexed into a single 12-bit ADC on an STM32F7 microcontroller. The host
communicates with the board over USB. Channel selection is handled autonomously
by the firmware using an I2C-controlled analog multiplexer, so the host
receives a sequenced stream of converted values without managing the mux
directly. Primary use case: slow multi-point temperature or voltage monitoring
in industrial environments with significant common-mode noise on the sensor
lines.

---

## External Interfaces

| Interface | Connector | Protocol | Direction |
|-----------|-----------|----------|-----------|
| Host communication | USB-C | USB 2.0 FS | bidirectional |
| Power input | USB-C | 5 V / 500 mA max | in |
| Analog inputs | 10 × 2-pin terminal | differential, ±10 V max | in |

---

## Functional Blocks

### 1. USB Interface
- USB-C receptacle
- EMC filter: common-mode choke + ESD protection clamp (TVS)
- Connected directly to STM32F7 USB FS peripheral

### 2. Power Supply
- Input: 5 V from USB
- Rail 1: 3.3 V LDO — powers digital logic, MCU VDD, I2C mux
- Rail 2: 1.7 V LDO — powers MCU VDDA (ADC reference domain)
- Sequencing: 3.3 V must be stable before 1.7 V is enabled (soft-start or PGOOD tie)

### 3. Analog Frontend (×10, identical instances)
Each channel consists of:
1. **EMC filter** — common-mode choke + differential RC filter at board entry
2. **Low-pass filter** — single-pole passive, sets anti-alias corner frequency
3. **Diff-to-single converter** — discrete or IC-based; converts differential
   signal to single-ended 0–1.7 V range for ADC input

### 4. Analog Multiplexer
- I2C-controlled 10:1 analog mux
- Driven by STM32F7 I2C master
- Single output routed to STM32F7 ADC_IN pin

### 5. Microcontroller — STM32F7
- USB FS/HS peripheral for host communication
- I2C master for mux control
- 12-bit SAR ADC for signal conversion
- Firmware sequences channels, buffers readings, reports over USB CDC or custom protocol

---

## Power Architecture

```
USB 5V ──► 3V3 LDO ──► MCU VDD, I2C Mux, USB EMC filter
       └──► 1V7 LDO ──► MCU VDDA (ADC reference domain)
```

Estimated current budget:
- STM32F7 active: ~100 mA (3V3) + ~5 mA (1V7)
- I2C Mux: ~1 mA
- 10× frontend passives: negligible
- Total: < 150 mA @ 3V3 → well within USB 500 mA

---

## Signal Chain

```
Differential input
  → EMC filter (CM rejection at board entry)
  → Low-pass filter (anti-alias, sets BW)
  → Diff-to-single converter (level shift to 0–1.7 V)
  → I2C Analog Mux (channel selected via I2C from STM32)
  → STM32F7 ADC (12-bit, single-ended)
  → USB (host reads converted values)
```

---

## Known Constraints

- **Form factor**: must fit standard 3U rack enclosure, max PCB 160 × 100 mm
- **Cost target**: < 35 € BOM at 50 units
- **EMC**: must pass EN 55032 Class B without additional shielding enclosure
- **Operating temperature**: −10 °C to +60 °C
- **Input protection**: must survive ±30 V on any analog input without damage

---

## Open Questions

- [ ] Which diff-to-single IC? INA828, AD8221, discrete? — depends on CMRR requirement
- [ ] Anti-alias filter corner frequency — need to define max signal BW first
- [ ] I2C mux part selection — ADG728? MAX4617? check availability
- [ ] Does the ADC need an external reference or is VDDA sufficient?
- [ ] USB CDC vs. custom HID class — ask firmware team
- [ ] Do we need a reverse-polarity protection FET on the 5V input?
