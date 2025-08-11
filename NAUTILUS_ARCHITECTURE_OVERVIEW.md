# NautilusTrader Architecture Overview

## High-Level Architecture

NautilusTrader follows an **event-driven, actor-based architecture** with clear separation of concerns. The system is built around a central **NautilusKernel** that orchestrates all components through message passing.

```
┌─────────────────────────────────────────────────────────────────┐
│                        NAUTILUS KERNEL                          │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   CLOCK     │  │  MESSAGE    │  │    CACHE    │  │ LOGGER  │ │
│  │             │  │    BUS      │  │             │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        CORE ENGINES                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │    DATA     │  │ EXECUTION   │  │    RISK     │  │PORTFOLIO│ │
│  │   ENGINE    │  │   ENGINE    │  │   ENGINE    │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TRADING COMPONENTS                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │  STRATEGIES │  │  TRADER     │  │ CONTROLLER  │  │ADAPTERS │ │
│  │             │  │             │  │             │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components & Their Roles

### 1. **NautilusKernel** (`system/kernel.py`)
- **Role**: Central orchestrator and system coordinator
- **Responsibilities**:
  - Manages the event loop and async operations
  - Coordinates all engines and components
  - Handles system startup/shutdown
  - Provides message bus and cache access
  - Manages logging and configuration

### 2. **Core Infrastructure** (`core/`)
- **Clock**: Time management (live vs backtest)
- **Message Bus**: Event routing and communication
- **Cache**: State persistence and data storage
- **UUID**: Unique identifier generation
- **Data Types**: Core data structures (Price, Quantity, Money)

### 3. **Data Engine** (`data/engine.pyx`)
- **Role**: Data ingestion, processing, and distribution
- **Responsibilities**:
  - Receives market data from adapters
  - Aggregates ticks into bars
  - Distributes data to strategies
  - Manages data subscriptions
  - Handles historical data loading

### 4. **Execution Engine** (`execution/engine.pyx`)
- **Role**: Order management and execution
- **Responsibilities**:
  - Receives orders from strategies
  - Routes orders to venues via adapters
  - Manages order lifecycle
  - Handles order confirmations and fills
  - Provides execution algorithms

### 5. **Risk Engine** (`risk/engine.py`)
- **Role**: Risk management and position monitoring
- **Responsibilities**:
  - Validates orders against risk limits
  - Monitors position exposures
  - Enforces trading rules
  - Provides risk metrics

### 6. **Portfolio** (`portfolio/portfolio.py`)
- **Role**: Account and position management
- **Responsibilities**:
  - Tracks account balances
  - Manages positions across venues
  - Calculates P&L
  - Handles margin requirements

## Component Interactions & Data Flow

### 1. **System Initialization Flow**
```
1. NautilusKernel.start()
   ├── Initialize Clock, MessageBus, Cache, Logger
   ├── Start Data Engine
   ├── Start Execution Engine  
   ├── Start Risk Engine
   ├── Initialize Portfolio
   └── Start Trader
```

### 2. **Market Data Flow**
```
External Data Source
        │
        ▼
   Adapter (Binance, Bybit, etc.)
        │
        ▼
   Data Engine
        │
        ▼
   Message Bus
        │
        ▼
   Strategies ←── Indicators
        │
        ▼
   Order Generation
```

### 3. **Order Execution Flow**
```
Strategy
    │
    ▼
Order Command
    │
    ▼
Execution Engine
    │
    ▼
Risk Engine (Validation)
    │
    ▼
Adapter (Venue)
    │
    ▼
Exchange
    │
    ▼
Execution Report
    │
    ▼
Portfolio Update
```

### 4. **Event-Driven Communication**
All components communicate through the **Message Bus** using typed messages:

- **Commands**: Instructions to perform actions
- **Events**: Notifications of state changes
- **Requests**: Queries for information
- **Responses**: Answers to requests

## Key Design Patterns

### 1. **Actor Model**
- Each component is an actor with its own state
- Communication through message passing
- Isolation and concurrency safety

### 2. **Event Sourcing**
- All state changes are events
- Events are persisted and replayable
- Enables backtesting and audit trails

### 3. **Dependency Injection**
- Components receive dependencies through configuration
- Enables testing and modularity
- Clear separation of concerns

### 4. **Strategy Pattern**
- Trading strategies inherit from base Strategy class
- Pluggable strategy implementations
- Consistent interface across backtest and live

## Code Organization

### **Layer 1: Core Infrastructure**
```
core/
├── datetime.pyx      # Time handling
├── message.pyx       # Message types
├── uuid.pyx          # Unique identifiers
├── correctness.pyx   # Validation
└── nautilus_pyo3.pyi # Rust bindings
```

### **Layer 2: System Management**
```
system/
├── kernel.py         # Main orchestrator
└── config.py         # Configuration
```

### **Layer 3: Domain Engines**
```
data/engine.pyx       # Data processing
execution/engine.pyx  # Order execution
risk/engine.py        # Risk management
portfolio/portfolio.py # Account management
```

### **Layer 4: Trading Logic**
```
trading/
├── strategy.pyx      # Strategy base class
├── trader.py         # Trading coordination
└── controller.py     # System control
```

### **Layer 5: External Integration**
```
adapters/             # Exchange integrations
live/                 # Live trading components
backtest/             # Backtesting engine
```

## Example: Simple Strategy Flow

```python
# 1. Strategy receives market data
def on_trade_tick(self, tick: TradeTick):
    # 2. Update indicators
    self.fast_ema.update_raw(tick.price)
    self.slow_ema.update_raw(tick.price)
    
    # 3. Generate signals
    if self.fast_ema.value > self.slow_ema.value:
        # 4. Submit order
        self.submit_order(
            order=self.order_factory.market(
                instrument_id=tick.instrument_id,
                order_side=OrderSide.BUY,
                quantity=Quantity(100),
            )
        )
```

## Performance Characteristics

### **High Performance**
- Core components written in Rust/Cython
- Async/await for non-blocking I/O
- Zero-copy data structures
- Efficient memory management

### **Scalability**
- Actor-based concurrency
- Message-driven architecture
- Horizontal scaling possible
- Stateless components

### **Reliability**
- Type safety through Rust
- Comprehensive error handling
- State persistence
- Audit trails

## Development Workflow

### **Backtesting**
1. Configure BacktestEngine
2. Add historical data
3. Add strategies
4. Run simulation
5. Analyze results

### **Live Trading**
1. Configure LiveEngine
2. Connect to venues
3. Deploy strategies
4. Monitor execution
5. Manage risk

## Key Benefits of This Architecture

1. **Separation of Concerns**: Each component has a single responsibility
2. **Testability**: Components can be tested in isolation
3. **Extensibility**: Easy to add new strategies, adapters, or components
4. **Performance**: Optimized for high-frequency trading
5. **Reliability**: Type safety and error handling
6. **Flexibility**: Works for backtesting and live trading
7. **Scalability**: Can handle multiple venues and strategies
