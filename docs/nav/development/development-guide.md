# Development guide

## HW Implementation

[PR #2260: Add RISC-V CLIC and CLINT interrupt controller support](https://github.com/enjoy-digital/litex/pull/2260) has been posted to support for the RISC-V Core Local Interrupt Controller (CLIC) and the CLINT (Core Local Interruptor) in the LiteX SoC framework.


### Key Changes

There are two Interrupt Controller Implementations that have been added to Litex SOC framework which enables LiteX-based RISC-V SoCs to choose between:

#### CLINT 

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

6. **Software Support** (`.../irq.h`):
    - C functions for CLINT configuration and control.

The implementation of the CLINT design is compliant with both the older SiFive CLINT design and the newer [RISC-V ACLINT specification](https://github.com/riscvarchive/riscv-aclint).

#### CLIC 

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

7. **Software Support** (`.../irq.h`):
    - C functions for CLIC configuration and control.
    - Interrupt enable/disable, priority setting, attribute configuration.
    - Support for first 16 interrupts via direct CSR access.


The CLIC implementation is compliant with the [RISC-V Fast Interrupts (CLIC) specification](https://github.com/riscv/riscv-fast-interrupt) as listed below:

  - 64 local interrupts with individual control (clicintattr, clicintip, clicintie, cliciprio)
  - Priority-based arbitration with 8-bit priority levels
  - mithreshold CSR for interrupt filtering
  - Vectored interrupt mode support in mtvec
  - Trigger type configuration for edge/level detection

Some other features from the specification can be added later and currently not supported:

  - No nested preemption support (missing context preservation)
  - No CLIC vector table mode (mtvec.mode=11)
  - No interrupt claiming protocol
  - Missing several CLIC extensions (Smclicsehv, Sditrig, Smtp, Smcspsw)