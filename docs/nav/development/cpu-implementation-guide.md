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

Already supported.

#### Vexriscv CLIC

Implementation :
[Add RISC-V CLIC to Vexriscv](https://github.com/disdi/VexRiscv) 
[Add RISC-V CLIC to Vexriscv Configuration ](https://github.com/disdi/pythondata-cpu-vexriscv)

Features:

1. Plugin based : CSR Plugin has been extended to support CLIC.
2. Configuration based: CLIC implentation can be intergrated in any configuration.

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