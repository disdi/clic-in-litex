# Milestones

## CPU Implementation

For detailed information about implementing the CLINT/CLIC interface in a RISC-V CPU, see the [CPU Implementation Guide](cpu-implementation-guide.md).

## Litex Implementation

[PR #2260: Add RISC-V CLIC and CLINT interrupt controller support](https://github.com/enjoy-digital/litex/pull/2260) has been posted to support for the RISC-V Core Local Interrupt Controller (CLIC) and the CLINT (Core Local Interruptor) in the LiteX SoC framework.

---

### Hardware Changes

---

There are two Interrupt Controller Implementations that have been added to Litex SOC framework which enables LiteX-based RISC-V SoCs to choose between CLINT and CLIC.

Both controllers expose standardized signals for integration:

- **CLINT:**  
    - `timer_interrupt`
    - `software_interrupt`

- **CLIC:**  
    - `clic_interrupt`
    - `clic_interrupt_id`
    - `clic_interrupt_priority`

#### CLINT Hardware Integration in Litex

The basic RISC-V interrupt architecture defined in the RISC-V privileged specification, using CSRs (Control and Status Registers) like mie and mip for interrupt management.

##### Summary of Changes:

1. **CLINT Core Module** (`litex/soc/cores/clint.py`):
    - Multi-HART support with configurable `num_harts` parameter.
    - Separate timer and software interrupt outputs per HART.
    - 64-bit `MTIME` counter with auto-increment.
    - Per-HART 64-bit `MTIMECMP` registers.
    - Per-HART `MSIP` bits for software interrupts.
    - CSR-based register interface with proper naming.
    - Helper method `add_to_soc()` for easy integration.

2. **Minerva CPU Updates** (`litex/soc/cores/cpu/minerva/core.py`):
    - Added CLINT interrupt support to Minerva CPU.

3. **Ibex CPU Updates** (`litex/soc/cores/cpu/ibex/core.py`):
    - Added CLINT interrupt support to Ibex CPU.

4. **VexRiscv CPU Updates** (`litex/soc/cores/cpu/vexriscv/core.py`):
    - Added CLINT interrupt support to VexRiscv CPU.

5. **SoCCore Support** (`litex/soc/integration/soc_core.py`):
    - Added CLINT parameters (`--with-clint`).
    - CLINT instantiation for compatible CPUs.

6. **Software Support** (`.../irq.h`, `.../clint.h`):
    - Generic Interrupt Service Routines (ISRs) to handle timer and software interrupts.
    - C functions for CLINT configuration and control provided via `clint.h`.

The implementation of the CLINT design is compliant with both the older SiFive CLINT design and the newer [RISC-V ACLINT specification](https://github.com/riscvarchive/riscv-aclint).

#### CLIC Hardware Integration in Litex

An advanced interrupt controller that provides enhanced features for real-time applications.

##### Summary of Changes:
1. **CLIC Core Module** (`litex/soc/cores/clic.py`):
    - Implements RISC-V CLIC specification features.
    - Supports up to 4096 interrupts with configurable priority.
    - Edge/level trigger configuration per interrupt.
    - Hardware priority arbitration and interrupt preemption.
    - CSR interface for configuration registers.

2. **Minerva CPU Updates** (`litex/soc/cores/cpu/minerva/core.py`):
    - Added CLIC interrupt signals (interrupt request, ID, priority).
    - Automatic CLIC instantiation when CPU has CLIC support.
    - Defined CLIC memory address region.

3. **Ibex CPU Updates** (`litex/soc/cores/cpu/ibex/core.py`):
    - Added CLIC interrupt signals (interrupt request, ID, priority).
    - Automatic CLIC instantiation when CPU has CLIC support.
    - Defined CLIC memory address region.

4. **VexRiscv CPU Updates** (`litex/soc/cores/cpu/vexriscv/core.py`):
    - Added CLIC interrupt support to VexRiscv CPU.

5. **SoC Integration** (`litex/soc/integration/soc.py`):
    - Added `add_clic()` method for easy CLIC integration.
    - Automatic connection of interrupt sources to CLIC inputs.
    - CSR mapping for CLIC configuration.

6. **SoCCore Support** (`litex/soc/integration/soc_core.py`):
    - Added CLIC parameters (`--with-clic`, `--clic-num-interrupts`, `--clic-ipriolen`).
    - CLIC instantiation for compatible CPUs.


---

### Software Changes

---

The CLINT/CLIC Interrupt Controller Implementations if enabled in LiteX-based RISC-V SoCs can be accessed via software.

### CLINT Software Integration in Litex

1. **Software Driver** (`.../irq.h`, `.../clint.h`):
    - Provides generic Interrupt Service Routines (ISRs) for handling timer and software interrupts.
    - Includes C functions for configuring and controlling the CLINT via `clint.h`.

2. **Software Demo Application** (`clint_demo.c`):
    - Demonstrates triggering and handling software interrupts using the CLINT.
    - Offers a practical example of utilizing the CLINT C API.

### CLIC Software Integration in Litex

1. **Software Driver** (`.../irq.h`, `.../clic.h`):
    - Implements generic ISRs for managing prioritized external interrupts.
    - Supplies C functions for configuring and controlling the CLIC via `clic.h`.
    - Features interrupt enable/disable, priority configuration, and attribute settings.
    - Supports direct CSR access for the first 16 interrupts.

2. **Software Demo Application** (`clic_demo.c`):
    - Highlights advanced interrupt capabilities of the CLIC.
    - Includes tests for priority-based preemption, interrupt thresholding, and edge/level-triggered modes.
    - Serves as a detailed example of using the CLIC C API effectively.

---