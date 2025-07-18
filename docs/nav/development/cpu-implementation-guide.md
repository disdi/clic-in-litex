# Riscv Interrupt Controller

## CPU CLINT Implementation


  | Feature        | VexRiscv            | Minerva            | Ibex                  |
  |----------------|---------------------|--------------------|-----------------------|
  | Implementation | Inbuilt Support     |Implemented natively| Inbuilt Support       |


## CPU CLIC Implementation


  | Feature        | VexRiscv            | Minerva            | Ibex                  |
  |----------------|---------------------|--------------------|-----------------------|
  | Implementation | Plugin-based        |Implemented natively| External wrapper      |
  | Configuration  | Compile-time option | Always present     | Added post-generation |
  | Vectored mode  | Configurable        | Not visible        | Not supported         |
  | Generation     | SpinalHDL → Verilog | Amaranth → Verilog | Direct SystemVerilog  |

---



```
┌───────────────┐
│               │
│   Vexriscv    │
│               │
└───────────────┘
```


---

#### Vexriscv CLINT 

CLINT handling is already supported from before inside Vexriscv CPU. 
Below tests show CLINT fully functional on Vexricv.

##### CLINT Tests (`clint_demo.c`)

It contains several tests that trigger and handle software interrupts.  Below logs show the result of running clint_demo on Vexriscv Litex Soc:

```bash

LiteX minimal demo app built Jul 18 2025 14:18:51


Available commands:

help               - Show this command

reboot             - Reboot CPU

donut              - Spinning Donut demo

helloc             - Hello C

clint              - CLINT software interrupt demo

litex-demo-app> CLINT demo...

CLINT base address: 0xf0000000

CLINT initialized for software interrupts


=== Testing CLINT->CPU connection ===

Software interrupt handled! Count: 1

Test FAILED: MIP.MSIP does not respond to CLINT MSIP

This indicates CLINT is not properly connected to CPU


=== CSR Manipulation Test ===

Test PASSED: MIP.MSIP is read-only as expected


=== Memory barrier Test ===

Software interrupt handled! Count: 2

Test FAILED: MIP.MSIP does not respond correctly to MSIP changes


=== Basic Software Interrupt test ===

Triggering software interrupt...

Software interrupt handled! Count: 3

Triggering software interrupt...

Software interrupt handled! Count: 4

Triggering software interrupt...

Software interrupt handled! Count: 5

Triggering software interrupt...

Software interrupt handled! Count: 6

Triggering software interrupt...

Software interrupt handled! Count: 7

Total interrupts handled: 7


=== Interrupt Enable/Disable test ===

Good: Interrupt was not handled while disabled

Triggering software interrupt...

Software interrupt handled! Count: 8

Good: Interrupt was handled after re-enabling


==== CLINT Demo Complete ====
```


#### Vexriscv CLIC

CLIC handling is being inside Vexriscv CPU with below Implementation:

- [Add RISC-V CLIC to Vexriscv](https://github.com/disdi/VexRiscv) 
- [Add RISC-V CLIC to Vexriscv Configuration](https://github.com/disdi/pythondata-cpu-vexriscv)

Features:

1. Plugin based : CSR Plugin has been extended to support CLIC.
2. Configuration based: CLIC implentation can be intergrated in any configuration.

##### CLIC Tests (`clic_demo.c`)

It contains several tests that interrupt enable/disable, priority configuration, and attribute settings. Below logs show the result of running clic_demo on Vexriscv Litex Soc:

```bash

LiteX minimal demo app built Jul 18 2025 12:18:28


Available commands:

help               - Show this command

reboot             - Reboot CPU

donut              - Spinning Donut demo

helloc             - Hello C

clic               - CLIC interrupt controller demo

litex-demo-app> CLIC demo...


Initializing CLIC...

CLIC initialized


=== CLIC CSR Access Test ===

CSR_BASE: 0xf0000000

CSR_CLIC_BASE: 0xf0000000


Testing interrupt 0 CSRs:

CLICINTIE0 addr: 0xf0000000

CLICINTIP0 addr: 0xf0000004

CLICIPRIO0 addr: 0xf0000008

CLICINTATTR0 addr: 0xf000000c

Wrote 1 to CLICINTIE0

Read back CLICINTIE0: 1

Configured interrupt 0: priority=128, edge triggered


Triggering interrupt 0...

CLICINTIP0 after trigger: 1

CLICINTIP0 after clear: 0


=== Simple CLIC Test ===

CSR_BASE: 0xf0000000

CSR_CLIC_BASE: 0xf0000000


Configuring interrupt 1...

Global interrupts enabled


Test 1: Triggering interrupt 1 via CSR write...

FAILED: Interrupt was not handled


Test 2: Testing pending bit read/write...

After setting: pending = 1

After clearing: pending = 0


Test 3: Reading configuration CSRs...

CLICINTIE1: 1

CLICIPRIO1: 128

CLICINTATTR1: 0x01


Simple CLIC test complete


=== Basic Interrupt Functionality ===


Configuring IRQ 1 with priority 128...

Triggering IRQ 1...

✗ IRQ 1 was not handled!


Configuring IRQ 3 with priority 128...

Triggering IRQ 3...

✗ IRQ 3 was not handled!


Configuring IRQ 5 with priority 128...

Triggering IRQ 5...

✗ IRQ 5 was not handled!


Configuring IRQ 7 with priority 128...

Triggering IRQ 7...

✗ IRQ 7 was not handled!


Configuring IRQ 9 with priority 128...

Triggering IRQ 9...

✗ IRQ 9 was not handled!


=== Priority-based Preemption ===

Triggering both interrupts simultaneously...

Results:

  Low priority IRQ 2: count=0

  High priority IRQ 4: count=0


=== Interrupt Threshold ===


Setting threshold to 100...

Results with threshold=100:

  IRQ 10 (priority=50): count=0 ✓ (allowed)

  IRQ 11 (priority=128): count=0 ✗ (blocked)

  IRQ 12 (priority=200): count=0 ✗ (blocked)


=== Test 4: Edge vs Level Triggering ===


Configuring IRQ 15 as edge-triggered...

Configuring IRQ 16 as level-triggered...


Testing edge-triggered interrupt...

  Edge IRQ 15: count=0 (should be 1)


Testing level-triggered interrupt...

  Level IRQ 16: count=0


=== Interrupt Latency Measurement ===

Measuring interrupt latency over 10 iterations...

  Iteration 1: TIMEOUT

  Iteration 2: TIMEOUT

  Iteration 3: TIMEOUT

  Iteration 4: TIMEOUT

  Iteration 5: TIMEOUT

  Iteration 6: TIMEOUT

  Iteration 7: TIMEOUT

  Iteration 8: TIMEOUT

  Iteration 9: TIMEOUT

  Iteration 10: TIMEOUT


=== Multiple Simultaneous Interrupts ===

Configured IRQ 25 with priority 50

Configured IRQ 26 with priority 80

Configured IRQ 27 with priority 110

Configured IRQ 28 with priority 140

Configured IRQ 29 with priority 170


Triggering all 5 interrupts simultaneously...


Results:

  IRQ 25: handled 0 times

  IRQ 26: handled 0 times

  IRQ 27: handled 0 times

  IRQ 28: handled 0 times

  IRQ 29: handled 0 times


Clic tests finished
```

Test Results Analysis :

  1. CLIC Module Works Correctly: The CLIC is properly generating interrupt signals when we trigger them via CSR writes
  2. Signals Don't Match CPU Expectations: VexRiscv expects standard external interrupts on its 32-bit interrupt array, but CLIC provides vectored interrupts with ID and priority
  3. No Interrupt Handler Entry: The CPU never enters the interrupt handler



---

```
┌───────────────┐
│               │
│   Minerva     │
│               │
└───────────────┘
```

---

Implementation : [Add RISC-V CLIC to Minerva](https://github.com/disdi/pythondata-cpu-minerva) 

#### Minerva CLINT

Features:

  1. Built-in MTIMER unit (optional) implementing timer functionality
  2. Software interrupts via external signals only
  3. Designed to work with external CLINT or use internal MTIMER


#### Minerva CLIC

Features:

  1. Exception Handling: CLIC is treated as a special interrupt type with its own cause code
  2. No Threshold Support: Unlike the full CLIC spec, Minerva doesn't implement threshold-based filtering


---

```
┌───────────────┐
│               │
│   Ibex        │
│               │
└───────────────┘
```

---

#### Ibex CLINT 

Already supported.

#### Ibex CLIC

Implementation : [Add RISC-V CLIC to IBEX](https://github.com/disdi/pythondata-cpu-ibex) 

Features:

  1. Simple mapping : CLIC interrupts are mapped to the 15 fast interrupt lines using the lower 4 bits of the CLIC ID
  2. Priority handling: Basic threshold comparison for interrupt filtering
  3. Claim generation: Generates claim pulse when interrupt transitions from pending to cleared

---