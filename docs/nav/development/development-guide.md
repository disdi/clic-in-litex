# Milestones

## CPU Implementation

For detailed information about implementing the CLINT/CLIC interface in a RISC-V CPU, see the [CPU Implementation Guide](cpu-implementation-guide.md).

## Litex Implementation

[Add RISC-V CLIC and CLINT interrupt controller support](https://github.com/enjoy-digital/litex/pull/2260) has been posted to support for the RISC-V Core Local Interrupt Controller (CLIC) and the CLINT (Core Local Interruptor) in the LiteX SoC framework.

## Zephyr Implementation

[Add Litex CLIC support to Zephyr](https://github.com/zephyrproject-rtos/zephyr/pull/94853) has been posted to support for the RISC-V Core Local Interrupt Controller (CLIC) for LiteX SoC framework in Zephyr RTOS.

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

#### CLINT Software Integration in Litex

1. **Software Driver** (`.../irq.h`, `.../clint.h`):
    - Provides generic Interrupt Service Routines (ISRs) for handling timer and software interrupts.
    - Includes C functions for configuring and controlling the CLINT via `clint.h`.

2. **Software Demo Application** (`clint_demo.c`):
    - Demonstrates triggering and handling software interrupts using the CLINT.
    - Offers a practical example of utilizing the CLINT C API.

#### CLIC Software Integration in Litex

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

## Linux Implementation

VexRiscv-SMP Litex SOC which is capable of booting Linux already supports CLINT Interrupt Controller.
CLIC implementation has been added to VexRiscv-SMP Litex SOC with below Pull-Request:


- [Adding CLIC support to VexRiscv SMP CPU](https://github.com/litex-hub/linux-on-litex-vexriscv/pull/438).
- [Adding CLIC support to Linux-on-LiteX SoC](https://github.com/litex-hub/pythondata-cpu-vexriscv_smp/pull/10).
- [Adding CLIC support to RISCV Opensbi](https://github.com/litex-hub/opensbi/pull/2)


---

### Hardware Changes

---

#### Summary of Changes:

1. ##### VexRiscv SMP CPU Core

    - **`VexRiscv/src/main/scala/vexriscv/demo/smp/VexRiscvSmpLitexCluster.scala`**
        - Added command-line option `--with-clic`
        - Modified CSR configuration to use `CsrPluginConfig.withClic()` when enabled

2. ##### Litex SOC with VexRiscv SMP CPU Core

    - **`litex/litex/soc/cores/cpu/vexriscv_smp/core.py`**
        - Added CLIC support detection and signal creation
        - Added `--with-clic` command-line argument to pass it to Verilog generator

3. ##### Linux-on-LiteX Integration

    - **`linux-on-litex-vexriscv/sim.py`**
        - Sets `VexRiscvSMP.with_clic = True` before SoC creation
        - Adds CLIC controller to simulated SoC when `--with-clic` is specified

    - **`linux-on-litex-vexriscv/make.py`**
        - Similar CLIC integration for hardware builds
        - Validates CPU has CLIC support before adding controller

---

### Software Changes

---

#### Summary of Changes:

1. ##### CLIC Software Integration in Opensbi

    - **`opensbi/platform/litex/vexriscv/platform.c`**
        - Added CLIC support detection and handling interrupts

2. ##### CLIC Node Generation in Device Tree

    - **`litex/litex/soc/cores/cpu/vexriscv_smp/core.py`**
        - Added `clic_base = 0xf200_0000`
        - Updated `mem_map` property to include CLIC when enabled

    - **`litex/litex/soc/integration/soc.py`**
        - Modified `add_clic()` to add CLIC memory region to bus
        - Added `self.bus.add_region("clic", SoCRegion(...))` for proper device tree generation

    - **`litex/litex/soc/integration/soc_core.py`**
        - Updated CLIC initialization to use CPU's CLIC base address from memory map

    - **`litex/litex/tools/litex_json2dts_linux.py`**
        - Added complete CLIC device tree generation support
        - Updated interrupt parent references to use CLIC when available

3. Kernel Driver - *PENDING*

---

### Testing

---

#### Summary of Changes:

###### LiteX-Generated CLIC DUT Test Framework

A complete cocotb test framework for CLIC using LiteX-generated DUT has been created :

- [CLIC Cocotb Test Framework](https://github.com/disdi/cocotbext-clic)

##### Components Created

###### 1. LiteX DUT Generator (`wrappers/generate_clic.py`)
- **Purpose**: Generates CLIC hardware using LiteX framework
- **Features**:
  - Full CLIC implementation from `litex.soc.cores.clic`
  - Wishbone slave interface for CSR access
  - Configurable number of interrupts (default: 16)
  - Proper CSR memory mapping at 0xf0c00000
  - Complete interrupt signaling interface

###### 2. Generated Files
- **`build_clic/gateware/dut.v`**: Complete CLIC Verilog implementation (~106KB)
- **`csr_clic.csv`**: CSR register map with all CLIC registers
- **`tb_clic_litex.v`**: Testbench wrapper for cocotb compatibility

###### 3. Test Infrastructure
- **`test_clic_litex.py`**: Main test suite with 7 test functions
- **`tests/test_clic_litex_basic.py`**: Basic functionality tests
- **`tests/test_clic_litex_priority.py`**: Priority arbitration tests  
- **`tests/test_clic_litex_csr.py`**: CSR access tests
- **`tests/test_clic_litex_performance.py`**: Performance measurement tests

##### How It Works

###### LiteX Generation Process
```python
# The generate_clic.py script:
1. Creates a CLICTestSoC with CLIC module
2. Maps CSR registers at 0xf0c00000
3. Connects wishbone interface
4. Wires CLIC interrupt signals
5. Generates synthesizable Verilog
```

###### Test Flow
```python
1. Generate DUT: python3 wrappers/generate_clic.py
2. Compile: pytest test_clic_litex.py::test_compile_litex_clic
3. Test: pytest test_clic_litex.py::test_litex_clic_basic
```

##### Test Coverage

###### Functional Tests

✅ **Compilation**: Successful

✅ **Basic Test**: Interrupt generation and acknowledgment

✅ **Individual Interrupts**: Parameterized testing (0-3)

✅ **CSR Access**: Wishbone register read/write

✅ **Priority Arbitration**: Multi-interrupt priority handling

###### Performance Tests

✅ **Interrupt Latency**: Time required to handle interrupts

✅ **Interrupt Throughput**: Interrupts per second measurement

✅ **Priority Switch Time**: Time required to switch between interrupts   

✅ **Acknowledgment Time**: Time required to acknowledge an interrupt

---

## CLIC Integration with Full System

---

LiteX-generated CLIC can be integrated into a complete SoC:

```python
from litex.soc.cores.clic import CLIC

class MySoC(SoCCore):
    def __init__(self):
        # Add CLIC to your SoC
        self.submodules.clic = CLIC(num_interrupts=64)
        self.clic.add_csr_interface(self)
        
        # Connect to CPU
        self.cpu.clicInterrupt.eq(self.clic.clicInterrupt[0])
        # ... other connections
```


