# Footer

## Introduction

By integrating RISC-V CLIC (Core-Local Interrupt Controller) support into the LiteX SoC framework, we aim to enhance LiteX with modern interrupt handling capabilities that support  more advanced and flexible interrupt controller with features like nested interrupts, per-interrupt priority levels, and vectored interrupt handling.

### Features

* Up to 4096 interrupts.

* Each interrupt can have a configurable priority and trigger mode (level/edge).

* Supports vectored interrupt mode (faster response time).

* Designed to be memory-mapped and visible to software.

### Use Case: 

Embedded and real-time systems that need fine-grained interrupt control.

### Status: 

Still a draft specification (as of 06/2025), but adopted by some vendors like SiFive.