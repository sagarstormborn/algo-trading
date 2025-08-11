# NautilusTrader Reference Guide

This document provides a quick reference to the NautilusTrader repository structure and key components for understanding and learning purposes.

## Repository Location
The NautilusTrader repository is cloned in: `temp/nautilus_trader/`

## What is NautilusTrader?

NautilusTrader is a high-performance, production-grade algorithmic trading platform written in Python, Cython, and Rust. It provides:

- **Event-driven backtesting** with nanosecond precision
- **Live trading** with the same strategy code as backtesting
- **Multi-venue support** for various exchanges and data providers
- **AI-first design** for machine learning integration
- **Type safety** through Rust-powered core components

## Key Features

- **Fast**: Core written in Rust with async networking
- **Reliable**: Rust-powered type and thread safety
- **Portable**: Runs on Linux, macOS, and Windows
- **Flexible**: Modular adapters for any REST API or WebSocket
- **Advanced**: Multiple order types, time-in-force options, contingency orders
- **Multi-venue**: Support for market-making and arbitrage strategies

## Repository Structure

### Core Directories

```
nautilus_trader/
├── nautilus_trader/          # Main Python package
│   ├── adapters/             # Exchange and data provider integrations
│   ├── backtest/             # Backtesting engine
│   ├── data/                 # Data handling and streaming
│   ├── execution/            # Order execution and management
│   ├── indicators/           # Technical indicators
│   ├── live/                 # Live trading components
│   ├── model/                # Data models and types
│   ├── portfolio/            # Portfolio management
│   ├── risk/                 # Risk management
│   ├── strategies/           # Strategy framework
│   └── trading/              # Trading logic and components
├── examples/                 # Example strategies and usage
│   ├── backtest/             # Backtesting examples
│   ├── live/                 # Live trading examples
│   ├── sandbox/              # Sandbox environment examples
│   └── other/                # Miscellaneous examples
├── tests/                    # Test suite
├── docs/                     # Documentation
└── crates/                   # Rust crates (core components)
```

### Key Components

#### 1. **Adapters** (`nautilus_trader/adapters/`)
- Exchange integrations (Binance, Bybit, Interactive Brokers, etc.)
- Data provider integrations (Databento, Tardis, etc.)
- Each adapter provides unified interface for different venues

#### 2. **Data** (`nautilus_trader/data/`)
- Data streaming and handling
- Bar aggregation
- Tick data processing
- Historical data management

#### 3. **Execution** (`nautilus_trader/execution/`)
- Order management
- Position management
- Execution algorithms
- Order routing

#### 4. **Indicators** (`nautilus_trader/indicators/`)
- Technical analysis indicators
- Custom indicator framework
- Real-time calculation

#### 5. **Strategies** (`nautilus_trader/strategies/`)
- Strategy base classes
- Signal generation
- Risk management integration

#### 6. **Backtest** (`nautilus_trader/backtest/`)
- Historical data simulation
- Event-driven backtesting engine
- Performance analysis

## Example Strategies

### Simple EMA Cross Strategy
Location: `examples/backtest/crypto_ema_cross_ethusdt_trade_ticks.py`

This example demonstrates:
- Basic strategy implementation
- EMA indicator usage
- Order placement
- Position management

### Market Making Strategy
Location: `examples/backtest/fx_market_maker_gbpusd_bars.py`

This example shows:
- Market making logic
- Bid/ask spread management
- Risk controls

## Installation and Setup

### Prerequisites
- Python 3.11-3.13
- Rust 1.89.0+ (for compilation)
- uv package manager (recommended)

### Quick Installation
```bash
# Clone the repository
git clone --branch develop --depth 1 https://github.com/nautechsystems/nautilus_trader.git

# Install with uv
cd nautilus_trader
uv sync --all-extras
```

### Using Makefile
```bash
# Install in release mode
make install

# Install in debug mode
make install-debug

# Build only
make build

# Run tests
make pytest
```

## Learning Path

1. **Start with Examples**: Begin with simple backtesting examples
2. **Understand Data Flow**: Learn how data flows through the system
3. **Study Indicators**: Explore technical indicators and custom indicators
4. **Build Simple Strategies**: Create basic strategies using the framework
5. **Explore Live Trading**: Move to live trading with paper accounts
6. **Advanced Features**: Dive into multi-venue, custom components, etc.

## Key Concepts

### Event-Driven Architecture
- All operations are event-driven
- Events flow through the system asynchronously
- Enables high-performance processing

### Strategy Framework
- Inherit from `Strategy` base class
- Implement `on_start()`, `on_stop()`, event handlers
- Use indicators for signal generation
- Manage positions and orders

### Data Types
- `Bar`: OHLCV data
- `Tick`: Trade or quote tick data
- `OrderBook`: Market depth data
- `Position`: Current position information
- `Order`: Order details and status

### Order Types
- Market, Limit, Stop orders
- Time in force: IOC, FOK, GTC, GTD, DAY
- Contingency orders: OCO, OTO, OUO
- Execution instructions: post-only, reduce-only

## Useful Commands

```bash
# Run a backtest example
python examples/backtest/crypto_ema_cross_ethusdt_trade_ticks.py

# Build documentation
make docs

# Run performance tests
make test-performance

# Clean build artifacts
make clean
```

## Documentation Links

- **Official Docs**: https://nautilustrader.io/docs/
- **Installation Guide**: https://nautilustrader.io/docs/latest/getting_started/installation
- **Examples**: https://nautilustrader.io/docs/latest/examples/
- **API Reference**: https://nautilustrader.io/docs/latest/api/

## Community

- **Discord**: https://discord.gg/NautilusTrader
- **GitHub**: https://github.com/nautechsystems/nautilus_trader
- **Website**: https://nautilustrader.io

## Notes

- The repository is actively developed with bi-weekly releases
- API may change between versions until v2.x stable release
- Use `develop` branch for latest features
- Use `master` branch for production stability