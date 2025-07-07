# Overview

This diagram shows how PLIC handles external interrupt distribution while CLIC provides advanced local interrupt management, creating a comprehensive interrupt handling solution for the Litex SOC.

## Architecture Diagram

The following diagram illustrates the comprehensive interrupt handling architecture, showing how PLIC manages external interrupt sources while CLIC provides advanced local interrupt management for the CPU core.


``` bash
┌──────────────────────────────────────────────────────────────┐
│                  Litex SOC with PLIC + CLIC                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  External Interrupt Sources                                  │
│  ┌───────────────────────┐                                   │
│  │ interrupts[31:1]      │                                   │
│  │ • UART                │                                   │
│  │ • GPIO                │                                   │
│  │ • Ethernet            │                                   │
│  │ • DMA                 │                                   │
│  │ • ...                 │                                   │
│  └───────────┬───────────┘                                   │
│              │                                               │
│              ▼                                               │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                PLIC Controller                        │   │
│  │  ┌─────────┐    ┌─────────────┐    ┌───────────────┐  │   │
│  │  │ Gateway │    │  Priority   │    │   Targets     │  │   │
│  │  │ Logic   │    │ Arbitration │    │ ┌────┬──────┐ │  │   │
│  │  │         │───▶│  Tree-based │───▶│ │ M  │ S    │ │  │   │
│  │  │ Edge    │    │  Priority   │    │ │Mode│Mode  │ │  │   │
│  │  │ Detect  │    │  Selection  │    │ └─┬──┴──┬───┘ │  │   │
│  │  └─────────┘    └─────────────┘    └───┼─────┼─────┘  │   │
│  │                                        │     │        │   │
│  └────────────────────────────────────────┼─────┼────────┘   │
│                                           │     │            │
│  Local Interrupt Sources:                 │     │            │
│  ┌───────────────────────┐                │     │            │
│  │ • Timer Compare       │                │     │            │
│  │   (MTIMECMP vs MTIME) │                │     │            │
│  │ • Software Trigger    │                │     │            │
│  │   (MSIP register)     │                │     │            │
│  └───────────┬───────────┘                │     │            │
│              │                            │     │            │
│              ▼                            ▼     ▼            │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                  Riscv CPU Core                       │   │
│  │                                                       │   │
│  │  Interrupt Interfaces:         Memory Interfaces:     │   │
│  │  ┌─────────────────────┐       ┌───────────────────┐  │   │
│  │  │ PLIC:               │       │ • iBus            │  │   │
│  │  │ • Machine External  │       │ • dBus            │  │   │
│  │  │ • Supervisor Ext    │       │                   │  │   │
│  │  │                     │       │ Cache: I/D$ 4KB   │  │   │
│  │  │ CLIC:               │       │ Width: 32-bit     │  │   │
│  │  │ • interrupt_valid   │       └───────────────────┘  │   │
│  │  │ • interrupt_id[7:0] │                              │   │
│  │  │ • interrupt_level   │                              │   │
│  │  │ • interrupt_priv    │                              │   │
│  │  │ • mtvec_addr        │                              │   │
│  │  │ • mtvec_mode        │                              │   │
│  │  └─────────────────────┘                              │   │
│  │                                                       │   │
│  │  Additional CSRs:                                     │   │
│  │  • mintthresh, mtvt, mnxti, mintstatus                │   │
│  │  • mscratchcsw, mnscratchcsw                          │   │
│  │                                                       │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```


Benefits of PLIC + CLIC Architecture:

* PLIC: System-wide external interrupt distribution and prioritization
* CLIC: Advanced per-hart interrupt management with vectoring and preemption
* Unified: Single interrupt interface to CPU with enhanced capabilities
* Scalable: Easy to extend to multiple cores while maintaining per-hart CLIC benefits
