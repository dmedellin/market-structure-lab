# Market Structure Lab

`market-structure-lab` is the repository, the application slug and the image
title. What it publishes at `https://learn.geterdone.io/` is a **library of
learning paths** — eight interactive courses and 118 lessons today, all of them
on one subject, whose path is now complete end to end, with more subjects
planned. Every page is a single HTML file with its CSS, JavaScript and graphics
inline — it loads no fonts, no frameworks, no analytics, and no third-party
requests of any kind.

## The paths layer

A **path** is an ordered sequence of courses on one subject. The library is
organized around that idea rather than around any one subject:

| URL | What it is |
| --- | --- |
| `/` | the **site index**: every path, plus search across every published course |
| `/paths/<subject>/` | one **path page**: that subject's courses, in order |
| `/<course>/` | a **course home** |
| `/<course>/<lesson>/` | a **lesson** |

The site index and the path pages are **shared chrome and subject-agnostic**. The
owner plans paths for mathematics, computer science and philosophy, and those
paths reuse this frame unchanged: nothing in the index, in a path page, in a
footer or in site metadata may assume the subject is trading. Only course and
lesson pages are subject-specific. The invariant suite enforces exactly that
(`TestSharedChromeIsSubjectAgnostic`), including the rule that the index never
writes "the path" — it holds paths, plural.

A path page is **neither a course home nor a lesson**, even though it sits two
segments deep like a lesson does. Every guard declares it separately
(`PATH_PAGE`) rather than classifying pages by URL shape.

## The trading path — eight courses, all published

`https://learn.geterdone.io/paths/trading/` is the ordered path. Course 1 teaches
you to read what price is doing; course 2 turns that read into a plan you can
size, place, manage and review; course 3 takes that plan into options, where the
instrument itself carries risk the stock chart does not show; course 4 is the
indicator toolkit and how to state a rule precisely; course 5 is what traded
volume and order flow show about participation, value and executed flow — and
what they do not; course 6 decides what a trade may cost before it is taken, in
risk budget, stop distance, position size, drawdown and ruin; course 7 asks
whether the whole rule set ever worked, and what a backtest can and cannot
establish; and course 8 builds the system that would run it — architecture,
market data, scheduling, signal and risk engines, broker APIs, order management,
paper trading, reliability, observability, secrets and kill switches, deployment,
where AI belongs, and one versioned production specification. A reader is
expected to walk them in order, which is why the courses share one theme setting,
one visual system, one navigation model, and one set of guards — and why every
course home says which number it is (`Course N of 8`) and links to its
neighbours.

| # | Course | Lessons | URL | Status |
| --- | --- | --- | --- | --- |
| 1 | Market Structure | 7 | `/market-structure/` | published |
| 2 | Trade Setup and Execution | 15 | `/trade-setup-execution/` | published |
| 3 | Options Trading | 16 | `/options-trading/` | published |
| 4 | Technical Indicators | 16 | `/technical-indicators/` | published |
| 5 | Volume and Order Flow | 16 | `/volume-and-order-flow/` | published |
| 6 | Trading Risk Management | 16 | `/trading-risk-management/` | published |
| 7 | Backtesting and Trading Systems | 16 | `/backtesting-and-trading-systems/` | published |
| 8 | Algorithmic and Automated Trading | 16 | `/algorithmic-and-automated-trading/` | published |

**The trading path is complete.** All eight courses are published; there is no
announced-but-unpublished entry left anywhere in this repository, and no ninth
course was ever announced, so nothing reserves a slot for one. Courses 5, 6, 7
and finally 8 each left the announced group the day their pages landed; the move
was always one-way, and course 8 was the last one this path will make.
`TestPathIsComplete` fails the build if any page still calls a course upcoming,
or if any availability count reads as a fraction of the path.

Course 1 was published at `/market-structure-lab/` until the paths layer landed.
That slug names the repository and the application, not the course, so the course
took its own name. **The old URLs are gone**, with no redirect stubs.

### Course 1 — Market Structure (7 lessons)

How price actually moves: structure, ranges and liquidity, multi-timeframe
alignment, entry models, invalidation and reward-to-risk, participation, and
finally how the read maps onto an options contract.

| # | Lesson |
| --- | --- |
| 01 | Market Structure Lab |
| 02 | Ranges, Breakouts & Liquidity Sweeps Lab |
| 03 | Multi-Timeframe Market Structure Lab |
| 04 | Pullbacks & Entry Models Lab |
| 05 | Invalidation, Stops & Reward-to-Risk Lab |
| 06 | Volume & Relative Strength Lab |
| 07 | Options Contract Selection Lab |

### Course 2 — Trade Setup and Execution (15 lessons)

Turning a read into an executed, reviewed trade: thesis, levels, confluence, the
three setup families, entry confirmation, stops, targets, reward-to-risk, sizing,
management, backtesting, journaling, and performance review.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Trade Thesis | Build a conditional trade plan from context, setup, trigger, invalidation, target, and no-trade conditions. |
| 02 | Support and Resistance | Place support and resistance zones, classify reactions, and distinguish rejection from acceptance and role reversal. |
| 03 | Confluence | Evaluate setup quality using independent evidence from context, location, trigger, participation, and relative performance. |
| 04 | Breakout Setups | Replay confirmed, retested, failed, and crowded breakouts and evaluate entry, wait, or no-trade decisions. |
| 05 | Pullback Setups | Explore pullback depth, structural validity, reaction evidence, and local structure shifts. |
| 06 | Reversal Setups | Advance through trend maturity, reaction, structure break, retest, and continuation. |
| 07 | Entry Confirmation | Compare reaction, structure-shift, and retest entry models and select the first candle that satisfies each rule. |
| 08 | Stop-Loss Placement | Drag a stop around structural invalidation and see how distance changes illustrative position size. |
| 09 | Profit Targets | Place structural targets, compare R multiples, and evaluate single-target, scale-out, and trailing plans. |
| 10 | Risk-to-Reward | Calculate risk, reward, break-even win rate, and expectancy for adjustable long and short plans. |
| 11 | Position Sizing | Calculate maximum share and long-option quantities from equity, risk percentage, stop distance, premium loss, and costs. |
| 12 | Trade Management | Simulate holding, scaling, break-even stops, trailing, and exits while scoring adherence to a plan. |
| 13 | Backtesting | Generate synthetic trade samples, inspect equity, drawdown, distributions, and compare in-sample with out-of-sample. |
| 14 | Trading Journal | Create, edit, store, import, and export structured journal entries with R outcomes, adherence, and mistake tags. |
| 15 | Performance Review | Import journal data, filter and segment performance, diagnose recurring mistakes, and generate one improvement rule. |

Course 2 ships one supporting file, `trade-journal-schema.json`. Lesson 14
exports `trade-journal-v1` JSON, lesson 15 imports that export directly, and the
schema documents the exchange shape. It is published like any other URL and is
checked by every guard listed below — as JSON, not as a page.

### Course 3 — Options Trading (16 lessons)

The contract itself: what an option is, what it costs and why, how its value
moves with price, time and volatility, the core single-leg and two-leg
strategies, and what actually happens at expiration.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Options Contract Fundamentals | Decode option contract terms, holder rights, writer obligations, multipliers, premium cash flow, and expiration payoff. |
| 02 | Calls and Puts | Compare long and short calls and puts using rights, obligations, payoff charts, breakeven, and maximum risk. |
| 03 | Moneyness | Classify calls and puts as ITM, ATM, or OTM and calculate intrinsic value from stock and strike. |
| 04 | Option Premium | Decompose theoretical option premium into intrinsic and extrinsic value and change core pricing inputs. |
| 05 | Option Chain and Liquidity | Read option-chain fields, quantify bid-ask friction, inspect activity, and evaluate a limit-order selection. |
| 06 | Expiration and Time Decay | Visualize long-option value by days remaining and inspect theoretical theta, intrinsic value, and extrinsic value. |
| 07 | Implied Volatility | Model option-value changes from IV expansion and contraction separately from underlying movement. |
| 08 | Delta and Gamma | Compare delta-only and delta-plus-gamma estimates with full theoretical repricing and visualize delta across stock prices. |
| 09 | Theta and Vega | Apply time and IV shocks, compare theta-plus-vega estimates with full repricing, and visualize volatility-dependent decay. |
| 10 | Long Calls and Long Puts | Plan long calls and puts with expiration breakeven, premium risk, modeled early-exit value, and payoff charts. |
| 11 | Covered Calls | Build covered calls, compare them with stock-only payoff, and calculate breakeven, maximum profit, and downside risk. |
| 12 | Cash-Secured Puts | Calculate cash reservation, effective purchase price, payoff, maximum premium profit, and downside risk for cash-secured puts. |
| 13 | Vertical Debit Spreads | Construct bull call and bear put debit spreads and calculate debit, breakeven, maximum loss, and maximum profit. |
| 14 | Vertical Credit Spreads | Construct bull put and bear call credit spreads and calculate credit, breakeven, maximum profit, and maximum loss. |
| 15 | Exercise, Assignment, and Expiration | Simulate expiration outcomes, exercise and assignment obligations, resulting shares, and broker-handling risks. |
| 16 | Options Trade Planning | Score a complete options plan across thesis, strategy fit, timing, spread, risk budget, event exposure, and exit rules. |

Course 3 ships one supporting file, `options-trade-plan-schema.json`. Lesson 16
scores a complete options plan and exports it as `options-trade-plan-v1` JSON;
the schema documents that shape. Like course 2's journal schema it is published
as a real URL and checked as JSON, never as a page.

Course 3 also carries outbound reference links to four authoritative,
non-commercial sources — the Options Industry Council (`optionseducation.org`),
FINRA, the SEC's `investor.gov`, and Cboe. They are reviewed origins listed in
`ci.yml`; a link navigates and loads nothing, so the pages stay self-contained.

### Course 4 — Technical Indicators (16 lessons)

`https://learn.geterdone.io/technical-indicators/`

The measurement toolkit, and how to state a rule precisely enough to hand to a
machine. Sixteen lessons: what an indicator is computed from, moving averages and
their crossovers, RSI, the stochastic oscillator, MACD, ADX, average true range,
Bollinger, Keltner and Donchian channels, rate of change, divergence, then how to
combine indicators without redundancy, choose them by market regime, and turn an
observation into an unambiguous condition.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Technical Indicator Fundamentals | Show how an indicator transforms historical price data, why lookback length changes responsiveness, and why a reading is only meaningful in context. |
| 02 | Simple and Exponential Moving Averages | Calculate and compare simple and exponential moving averages, and see how source and lookback change responsiveness. |
| 03 | Moving Average Trend Filters and Crossovers | Use fast and slow averages as a trend-state model, detect crossovers, and separate delayed confirmation from prediction. |
| 04 | Relative Strength Index | Calculate RSI with Wilder smoothing and test threshold behaviour across regimes without treating extremes as reversal commands. |
| 05 | Stochastic Oscillator | Measure where the close sits inside its recent range and compare %K and %D smoothing in trends and in ranges. |
| 06 | Moving Average Convergence Divergence | Separate the MACD line, signal line and histogram, change the three periods, and identify zero-line and signal-line events. |
| 07 | Average Directional Index and Directional Movement | Calculate +DI, −DI and ADX, and distinguish directional dominance from trend strength. |
| 08 | Average True Range | Inspect true range, see how gaps affect volatility measurement, and keep volatility separate from direction. |
| 09 | Bollinger Bands | Build a standard-deviation envelope, inspect band width and %B, and read contraction and expansion. |
| 10 | Keltner Channels | Construct an EMA-centred ATR envelope, compare it with Bollinger Bands, and define channel-break conditions precisely. |
| 11 | Donchian Channels | Track rolling highs and lows, compare current-bar and prior-channel calculations, and detect completed breakouts. |
| 12 | Rate of Change and Momentum | Measure change over a fixed lookback in percentage and absolute terms, and separate momentum from direction. |
| 13 | Indicator Divergence | Compare aligned price and indicator swings, classify regular divergence, and require price confirmation. |
| 14 | Combining Indicators Without Redundancy | Group indicators by function, compare correlations, and avoid stacking transformations of the same behaviour. |
| 15 | Indicator Selection by Market Regime | Classify regimes, select indicators suited to the decision, and see why one threshold behaves differently in each. |
| 16 | Indicator-Based Trading Rules | Convert observations into deterministic conditions, detect contradictory rules, and export a machine-readable specification. |

Course 4 ships one supporting file, `indicator-rule-schema.json`. Lesson 16
exports a rule specification as `technical-indicator-rule-v1` JSON; the schema
documents that shape. Like the other six schemas it is published as a real URL
and checked as JSON, never as a page.

**Course 4's own scope and risk notice, stated on the page.** The course teaches
indicator calculation, interpretation and rule specification. It does **not**
provide live data, trading signals, profitability claims, or personalized
investment advice; backtesting, costs, robustness and automation belong to later
courses. Indicators transform historical price data and do not guarantee future
direction. All price series are synthetic and deterministic, and small
differences from a charting platform can come from source, seed, rounding,
missing-bar, adjustment or incomplete-bar conventions. Volume-derived tools
(VWAP, OBV, volume profile, cumulative delta, footprint charts, order-book
concepts) are deliberately reserved for course 5, which is now published at
`/volume-and-order-flow/`.

### Course 5 — Volume and Order Flow (16 lessons)

`https://learn.geterdone.io/volume-and-order-flow/`

What the participants are doing, not just what price did. Sixteen lessons: what
volume measures and how it pairs with price direction, relative volume and
spikes, confirmation, on-balance volume, accumulation/distribution and Chaikin
money flow, session and anchored VWAP, volume profile with its value area, POC,
HVN and LVN — then the execution side: bid, ask, spread and order types, time
and sales, footprint charts and bid-ask delta, cumulative volume delta, the
order book and market depth, and finally rules written from all of it.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Volume Fundamentals | Understand what volume measures, separate participation from direction, and read price progress together with trading activity. |
| 02 | Price and Volume Relationships | Interpret the four basic combinations of price direction and changing participation. |
| 03 | Relative Volume and Volume Spikes | Normalize current volume against a baseline and distinguish participation expansion from climax or absorption. |
| 04 | Volume Confirmation | Evaluate whether volume supports a breakout, continuation, rejection, or failed move. |
| 05 | On-Balance Volume | Use On-Balance Volume to accumulate volume by closing direction and compare its trend with price. |
| 06 | Accumulation/Distribution and Chaikin Money Flow | Measure where price closes inside each bar’s range and weight that location by volume. |
| 07 | Volume-Weighted Average Price | Calculate session VWAP and use price location around it to describe accepted value and directional control. |
| 08 | Anchored Volume-Weighted Average Price | Start VWAP from a selected event and evaluate whether price is accepted above or below the event’s average traded value. |
| 09 | Volume Profile | Organize traded volume by price rather than time and identify where the market spent activity. |
| 10 | Value Area, POC, HVN, and LVN | Interpret value-area boundaries, high-volume nodes, and low-volume nodes as auction locations. |
| 11 | Bid, Ask, Spread, and Order Types | Understand quoted prices, resting liquidity, marketable orders, and execution trade-offs. |
| 12 | Time and Sales | Read the transaction stream by price, size, side classification, pace, and price response. |
| 13 | Footprint Charts and Bid-Ask Delta | Compare executed volume at the bid and ask within each price level and candle. |
| 14 | Cumulative Volume Delta | Accumulate bid-ask delta through time and compare aggressive flow with price structure. |
| 15 | Order Book and Market Depth | Inspect resting liquidity, queue changes, spread, depth, and the difference between displayed intent and executed trades. |
| 16 | Volume and Order Flow Trading Rules | Convert market context, participation, aggressive flow, and price confirmation into explicit testable rules. |

Course 5 ships one supporting file, `volume-order-flow-rule-schema.json`. Lesson
16 exports a rule specification as `volume-order-flow-rule-v1` JSON; the schema
documents that shape. Like the other six schemas it is published as a real URL
and checked as JSON, never as a page.

Course 5 carries outbound reference links to two further origins: CME Group
(`cmegroup.com`) and Nasdaq (`nasdaq.com`), both exchanges' own material rather
than a vendor selling order-flow software. They are reviewed origins listed in
`ci.yml`, and that review records **unequal verification**, deliberately:
`nasdaq.com` answered HTTP 200 when it was checked; `cmegroup.com` answers 403 to
every automated request including one for its own root, which is WAF
bot-blocking rather than a dead link — so the four deep paths course 5 cites
**could not be verified** from an automated environment and remain unchecked as
paths. They are allowed on the strength of the origin being a primary source.

**Course 5's own scope and risk notice, stated on the page.** The course teaches
the interpretation of volume, value, executed flow and displayed depth. It does
**not** provide live market data, trading signals, execution access,
profitability claims, or personalized investment advice. Real outputs vary by
venue, feed, vendor, asset class, session, aggregation and classification
method; time-and-sales and footprint side classifications are simplified and
labelled as such, and the order book shows displayed liquidity, which can be
added, consumed, moved or cancelled. Position risk, portfolio risk and
risk-of-ruin belong to course 6; strategy validation belongs to course 7.

### Course 6 — Trading Risk Management (16 lessons)

`https://learn.geterdone.io/trading-risk-management/`

What a trade is allowed to cost, decided before it is taken. Sixteen lessons:
which risks can be controlled at all, the account risk budget and how it is
spread across trades, days and weeks, risk per trade, stops placed where the
thesis is invalid rather than where the loss feels tolerable, position sizing
that follows from those two, R-multiples and expectancy, losing streaks,
drawdown and risk of ruin, ATR-based sizing when volatility moves, gap,
slippage and execution risk, leverage and margin, correlation and portfolio
exposure, options-specific risk, hard daily and weekly limits, and a written
risk plan built from all of it.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Risk Management Fundamentals | Understand which trading risks can be controlled, define a planned loss, and separate market uncertainty from account damage. |
| 02 | Account Risk and Risk Budget | Allocate risk across individual trades, open positions, daily limits, and weekly limits without exceeding the account risk budget. |
| 03 | Risk Per Trade | Measure how fixed-percentage risk changes account decay, losing-streak impact, and the return required to recover. |
| 04 | Stop-Loss and Structural Invalidation | Place the stop where the trade thesis becomes invalid, then size the position to make that structural distance affordable. |
| 05 | Position Sizing | Calculate shares or contracts from account risk, entry price, stop price, contract multiplier, and estimated execution cost. |
| 06 | Reward-to-Risk and R-Multiples | Express trade outcomes in units of initial risk, compare targets consistently, and avoid confusing a large target with a high-quality setup. |
| 07 | Win Rate, Average Win/Loss, and Expectancy | Combine win rate, average win, average loss, and trading costs to estimate the average outcome per trade. |
| 08 | Losing Streaks and Drawdown | Measure peak-to-trough decline, understand recovery requirements, and distinguish normal strategy variance from unacceptable account damage. |
| 09 | Risk of Ruin | Estimate how strategy expectancy, payoff, risk per trade, and sequence variance affect the probability of crossing a failure threshold. |
| 10 | Volatility and ATR-Based Risk | Use recent price range and Average True Range to adapt stop distance and position size when market volatility changes. |
| 11 | Gap, Slippage, Liquidity, and Execution Risk | Model the difference between the planned stop and the actual fill when price gaps, spreads widen, or available liquidity is insufficient. |
| 12 | Leverage and Margin Risk | Understand how leverage magnifies equity changes, how margin requirements constrain positions, and why buying power is not a risk limit. |
| 13 | Correlation, Concentration, and Portfolio Exposure | Measure how positions that share sector, market, or factor exposure can behave like one oversized trade during stress. |
| 14 | Options Risk Management | Compare premium risk, assignment exposure, expiration behavior, volatility sensitivity, and defined versus undefined option risk. |
| 15 | Daily and Weekly Risk Limits | Use hard session and weekly limits to stop adding exposure after losses, execution errors, or unfavorable market conditions. |
| 16 | Trading Risk Plan | Combine account limits, position sizing, execution constraints, portfolio exposure, options rules, and review triggers into one testable risk specification. |

Course 6 ships one supporting file, `trading-risk-plan-schema.json`. Lesson 16
exports a risk plan as `trading-risk-plan-v1` JSON; the schema documents that
shape. Like the other six schemas it is published as a real URL and checked as
JSON, never as a page.

**Course 6's own scope and risk notice, stated on the page.** The course teaches
how risk is measured, sized and limited. It does **not** provide live market
data, trading signals, execution access, profitability claims, or personalized
investment advice. Every account curve, trade sequence, Monte Carlo path, option
payoff and portfolio shock is a deterministic synthetic example. Fixed-percentage
risk is applied to current equity, so dollar risk falls during a drawdown;
recovery gain is computed as `1 / (1 - drawdown) - 1`; and position size is
rounded down after entry-to-stop distance, contract multiplier and a slippage
reserve are included. Margin rules, assignment procedures and contract
specifications vary by broker and venue and must be verified independently.

### Course 7 — Backtesting and Trading Systems (16 lessons)

`https://learn.geterdone.io/backtesting-and-trading-systems/`

Whether the rule set ever worked, and what a historical test can and cannot
establish. Sixteen lessons: turning an idea into deterministic rules, historical
data quality, survivorship and corporate actions, bar construction and session
choice, look-ahead bias and data leakage, execution simulation, position sizing
and portfolio accounting, transaction costs and slippage, the trade log, equity
curve and drawdown, performance metrics and expectancy, benchmarking and
risk-adjusted comparison, in-sample versus out-of-sample data, walk-forward
testing, overfitting with sensitivity and Monte Carlo stress testing, and a
versioned system specification with a backtest report.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Backtesting Fundamentals | Use historical data to simulate a defined strategy, separate assumptions from results, and understand what a backtest can and cannot establish. |
| 02 | Testable Trading Rules and Hypotheses | Convert a market idea into deterministic entry, exit, sizing, and invalidation rules that produce the same decision from the same data. |
| 03 | Historical Data and Data Quality | Detect missing bars, duplicates, stale values, timestamp errors, and price outliers before they create false signals or distorted returns. |
| 04 | Survivorship, Selection, and Corporate Actions | Build a point-in-time universe, include failed and delisted instruments, and adjust splits and distributions without using information learned later. |
| 05 | Timeframes, Sessions, and Bar Construction | Define how raw trades or quotes become bars, which sessions are eligible, and how timeframe choices change indicators, signals, and fills. |
| 06 | Signal Timing, Look-Ahead Bias, and Data Leakage | Prevent the strategy from using future prices, completed-bar values, revised data, or preprocessing information that was unavailable at decision time. |
| 07 | Trade Execution Simulation | Model market, limit, stop, stop-limit, target, and cancellation behavior using prices that could realistically execute in the tested sequence. |
| 08 | Position Sizing and Portfolio Accounting | Track cash, equity, buying power, open positions, realized and unrealized P/L, rejected orders, and sizing rules throughout the test. |
| 09 | Transaction Costs, Spread, Slippage, and Liquidity | Deduct commissions, fees, bid-ask spread, slippage, and size-dependent market impact from every simulated entry, exit, and rebalance. |
| 10 | Trade Log, Equity Curve, and Drawdown | Create an auditable trade log, reconstruct portfolio equity through time, and measure peak-to-trough loss and recovery duration. |
| 11 | Performance Metrics and Expectancy | Calculate win rate, average win, average loss, expectancy, profit factor, return, volatility, trade frequency, and sample size without relying on one metric. |
| 12 | Benchmarking and Risk-Adjusted Performance | Compare the system with an appropriate benchmark and cash rate, then separate market exposure from independent performance and risk taken. |
| 13 | In-Sample, Validation, and Out-of-Sample Data | Separate rule development, parameter selection, and final evaluation so the last dataset remains unseen until the system is fixed. |
| 14 | Walk-Forward Testing | Repeat chronological training and test windows, choose parameters only from past data, and stitch the unseen test windows into one forward simulation. |
| 15 | Overfitting, Sensitivity, Monte Carlo, and Stress Testing | Test nearby parameters, resample trade sequences, increase costs, remove favorable periods, and verify that the result is not dependent on one precise historical path. |
| 16 | Trading System Specification and Backtest Report | Combine hypothesis, data, rules, execution, sizing, costs, validation, metrics, limits, and acceptance criteria into a versioned system specification and report. |

Course 7 ships one supporting file, `trading-system-specification-schema.json`.
Lesson 16 exports a system specification as `trading-system-specification-v1`
JSON; the schema documents that shape. Like the other six schemas it is
published as a real URL and checked as JSON, never as a page.

**Course 7's own scope and risk notice, stated on the page.** The course teaches
how a strategy is tested and reported. It does **not** provide live market data,
trading signals, execution access, profitability claims, or personalized
investment advice. Historical simulations are treated as hypothetical evidence,
never as predictions: signals are separated from order submission and execution,
and costs are applied at entries and exits rather than deducted from the final
result. Every price path, trade, universe, fill, cost, fold and Monte Carlo path
is a deterministic synthetic example, and a backtest result never establishes
future performance.

### Course 8 — Algorithmic and Automated Trading (16 lessons)

`https://learn.geterdone.io/algorithmic-and-automated-trading/`

The system that would run a strategy, and what running one unattended actually
requires. Sixteen lessons: choosing a level of automation and separating
strategy, signal, risk, order and execution responsibilities, system
architecture and ownership, market-data ingestion and normalization, exchange
calendars and deterministic scheduling, the signal engine and strategy state,
the portfolio and risk engine, broker APIs and the asynchronous order lifecycle,
order management and execution quality, paper trading and forward testing,
scanners, alerts and human approval, idempotency, bounded retries and recovery,
observability and an immutable audit trail, secrets, permissions and kill
switches, deployment, environments and rollback, where AI belongs in the
workflow and where it must not decide, and a versioned production-readiness
specification.

| # | Lesson | What it does |
| --- | --- | --- |
| 01 | Algorithmic and Automated Trading Fundamentals | Separate strategy rules, signal generation, risk checks, order submission, and execution, then choose the appropriate level of automation. |
| 02 | Trading System Architecture and Components | Define the services, boundaries, data stores, messages, and ownership required to move from market data to an auditable trading decision. |
| 03 | Market Data Ingestion and Normalization | Receive historical and streaming data, validate timestamps and symbols, remove duplicates, handle late events, and expose one normalized market-data model. |
| 04 | Time, Sessions, Events, and Scheduling | Use exchange calendars, time zones, session boundaries, event windows, and deterministic schedulers instead of assuming every day and minute is tradable. |
| 05 | Signal Engine and Strategy State | Convert normalized events into deterministic strategy-state transitions while preventing repeated, contradictory, or stale signals. |
| 06 | Portfolio, Position, and Risk Engine | Maintain authoritative cash, positions, exposure, open orders, and risk limits before any order is submitted. |
| 07 | Broker APIs and Order Lifecycle | Submit, query, cancel, and reconcile orders through a broker adapter while treating every response and status update as asynchronous state. |
| 08 | Order Management and Execution | Select order types, manage open orders, control participation, and measure fill quality against the decision price and available liquidity. |
| 09 | Paper Trading and Forward Testing | Run the complete system on current market data without live capital, then compare backtest assumptions with observed signals, latency, and simulated fills. |
| 10 | Scanners, Alerts, and Human Approval | Screen instruments, rank candidates, deduplicate alerts, communicate the exact thesis, and expire decisions that are no longer current. |
| 11 | Reliability, Idempotency, Retries, and Recovery | Design duplicate-safe commands, bounded retries, durable state, reconciliation, and restart behavior for uncertain networks and asynchronous broker updates. |
| 12 | Observability, Logging, and Auditability | Measure data freshness, decision latency, broker latency, error rate, positions, risk, and end-to-end traces while preserving an immutable decision audit trail. |
| 13 | Security, Secrets, Permissions, and Kill Switches | Protect broker credentials, restrict execution permissions, separate environments, audit access, rotate secrets, and provide immediate mechanisms to stop new trading. |
| 14 | Deployment, Environments, and Configuration | Build reproducible artifacts, separate development, paper, and live configuration, validate changes, deploy gradually, and roll back without changing trading state unexpectedly. |
| 15 | AI-Assisted and Agentic Trading Workflows | Use AI for research, extraction, classification, and trade proposals while keeping market data, rules, risk, permissions, and execution controls deterministic and auditable. |
| 16 | Automated Trading System Specification and Production Readiness | Combine strategy, data, architecture, risk, broker, reliability, security, deployment, observability, approval, and rollback requirements into one versioned production specification. |

Course 8 ships one supporting file, `automated-trading-system-schema.json`.
Lesson 16 exports a production specification as `automated-trading-system-v1`
JSON; the schema documents that shape. Like the other six schemas it is
published as a real URL and checked as JSON, never as a page.

Course 8 is the last course on the path. Its home links back to course 7 with
`rel=prev`; the forward half of its pager is **not** a disabled "course 9" slot,
because no ninth course was ever announced — it is a real link back to the path
page, deliberately without `rel=next`, since the path page is not the next
document in the sequence but the sequence itself.

**Course 8's own scope and risk notice, stated on the page.** The course is
educational. It does **not** connect to a broker, ingest live market data, place
orders, provide trading signals, or claim that any automated strategy will be
profitable, and no page in it can submit an order — every market path, event,
order, failure and portfolio state in it is a deterministic synthetic example.
The page states the point the rest of the course is built around: automating a
strategy does not reduce its risk. It removes the pause in which a person would
have noticed a stale price, a duplicated order, a wrong size or a broken
assumption, so an automated system can lose money faster and more consistently
than a manual one.

### Data and risk notice

All charts, trades, prices, fills, and performance results across all eight
courses are synthetic educational examples. The pages contain no live data and no
trading signals. Real outcomes can differ because of spread, slippage,
commissions, gaps, taxes, liquidity, assignment, exercise, implied volatility,
time decay, and other factors. Every course and lesson page carries an
`Educational use only` disclaimer and the invariant suite fails the build if one
loses it. The two shared-chrome pages are exempt by name, not by shape: a
subject-specific notice is not theirs to carry.

**Options carry their own risk notice, and course 3 states it on the page.**
Options involve risk and are not suitable for every investor. Course 3 is
educational and provides no personalized investment advice and no live trading
signals. Its demonstrations use synthetic prices and a simplified European
Black-Scholes model; they do not model every listed-product feature, dividend,
early-exercise decision, fee, tax, margin rule, or market microstructure effect.
Contract specifications and broker procedures must be verified independently.

## URL layout

The site is published under one subdomain, `learn.geterdone.io`. The URL space
has three kinds of page — the index, a path page, and a course with its lessons.

```text
/                                       the site index (paths + course search)
├── /paths/trading/                     the trading PATH PAGE — eight courses in
│                                       order, all eight published
├── /market-structure/                  course 1 home — lists its seven lessons
│   ├── /market-structure/market-structure/                     lesson 1.01
│   ├── … five more …
│   └── /market-structure/options-contract-selection/           lesson 1.07
├── /trade-setup-execution/             course 2 home — lists its fifteen lessons
│   ├── /trade-setup-execution/trade-thesis/                    lesson 2.01
│   ├── … thirteen more …
│   ├── /trade-setup-execution/performance-review/              lesson 2.15
│   └── /trade-setup-execution/trade-journal-schema.json        published asset
├── /options-trading/                   course 3 home — lists its sixteen lessons
│   ├── /options-trading/options-contract-fundamentals/         lesson 3.01
│   ├── … fourteen more …
│   ├── /options-trading/options-trade-planning/                lesson 3.16
│   └── /options-trading/options-trade-plan-schema.json         published asset
├── /technical-indicators/              course 4 home — lists its sixteen lessons
│   ├── /technical-indicators/technical-indicator-fundamentals/ lesson 4.01
│   ├── … fourteen more …
│   ├── /technical-indicators/indicator-based-trading-rules/    lesson 4.16
│   └── /technical-indicators/indicator-rule-schema.json        published asset
├── /volume-and-order-flow/             course 5 home — lists its sixteen lessons
│   ├── /volume-and-order-flow/volume-fundamentals/             lesson 5.01
│   ├── … fourteen more …
│   ├── /volume-and-order-flow/volume-and-order-flow-trading-rules/  lesson 5.16
│   └── /volume-and-order-flow/volume-order-flow-rule-schema.json    published asset
├── /trading-risk-management/           course 6 home — lists its sixteen lessons
│   ├── /trading-risk-management/risk-management-fundamentals/  lesson 6.01
│   ├── … fourteen more …
│   ├── /trading-risk-management/trading-risk-plan/             lesson 6.16
│   └── /trading-risk-management/trading-risk-plan-schema.json  published asset
├── /backtesting-and-trading-systems/   course 7 home — lists its sixteen lessons
│   ├── /backtesting-and-trading-systems/backtesting-fundamentals/   lesson 7.01
│   ├── … fourteen more …
│   ├── /backtesting-and-trading-systems/trading-system-specification-and-backtest-report/   lesson 7.16
│   └── /backtesting-and-trading-systems/trading-system-specification-schema.json  published asset
└── /algorithmic-and-automated-trading/ course 8 home — lists its sixteen lessons
    ├── /algorithmic-and-automated-trading/algorithmic-and-automated-trading-fundamentals/   lesson 8.01
    ├── … fourteen more …
    ├── /algorithmic-and-automated-trading/automated-trading-system-specification-and-production-readiness/  lesson 8.16
    └── /algorithmic-and-automated-trading/automated-trading-system-schema.json   published asset
```

`/paths/` belongs to the paths layer: no course may ever take that first segment,
and nothing is served at `/paths/` itself — the list of paths is the site index.
Every course on the path has its own URLs; nothing on the path page is an entry
without a page behind it.

**128 pages and seven assets. Nothing else is served:**

| # | URL | Page | Source |
| --- | --- | --- | --- |
| — | `https://learn.geterdone.io/` | Site index — the paths, plus course search | `site/index.html` |
| path | `https://learn.geterdone.io/paths/trading/` | **Trading path** — the eight courses in order | `site/paths/trading/index.html` |
| — | `https://learn.geterdone.io/market-structure/` | **Market Structure** — course 1 home | `site/market-structure/index.html` |
| 1.01 | `https://learn.geterdone.io/market-structure/market-structure/` | Market Structure Lab | `site/market-structure/market-structure/index.html` |
| 1.02 | `https://learn.geterdone.io/market-structure/ranges-breakouts-liquidity/` | Ranges, Breakouts & Liquidity Sweeps Lab | `site/market-structure/ranges-breakouts-liquidity/index.html` |
| 1.03 | `https://learn.geterdone.io/market-structure/multi-timeframe-market-structure/` | Multi-Timeframe Market Structure Lab | `site/market-structure/multi-timeframe-market-structure/index.html` |
| 1.04 | `https://learn.geterdone.io/market-structure/pullbacks-entry-models/` | Pullbacks & Entry Models Lab | `site/market-structure/pullbacks-entry-models/index.html` |
| 1.05 | `https://learn.geterdone.io/market-structure/invalidation-stops-risk-reward/` | Invalidation, Stops & Reward-to-Risk Lab | `site/market-structure/invalidation-stops-risk-reward/index.html` |
| 1.06 | `https://learn.geterdone.io/market-structure/volume-relative-strength/` | Volume & Relative Strength Lab | `site/market-structure/volume-relative-strength/index.html` |
| 1.07 | `https://learn.geterdone.io/market-structure/options-contract-selection/` | Options Contract Selection Lab | `site/market-structure/options-contract-selection/index.html` |
| — | `https://learn.geterdone.io/trade-setup-execution/` | **Trade Setup and Execution** — course 2 home | `site/trade-setup-execution/index.html` |
| 2.01 | `https://learn.geterdone.io/trade-setup-execution/trade-thesis/` | Trade Thesis | `site/trade-setup-execution/trade-thesis/index.html` |
| 2.02 | `https://learn.geterdone.io/trade-setup-execution/support-resistance/` | Support and Resistance | `site/trade-setup-execution/support-resistance/index.html` |
| 2.03 | `https://learn.geterdone.io/trade-setup-execution/confluence/` | Confluence | `site/trade-setup-execution/confluence/index.html` |
| 2.04 | `https://learn.geterdone.io/trade-setup-execution/breakout-setups/` | Breakout Setups | `site/trade-setup-execution/breakout-setups/index.html` |
| 2.05 | `https://learn.geterdone.io/trade-setup-execution/pullback-setups/` | Pullback Setups | `site/trade-setup-execution/pullback-setups/index.html` |
| 2.06 | `https://learn.geterdone.io/trade-setup-execution/reversal-setups/` | Reversal Setups | `site/trade-setup-execution/reversal-setups/index.html` |
| 2.07 | `https://learn.geterdone.io/trade-setup-execution/entry-confirmation/` | Entry Confirmation | `site/trade-setup-execution/entry-confirmation/index.html` |
| 2.08 | `https://learn.geterdone.io/trade-setup-execution/stop-loss-placement/` | Stop-Loss Placement | `site/trade-setup-execution/stop-loss-placement/index.html` |
| 2.09 | `https://learn.geterdone.io/trade-setup-execution/profit-targets/` | Profit Targets | `site/trade-setup-execution/profit-targets/index.html` |
| 2.10 | `https://learn.geterdone.io/trade-setup-execution/risk-to-reward/` | Risk-to-Reward | `site/trade-setup-execution/risk-to-reward/index.html` |
| 2.11 | `https://learn.geterdone.io/trade-setup-execution/position-sizing/` | Position Sizing | `site/trade-setup-execution/position-sizing/index.html` |
| 2.12 | `https://learn.geterdone.io/trade-setup-execution/trade-management/` | Trade Management | `site/trade-setup-execution/trade-management/index.html` |
| 2.13 | `https://learn.geterdone.io/trade-setup-execution/backtesting/` | Backtesting | `site/trade-setup-execution/backtesting/index.html` |
| 2.14 | `https://learn.geterdone.io/trade-setup-execution/trading-journal/` | Trading Journal | `site/trade-setup-execution/trading-journal/index.html` |
| 2.15 | `https://learn.geterdone.io/trade-setup-execution/performance-review/` | Performance Review | `site/trade-setup-execution/performance-review/index.html` |
| asset | `https://learn.geterdone.io/trade-setup-execution/trade-journal-schema.json` | Trade journal exchange schema (JSON, not a page) | `site/trade-setup-execution/trade-journal-schema.json` |
| — | `https://learn.geterdone.io/options-trading/` | **Options Trading** — course 3 home | `site/options-trading/index.html` |
| 3.01 | `https://learn.geterdone.io/options-trading/options-contract-fundamentals/` | Options Contract Fundamentals | `site/options-trading/options-contract-fundamentals/index.html` |
| 3.02 | `https://learn.geterdone.io/options-trading/calls-and-puts/` | Calls and Puts | `site/options-trading/calls-and-puts/index.html` |
| 3.03 | `https://learn.geterdone.io/options-trading/moneyness/` | Moneyness | `site/options-trading/moneyness/index.html` |
| 3.04 | `https://learn.geterdone.io/options-trading/option-premium/` | Option Premium | `site/options-trading/option-premium/index.html` |
| 3.05 | `https://learn.geterdone.io/options-trading/option-chain-and-liquidity/` | Option Chain and Liquidity | `site/options-trading/option-chain-and-liquidity/index.html` |
| 3.06 | `https://learn.geterdone.io/options-trading/expiration-and-time-decay/` | Expiration and Time Decay | `site/options-trading/expiration-and-time-decay/index.html` |
| 3.07 | `https://learn.geterdone.io/options-trading/implied-volatility/` | Implied Volatility | `site/options-trading/implied-volatility/index.html` |
| 3.08 | `https://learn.geterdone.io/options-trading/delta-and-gamma/` | Delta and Gamma | `site/options-trading/delta-and-gamma/index.html` |
| 3.09 | `https://learn.geterdone.io/options-trading/theta-and-vega/` | Theta and Vega | `site/options-trading/theta-and-vega/index.html` |
| 3.10 | `https://learn.geterdone.io/options-trading/long-calls-and-long-puts/` | Long Calls and Long Puts | `site/options-trading/long-calls-and-long-puts/index.html` |
| 3.11 | `https://learn.geterdone.io/options-trading/covered-calls/` | Covered Calls | `site/options-trading/covered-calls/index.html` |
| 3.12 | `https://learn.geterdone.io/options-trading/cash-secured-puts/` | Cash-Secured Puts | `site/options-trading/cash-secured-puts/index.html` |
| 3.13 | `https://learn.geterdone.io/options-trading/vertical-debit-spreads/` | Vertical Debit Spreads | `site/options-trading/vertical-debit-spreads/index.html` |
| 3.14 | `https://learn.geterdone.io/options-trading/vertical-credit-spreads/` | Vertical Credit Spreads | `site/options-trading/vertical-credit-spreads/index.html` |
| 3.15 | `https://learn.geterdone.io/options-trading/exercise-assignment-and-expiration/` | Exercise, Assignment, and Expiration | `site/options-trading/exercise-assignment-and-expiration/index.html` |
| 3.16 | `https://learn.geterdone.io/options-trading/options-trade-planning/` | Options Trade Planning | `site/options-trading/options-trade-planning/index.html` |
| asset | `https://learn.geterdone.io/options-trading/options-trade-plan-schema.json` | Options trade plan schema (JSON, not a page) | `site/options-trading/options-trade-plan-schema.json` |
| — | `https://learn.geterdone.io/technical-indicators/` | **Technical Indicators** — course 4 home | `site/technical-indicators/index.html` |
| 4.01 | `https://learn.geterdone.io/technical-indicators/technical-indicator-fundamentals/` | Technical Indicator Fundamentals | `site/technical-indicators/technical-indicator-fundamentals/index.html` |
| 4.02 | `https://learn.geterdone.io/technical-indicators/moving-averages/` | Simple and Exponential Moving Averages | `site/technical-indicators/moving-averages/index.html` |
| 4.03 | `https://learn.geterdone.io/technical-indicators/moving-average-crossovers/` | Moving Average Trend Filters and Crossovers | `site/technical-indicators/moving-average-crossovers/index.html` |
| 4.04 | `https://learn.geterdone.io/technical-indicators/relative-strength-index/` | Relative Strength Index | `site/technical-indicators/relative-strength-index/index.html` |
| 4.05 | `https://learn.geterdone.io/technical-indicators/stochastic-oscillator/` | Stochastic Oscillator | `site/technical-indicators/stochastic-oscillator/index.html` |
| 4.06 | `https://learn.geterdone.io/technical-indicators/macd/` | Moving Average Convergence Divergence | `site/technical-indicators/macd/index.html` |
| 4.07 | `https://learn.geterdone.io/technical-indicators/average-directional-index/` | Average Directional Index and Directional Movement | `site/technical-indicators/average-directional-index/index.html` |
| 4.08 | `https://learn.geterdone.io/technical-indicators/average-true-range/` | Average True Range | `site/technical-indicators/average-true-range/index.html` |
| 4.09 | `https://learn.geterdone.io/technical-indicators/bollinger-bands/` | Bollinger Bands | `site/technical-indicators/bollinger-bands/index.html` |
| 4.10 | `https://learn.geterdone.io/technical-indicators/keltner-channels/` | Keltner Channels | `site/technical-indicators/keltner-channels/index.html` |
| 4.11 | `https://learn.geterdone.io/technical-indicators/donchian-channels/` | Donchian Channels | `site/technical-indicators/donchian-channels/index.html` |
| 4.12 | `https://learn.geterdone.io/technical-indicators/rate-of-change-and-momentum/` | Rate of Change and Momentum | `site/technical-indicators/rate-of-change-and-momentum/index.html` |
| 4.13 | `https://learn.geterdone.io/technical-indicators/indicator-divergence/` | Indicator Divergence | `site/technical-indicators/indicator-divergence/index.html` |
| 4.14 | `https://learn.geterdone.io/technical-indicators/combining-indicators/` | Combining Indicators Without Redundancy | `site/technical-indicators/combining-indicators/index.html` |
| 4.15 | `https://learn.geterdone.io/technical-indicators/indicator-selection-by-market-regime/` | Indicator Selection by Market Regime | `site/technical-indicators/indicator-selection-by-market-regime/index.html` |
| 4.16 | `https://learn.geterdone.io/technical-indicators/indicator-based-trading-rules/` | Indicator-Based Trading Rules | `site/technical-indicators/indicator-based-trading-rules/index.html` |
| asset | `https://learn.geterdone.io/technical-indicators/indicator-rule-schema.json` | Indicator rule schema (JSON, not a page) | `site/technical-indicators/indicator-rule-schema.json` |
| — | `https://learn.geterdone.io/volume-and-order-flow/` | **Volume and Order Flow** — course 5 home | `site/volume-and-order-flow/index.html` |
| 5.01 | `https://learn.geterdone.io/volume-and-order-flow/volume-fundamentals/` | Volume Fundamentals | `site/volume-and-order-flow/volume-fundamentals/index.html` |
| 5.02 | `https://learn.geterdone.io/volume-and-order-flow/price-volume-relationships/` | Price and Volume Relationships | `site/volume-and-order-flow/price-volume-relationships/index.html` |
| 5.03 | `https://learn.geterdone.io/volume-and-order-flow/relative-volume-and-volume-spikes/` | Relative Volume and Volume Spikes | `site/volume-and-order-flow/relative-volume-and-volume-spikes/index.html` |
| 5.04 | `https://learn.geterdone.io/volume-and-order-flow/volume-confirmation/` | Volume Confirmation | `site/volume-and-order-flow/volume-confirmation/index.html` |
| 5.05 | `https://learn.geterdone.io/volume-and-order-flow/on-balance-volume/` | On-Balance Volume | `site/volume-and-order-flow/on-balance-volume/index.html` |
| 5.06 | `https://learn.geterdone.io/volume-and-order-flow/accumulation-distribution-and-chaikin-money-flow/` | Accumulation/Distribution and Chaikin Money Flow | `site/volume-and-order-flow/accumulation-distribution-and-chaikin-money-flow/index.html` |
| 5.07 | `https://learn.geterdone.io/volume-and-order-flow/volume-weighted-average-price/` | Volume-Weighted Average Price | `site/volume-and-order-flow/volume-weighted-average-price/index.html` |
| 5.08 | `https://learn.geterdone.io/volume-and-order-flow/anchored-volume-weighted-average-price/` | Anchored Volume-Weighted Average Price | `site/volume-and-order-flow/anchored-volume-weighted-average-price/index.html` |
| 5.09 | `https://learn.geterdone.io/volume-and-order-flow/volume-profile/` | Volume Profile | `site/volume-and-order-flow/volume-profile/index.html` |
| 5.10 | `https://learn.geterdone.io/volume-and-order-flow/value-area-poc-hvn-lvn/` | Value Area, POC, HVN, and LVN | `site/volume-and-order-flow/value-area-poc-hvn-lvn/index.html` |
| 5.11 | `https://learn.geterdone.io/volume-and-order-flow/bid-ask-spread-and-order-types/` | Bid, Ask, Spread, and Order Types | `site/volume-and-order-flow/bid-ask-spread-and-order-types/index.html` |
| 5.12 | `https://learn.geterdone.io/volume-and-order-flow/time-and-sales/` | Time and Sales | `site/volume-and-order-flow/time-and-sales/index.html` |
| 5.13 | `https://learn.geterdone.io/volume-and-order-flow/footprint-charts-and-bid-ask-delta/` | Footprint Charts and Bid-Ask Delta | `site/volume-and-order-flow/footprint-charts-and-bid-ask-delta/index.html` |
| 5.14 | `https://learn.geterdone.io/volume-and-order-flow/cumulative-volume-delta/` | Cumulative Volume Delta | `site/volume-and-order-flow/cumulative-volume-delta/index.html` |
| 5.15 | `https://learn.geterdone.io/volume-and-order-flow/order-book-and-market-depth/` | Order Book and Market Depth | `site/volume-and-order-flow/order-book-and-market-depth/index.html` |
| 5.16 | `https://learn.geterdone.io/volume-and-order-flow/volume-and-order-flow-trading-rules/` | Volume and Order Flow Trading Rules | `site/volume-and-order-flow/volume-and-order-flow-trading-rules/index.html` |
| asset | `https://learn.geterdone.io/volume-and-order-flow/volume-order-flow-rule-schema.json` | Volume and order flow rule schema (JSON, not a page) | `site/volume-and-order-flow/volume-order-flow-rule-schema.json` |
| — | `https://learn.geterdone.io/trading-risk-management/` | **Trading Risk Management** — course 6 home | `site/trading-risk-management/index.html` |
| 6.01 | `https://learn.geterdone.io/trading-risk-management/risk-management-fundamentals/` | Risk Management Fundamentals | `site/trading-risk-management/risk-management-fundamentals/index.html` |
| 6.02 | `https://learn.geterdone.io/trading-risk-management/account-risk-and-risk-budget/` | Account Risk and Risk Budget | `site/trading-risk-management/account-risk-and-risk-budget/index.html` |
| 6.03 | `https://learn.geterdone.io/trading-risk-management/risk-per-trade/` | Risk Per Trade | `site/trading-risk-management/risk-per-trade/index.html` |
| 6.04 | `https://learn.geterdone.io/trading-risk-management/stop-loss-and-structural-invalidation/` | Stop-Loss and Structural Invalidation | `site/trading-risk-management/stop-loss-and-structural-invalidation/index.html` |
| 6.05 | `https://learn.geterdone.io/trading-risk-management/position-sizing/` | Position Sizing | `site/trading-risk-management/position-sizing/index.html` |
| 6.06 | `https://learn.geterdone.io/trading-risk-management/reward-to-risk-and-r-multiples/` | Reward-to-Risk and R-Multiples | `site/trading-risk-management/reward-to-risk-and-r-multiples/index.html` |
| 6.07 | `https://learn.geterdone.io/trading-risk-management/win-rate-average-win-loss-and-expectancy/` | Win Rate, Average Win/Loss, and Expectancy | `site/trading-risk-management/win-rate-average-win-loss-and-expectancy/index.html` |
| 6.08 | `https://learn.geterdone.io/trading-risk-management/losing-streaks-and-drawdown/` | Losing Streaks and Drawdown | `site/trading-risk-management/losing-streaks-and-drawdown/index.html` |
| 6.09 | `https://learn.geterdone.io/trading-risk-management/risk-of-ruin/` | Risk of Ruin | `site/trading-risk-management/risk-of-ruin/index.html` |
| 6.10 | `https://learn.geterdone.io/trading-risk-management/volatility-and-atr-based-risk/` | Volatility and ATR-Based Risk | `site/trading-risk-management/volatility-and-atr-based-risk/index.html` |
| 6.11 | `https://learn.geterdone.io/trading-risk-management/gap-slippage-liquidity-and-execution-risk/` | Gap, Slippage, Liquidity, and Execution Risk | `site/trading-risk-management/gap-slippage-liquidity-and-execution-risk/index.html` |
| 6.12 | `https://learn.geterdone.io/trading-risk-management/leverage-and-margin-risk/` | Leverage and Margin Risk | `site/trading-risk-management/leverage-and-margin-risk/index.html` |
| 6.13 | `https://learn.geterdone.io/trading-risk-management/correlation-concentration-and-portfolio-exposure/` | Correlation, Concentration, and Portfolio Exposure | `site/trading-risk-management/correlation-concentration-and-portfolio-exposure/index.html` |
| 6.14 | `https://learn.geterdone.io/trading-risk-management/options-risk-management/` | Options Risk Management | `site/trading-risk-management/options-risk-management/index.html` |
| 6.15 | `https://learn.geterdone.io/trading-risk-management/daily-and-weekly-risk-limits/` | Daily and Weekly Risk Limits | `site/trading-risk-management/daily-and-weekly-risk-limits/index.html` |
| 6.16 | `https://learn.geterdone.io/trading-risk-management/trading-risk-plan/` | Trading Risk Plan | `site/trading-risk-management/trading-risk-plan/index.html` |
| asset | `https://learn.geterdone.io/trading-risk-management/trading-risk-plan-schema.json` | Trading risk plan schema (JSON, not a page) | `site/trading-risk-management/trading-risk-plan-schema.json` |
| — | `https://learn.geterdone.io/backtesting-and-trading-systems/` | **Backtesting and Trading Systems** — course 7 home | `site/backtesting-and-trading-systems/index.html` |
| 7.01 | `https://learn.geterdone.io/backtesting-and-trading-systems/backtesting-fundamentals/` | Backtesting Fundamentals | `site/backtesting-and-trading-systems/backtesting-fundamentals/index.html` |
| 7.02 | `https://learn.geterdone.io/backtesting-and-trading-systems/testable-trading-rules-and-hypotheses/` | Testable Trading Rules and Hypotheses | `site/backtesting-and-trading-systems/testable-trading-rules-and-hypotheses/index.html` |
| 7.03 | `https://learn.geterdone.io/backtesting-and-trading-systems/historical-data-and-data-quality/` | Historical Data and Data Quality | `site/backtesting-and-trading-systems/historical-data-and-data-quality/index.html` |
| 7.04 | `https://learn.geterdone.io/backtesting-and-trading-systems/survivorship-selection-and-corporate-actions/` | Survivorship, Selection, and Corporate Actions | `site/backtesting-and-trading-systems/survivorship-selection-and-corporate-actions/index.html` |
| 7.05 | `https://learn.geterdone.io/backtesting-and-trading-systems/timeframes-sessions-and-bar-construction/` | Timeframes, Sessions, and Bar Construction | `site/backtesting-and-trading-systems/timeframes-sessions-and-bar-construction/index.html` |
| 7.06 | `https://learn.geterdone.io/backtesting-and-trading-systems/signal-timing-look-ahead-bias-and-data-leakage/` | Signal Timing, Look-Ahead Bias, and Data Leakage | `site/backtesting-and-trading-systems/signal-timing-look-ahead-bias-and-data-leakage/index.html` |
| 7.07 | `https://learn.geterdone.io/backtesting-and-trading-systems/trade-execution-simulation/` | Trade Execution Simulation | `site/backtesting-and-trading-systems/trade-execution-simulation/index.html` |
| 7.08 | `https://learn.geterdone.io/backtesting-and-trading-systems/position-sizing-and-portfolio-accounting/` | Position Sizing and Portfolio Accounting | `site/backtesting-and-trading-systems/position-sizing-and-portfolio-accounting/index.html` |
| 7.09 | `https://learn.geterdone.io/backtesting-and-trading-systems/transaction-costs-spread-slippage-and-liquidity/` | Transaction Costs, Spread, Slippage, and Liquidity | `site/backtesting-and-trading-systems/transaction-costs-spread-slippage-and-liquidity/index.html` |
| 7.10 | `https://learn.geterdone.io/backtesting-and-trading-systems/trade-log-equity-curve-and-drawdown/` | Trade Log, Equity Curve, and Drawdown | `site/backtesting-and-trading-systems/trade-log-equity-curve-and-drawdown/index.html` |
| 7.11 | `https://learn.geterdone.io/backtesting-and-trading-systems/performance-metrics-and-expectancy/` | Performance Metrics and Expectancy | `site/backtesting-and-trading-systems/performance-metrics-and-expectancy/index.html` |
| 7.12 | `https://learn.geterdone.io/backtesting-and-trading-systems/benchmarking-and-risk-adjusted-performance/` | Benchmarking and Risk-Adjusted Performance | `site/backtesting-and-trading-systems/benchmarking-and-risk-adjusted-performance/index.html` |
| 7.13 | `https://learn.geterdone.io/backtesting-and-trading-systems/in-sample-validation-and-out-of-sample-data/` | In-Sample, Validation, and Out-of-Sample Data | `site/backtesting-and-trading-systems/in-sample-validation-and-out-of-sample-data/index.html` |
| 7.14 | `https://learn.geterdone.io/backtesting-and-trading-systems/walk-forward-testing/` | Walk-Forward Testing | `site/backtesting-and-trading-systems/walk-forward-testing/index.html` |
| 7.15 | `https://learn.geterdone.io/backtesting-and-trading-systems/overfitting-sensitivity-monte-carlo-and-stress-testing/` | Overfitting, Sensitivity, Monte Carlo, and Stress Testing | `site/backtesting-and-trading-systems/overfitting-sensitivity-monte-carlo-and-stress-testing/index.html` |
| 7.16 | `https://learn.geterdone.io/backtesting-and-trading-systems/trading-system-specification-and-backtest-report/` | Trading System Specification and Backtest Report | `site/backtesting-and-trading-systems/trading-system-specification-and-backtest-report/index.html` |
| asset | `https://learn.geterdone.io/backtesting-and-trading-systems/trading-system-specification-schema.json` | Trading system specification schema (JSON, not a page) | `site/backtesting-and-trading-systems/trading-system-specification-schema.json` |
| — | `https://learn.geterdone.io/algorithmic-and-automated-trading/` | **Algorithmic and Automated Trading** — course 8 home | `site/algorithmic-and-automated-trading/index.html` |
| 8.01 | `https://learn.geterdone.io/algorithmic-and-automated-trading/algorithmic-and-automated-trading-fundamentals/` | Algorithmic and Automated Trading Fundamentals | `site/algorithmic-and-automated-trading/algorithmic-and-automated-trading-fundamentals/index.html` |
| 8.02 | `https://learn.geterdone.io/algorithmic-and-automated-trading/trading-system-architecture-and-components/` | Trading System Architecture and Components | `site/algorithmic-and-automated-trading/trading-system-architecture-and-components/index.html` |
| 8.03 | `https://learn.geterdone.io/algorithmic-and-automated-trading/market-data-ingestion-and-normalization/` | Market Data Ingestion and Normalization | `site/algorithmic-and-automated-trading/market-data-ingestion-and-normalization/index.html` |
| 8.04 | `https://learn.geterdone.io/algorithmic-and-automated-trading/time-sessions-events-and-scheduling/` | Time, Sessions, Events, and Scheduling | `site/algorithmic-and-automated-trading/time-sessions-events-and-scheduling/index.html` |
| 8.05 | `https://learn.geterdone.io/algorithmic-and-automated-trading/signal-engine-and-strategy-state/` | Signal Engine and Strategy State | `site/algorithmic-and-automated-trading/signal-engine-and-strategy-state/index.html` |
| 8.06 | `https://learn.geterdone.io/algorithmic-and-automated-trading/portfolio-position-and-risk-engine/` | Portfolio, Position, and Risk Engine | `site/algorithmic-and-automated-trading/portfolio-position-and-risk-engine/index.html` |
| 8.07 | `https://learn.geterdone.io/algorithmic-and-automated-trading/broker-apis-and-order-lifecycle/` | Broker APIs and Order Lifecycle | `site/algorithmic-and-automated-trading/broker-apis-and-order-lifecycle/index.html` |
| 8.08 | `https://learn.geterdone.io/algorithmic-and-automated-trading/order-management-and-execution/` | Order Management and Execution | `site/algorithmic-and-automated-trading/order-management-and-execution/index.html` |
| 8.09 | `https://learn.geterdone.io/algorithmic-and-automated-trading/paper-trading-and-forward-testing/` | Paper Trading and Forward Testing | `site/algorithmic-and-automated-trading/paper-trading-and-forward-testing/index.html` |
| 8.10 | `https://learn.geterdone.io/algorithmic-and-automated-trading/scanners-alerts-and-human-approval/` | Scanners, Alerts, and Human Approval | `site/algorithmic-and-automated-trading/scanners-alerts-and-human-approval/index.html` |
| 8.11 | `https://learn.geterdone.io/algorithmic-and-automated-trading/reliability-idempotency-retries-and-recovery/` | Reliability, Idempotency, Retries, and Recovery | `site/algorithmic-and-automated-trading/reliability-idempotency-retries-and-recovery/index.html` |
| 8.12 | `https://learn.geterdone.io/algorithmic-and-automated-trading/observability-logging-and-auditability/` | Observability, Logging, and Auditability | `site/algorithmic-and-automated-trading/observability-logging-and-auditability/index.html` |
| 8.13 | `https://learn.geterdone.io/algorithmic-and-automated-trading/security-secrets-permissions-and-kill-switches/` | Security, Secrets, Permissions, and Kill Switches | `site/algorithmic-and-automated-trading/security-secrets-permissions-and-kill-switches/index.html` |
| 8.14 | `https://learn.geterdone.io/algorithmic-and-automated-trading/deployment-environments-and-configuration/` | Deployment, Environments, and Configuration | `site/algorithmic-and-automated-trading/deployment-environments-and-configuration/index.html` |
| 8.15 | `https://learn.geterdone.io/algorithmic-and-automated-trading/ai-assisted-and-agentic-trading-workflows/` | AI-Assisted and Agentic Trading Workflows | `site/algorithmic-and-automated-trading/ai-assisted-and-agentic-trading-workflows/index.html` |
| 8.16 | `https://learn.geterdone.io/algorithmic-and-automated-trading/automated-trading-system-specification-and-production-readiness/` | Automated Trading System Specification and Production Readiness | `site/algorithmic-and-automated-trading/automated-trading-system-specification-and-production-readiness/index.html` |
| asset | `https://learn.geterdone.io/algorithmic-and-automated-trading/automated-trading-system-schema.json` | Automated trading system schema (JSON, not a page) | `site/algorithmic-and-automated-trading/automated-trading-system-schema.json` |

Course 1 and its lesson 01 share the name *Market Structure*: the course is the
whole seven-lesson sequence, lesson 01 is its first lesson on structure itself
(and keeps its original *Market Structure Lab* page title). Both are
authoritative and neither changes; navigation numbers the
lessons so a reader can tell them apart, and every guard identifies a page by its
own full `<link rel="canonical" …>` tag rather than by a title or a path
fragment, because course and lesson paths overlap by prefix and a course home
links to all of its own lessons.

`site/` **is** the document root: its tree maps one-to-one onto public paths, so
a lesson lives one directory below its course both on disk and in the URL.

Both a lesson and a path page are two segments deep, so both link up with `../`
and `../../`; a lesson's `../` is its own course home, a path page's is the paths
layer. Nothing may use a root-absolute `/…` path: the suite rejects them so the
tree also previews correctly under a subpath.

**Two sets of URLs are retired, with no redirect stubs.** The seven flat lesson
URLs course 1 published first (`/ranges-breakouts-liquidity/`, …) and then the
whole `/market-structure-lab/…` prefix it used until the paths layer landed.
Retiring both was a deliberate, accepted break: nothing serves them and no guard
or contract lists them. A request for one is a plain 404. Do not re-add them to
any page map — a path in these maps is a path that must exist.

That map is declared in five places, and all five must agree:

- `tests/test_site_invariants.py` → `REQUIRED_PAGES` (pages on disk, including
  `SITE_INDEX` and `PATH_PAGE`) and `NON_HTML_ASSETS` (all four JSON schemas,
  each declared as an asset rather than by loosening any page check);
- `scripts/smoke.py` → `PATH_PAGE_PATH`, `COURSE_PATH`, `COURSE_LESSONS`,
  `COURSE_2_PATH`, `COURSE_2_LESSONS`, `COURSE_3_PATH`, `COURSE_3_LESSONS`,
  `COURSE_4_PATH`, `COURSE_4_LESSONS`, `COURSE_5_PATH`, `COURSE_5_LESSONS` and
  `PUBLISHED_ASSETS` (served responses);
- `release/contract.json` → `acceptance.checks`, one check id per URL
  (`learn-index`; `trading-path` for the path page; `course-home` and
  `lesson-page`/`lesson-<slug>` for course 1; `course2-home` and
  `course2-lesson-<slug>` for course 2, and the same shape for courses 3 to
  8 — course-scoped because a slug is unique only within a course (courses 2
  and 6 both ship a `position-sizing` lesson);
  `journal-schema`, `trade-plan-schema`, `indicator-rule-schema`,
  `volume-order-flow-rule-schema`, `trading-risk-plan-schema`,
  `trading-system-specification-schema` and `automated-trading-system-schema`
  for the seven assets, each fetched and parsed as JSON). One id is shortened
  against that scheme — course 8's lesson 16 slug would push
  `course8-lesson-<slug>` past the 72-character cap the contract schema sets, so
  `scripts/smoke.py` and both contract documents name it
  `course8-lesson-system-specification-and-production-readiness`, and
  `TestDeclaredUrlSpaceAgrees` fails if the two files ever stop agreeing on it.
  `release/contract.schema.json` requires every one of those ids by name — all
  139 of them — so a check cannot be quietly dropped;
- `.github/workflows/ci.yml` → the "Published URL space is complete" step;
- `Containerfile.release` and `.github/workflows/pages.yml` (publish-time guards).

A page added to one of them and not the others is a page nothing checks.

Further site-wide invariants exist because eight courses now share one origin.
Each of them is something a reader carries across a course boundary, so each is
pinned once and asserted on all 128 pages (`TestPinnedConventions`):

- **One theme key.** Every page persists the reader's light/dark choice under the
  single `localStorage` key `learn-theme`. The per-course keys the courses shipped
  with (`marketStructureTheme`, `market-lab-theme`, `options-course-theme`,
  course 4's `technical-indicators-theme`, course 5's `vof-theme`, course 6's
  `trm-theme`, course 7's `bts-theme` and course 8's `aat-theme` — eight
  packages, eight different keys) silently reset a reader's choice at every course
  boundary; standardizing cost one stored preference, once, and the suite now
  fails any page that invents its own key.
- **One complete pager per course, in one markup.** `prev`/`next` links must walk
  each course in the order declared in `COURSES`, so a reordered syllabus and a
  reordered pager cannot disagree and no lesson becomes a dead end — and the
  pager is always `nav.lesson-nav` with `a.lesson-link.prev` / `a.lesson-link.next`
  anchors. The first lesson omits the prev anchor entirely; the last lesson's
  forward link points at the course home and carries **no** `rel`, because the
  course home is not the next document in the sequence.
- **One light palette.** The light theme has two paths — the explicit toggle
  (`[data-theme="light"]`) and `@media (prefers-color-scheme: light)` for the
  reader who never touches it — and both declare the same token values. Every
  page that declares a light token declares the pinned value for it; component
  rules read tokens, so a `[data-theme="light"] .foo` override (which reaches
  the toggle path only) fails the suite.
- **One theme toggle.** `<button class="icon-btn" id="themeToggle" type="button">`
  with a static, direction-neutral `aria-label` plus `title`. A label rewritten
  from JavaScript has to choose between naming the current theme and the next
  one, and the courses chose differently; a static label is accurate in both
  states and cannot diverge.

Two further invariants come from the library being subject-agnostic rather than
from the courses:

- **The frame names no subject.** The masthead and footer of the site index and
  of every path page carry no trading vocabulary, and the index never writes
  "the path" — it lists paths (`TestSharedChromeIsSubjectAgnostic`). A
  subject-scoped notice is marked `class="risk"` and is exempt: it describes the
  courses that page lists, not the frame.
- **Every course knows its place.** A course home states `Course N of 8` and its
  `rel=prev`/`rel=next` links resolve to the adjacent course homes — course 1
  ships no `prev`, and course 8 ships no `next` because it is the last course on
  the path (`TestPathPosition`). Each course's forward link stopped being a
  disabled span and became a real `rel="next"` anchor the day its successor
  shipped — course 4's when course 5 landed, course 5's when course 6 landed,
  course 7's when course 8 landed. There is no disabled forward link left in the
  library, and no course after 8 to make one for.

The apex `geterdone.io` is a separate, live GitHub Pages site. It is not part of
this project and nothing here touches it: every footer links to
`https://learn.geterdone.io`, and `TestFooterSiteIdentity` fails any page whose
footer points at the apex instead.

## Local preview

No build step, no dependencies:

```sh
python3 -m http.server 8000 --directory site
```

Then open <http://127.0.0.1:8000/>. Directory URLs resolve to `index.html`, so
`http://127.0.0.1:8000/paths/trading/` previews the path page,
`http://127.0.0.1:8000/trade-setup-execution/` previews course 2's home and
`http://127.0.0.1:8000/trade-setup-execution/trade-thesis/` previews its lesson
01, exactly as the public paths will serve them.

Opening the HTML file directly with `file://` also works, but the local server is
the accurate preview because it exercises the same directory-index behavior as
production.

The same checks CI runs are reproducible locally, with no installation step:

```sh
python3 -m unittest discover -s tests -v        # on-disk invariants
python3 scripts/smoke.py http://127.0.0.1:8000  # acceptance checks against the preview
python3 scripts/validate_release_contract.py \
    release/contract.json release/contract.example.json
```

`smoke.py` checks all 128 published pages plus all seven JSON assets — one report
line per URL, each page demanding that document's own canonical tag and each
asset fetched, typed and parsed as JSON. The path page has its own check id
(`trading-path`) with its own markers: it is the only URL that shows the whole
path in one place. Those markers used to name the last published course and the
first announced one and moved forward at every launch; with the path complete
they name the LAST course and the link to its home, which is what distinguishes
a listed course from a mentioned one. Against the plain
`python3 -m http.server` preview the `internal-health` and `security-headers`
checks fail by design: `/healthz` and the header policy come from the
in-container Caddy (`deploy/Caddyfile`), not from anything in `site/`.

## Repository layout

```text
site/                     the published document root — nothing else is served
site/paths/<subject>/     one path page per subject (the paths layer)
Containerfile.release     builds the release image (static files + Caddy)
compose.template.yaml     immutable Compose template rendered by the deploy wrapper
deploy/Caddyfile          in-container web server: headers, cache policy, /healthz
deploy/registry-entry.PROPOSED.yaml   proposed platform registry entry (for review)
release/contract.json                 committed release-contract source (see below)
release/contract.schema.json          release-contract schema
release/contract.example.json         shape reference; never staged as a release
scripts/validate_release_contract.py  stdlib JSON Schema checker for the two above
scripts/smoke.py          standard-library acceptance smoke client
tests/                    on-disk invariant suite (standard library, no install)
.github/workflows/ci.yml       PR checks: HTML, self-containment, links, container
.github/workflows/pages.yml    GitHub Pages publish (the live delivery path)
.github/workflows/release.yml  protected-main build, publish, release metadata
AGENTS.md                 working agreement — read before changing anything
```

## Two delivery paths

**1. GitHub Pages — live.** `.github/workflows/pages.yml` uploads `site/` on every
push to `main` and deploys it to `learn.geterdone.io` (`site/CNAME` holds the
custom domain). Before uploading it re-checks self-containment, asserts that all
128 pages exist, and parses all seven published JSON assets. This path does not
touch platform-ops, the shared Caddy edge, or any registry reservation, and it
is **not** a shortcut around those gates — they govern the Hetzner platform,
which is a different path.

**2. The Hetzner container platform — not built.** That platform serves
applications **only** as containers behind `reverse_proxy 127.0.0.1:<port>`; it
has no file server and no host document root. So the site would ship as an image:
`Containerfile.release` copies `site/` into `/srv` behind a small in-container
Caddy that also answers `GET /healthz` with `200`.

A push to protected `main` re-runs the full check set, renders the deployment
placeholders, builds the image, pushes it to
`ghcr.io/dmedellin/market-structure-lab` by **immutable digest**, and emits the
immutable release contract plus release metadata (image digest, git revision,
release-contract sha256, compose template and rendered-Compose sha256).

`release/contract.json` is the committed contract source and the **single source
of truth for `__LOOPBACK_PORT__` and `__APP_SUBNET__`**. The release workflow
renders `Containerfile.release`, `deploy/Caddyfile` and
`deploy/compose.template.yaml` from it, fills in only the fields the run can
prove, and validates the emitted document against `release/contract.schema.json`.
Because the port and subnet are still unallocated, that render step **fails the
workflow on purpose** with a message naming the allocation gate; no image can be
built until a human allocates them. A future host deploy would consume that
metadata through a root-owned wrapper on a self-hosted runner; the deploy job in
`release.yml` is committed but **inert**, and a public route and DNS pointing at
that host would be a separate, human-reviewed edge transaction.

The normative rules live in `dmedellin/platform-ops`
(`docs/DEPLOYMENT_CONTRACT.md`, `docs/EDGE_ROUTING_CONTRACT.md`,
`docs/APP_ONBOARDING.md`). See [AGENTS.md](AGENTS.md).

## STATUS

**Deployed on GitHub Pages.** `https://learn.geterdone.io/` serves this `site/`
tree — the site index, the trading path page, all eight course homes, all 118
lessons, and the seven published schemas (trade journal, options trade plan,
indicator rule, volume and order flow rule, trading risk plan, trading system
specification, and automated trading system) — from the `pages.yml` workflow.
128 pages and 7 assets; the trading path is complete, and nothing in the library
is announced without a page behind it.

**The Hetzner container path remains UNBUILT.** No image of this repository has
ever been built, deployed, or accepted on that platform. As of 2026-08-15, all of
the following are still open:

- **Platform onboarding is unbuilt.** The Hetzner host has no registry entry for
  `market-structure-lab`, no self-hosted repository-scoped runner, and no
  installed deploy wrapper for this app. Nothing has been installed on any host.
- **The loopback port and app subnet are UNALLOCATED.** They appear throughout as
  the literal placeholders `__LOOPBACK_PORT__` and `__APP_SUBNET__`. Allocation is
  an explicit human decision plus a live host preflight and is deliberately not
  automated.
- **No edge route exists** for `learn.geterdone.io` on that host. DNS for the
  subdomain points at GitHub Pages; nothing points at Hetzner, and creating a
  route there is a separate reviewed transaction, not a release.
- **The release deploy job is inert** (`if: false` in `release.yml`) and depends
  on a self-hosted runner that does not exist and a human-approved `production`
  environment that has not been created.
- **No container acceptance has occurred.** No image build, container deployment,
  container smoke run, or SRE acceptance for this repository has ever run. Any
  statement to the contrary is wrong.

## License

[MIT](LICENSE) © 2026 dmedellin.
