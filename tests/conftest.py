import pytest
from typing import Callable
from unittest.mock import MagicMock, patch
from longport.openapi import Market
from modules.long_port_market_adapter import LongPortMarketAdapter


@pytest.fixture(scope="module")
def live_adapter() -> LongPortMarketAdapter:
    adapter = LongPortMarketAdapter()
    return adapter


@pytest.fixture(scope="module")
def mock_adapter() -> LongPortMarketAdapter:
    with patch("modules.long_port_market_adapter.QuoteContext"):
        adapter = LongPortMarketAdapter()
        adapter.ctx = MagicMock()

        # ==================== 1. 基础工厂函数定义 ====================
        def list_factory(prefix: str) -> Callable[[list[str]], list[str]]:
            """创建返回列表的侧效应"""
            return lambda symbols: [f"{prefix}: {s}" for s in symbols]

        def single_factory(prefix: str) -> Callable[[str], str | None]:
            """创建返回单个值的侧效应"""
            return lambda symbol: None if not symbol else f"{prefix}: {symbol}"

        def indexed_list_factory(prefix: str) -> Callable[[str, int], list[str]]:
            """创建返回带索引列表的侧效应"""
            return lambda symbol, count: [
                f"{prefix}: {symbol}_{i}" for i in range(count)
            ]

        def const_list_factory(prefix: str) -> Callable[[], list[str]]:
            """创建返回固定列表的侧效应"""
            return lambda: [f"{prefix}"]

        # ==================== 2. 基础市场数据 mock ====================
        # 批量获取类 API
        adapter.ctx.static_info.side_effect = list_factory("mock_static_info")
        adapter.ctx.quote.side_effect = list_factory("mock_quote")

        # 单个获取类 API
        adapter.ctx.depth.side_effect = single_factory("mock_depth")
        adapter.ctx.brokers.side_effect = single_factory("mock_broker")

        # 固定返回值 API
        adapter.ctx.participants.return_value = [
            "mock_participant_1",
            "mock_participant_2",
        ]

        # ==================== 3. 交易数据 mock ====================
        adapter.ctx.trades.side_effect = indexed_list_factory("mock_trades")
        adapter.ctx.intraday.side_effect = lambda symbol: [  # type: ignore
            f"mock_intraday: {symbol}_{i}" for i in range(1, 3)
        ]

        # ==================== 4. K线和历史数据 mock ====================
        adapter.ctx.candlesticks.side_effect = (
            lambda symbol, period, count, adjust_type, *args: [  # type: ignore
                f"mock_candle: {symbol}_{period}_{i}"
                for i in range(count)  # type: ignore
            ]
        )
        adapter.ctx.history_candlesticks_by_date.side_effect = (
            lambda symbol, period, adjust_type, *args: [  # type: ignore
                f"mock_history_candle: {symbol}_{period}_{i}"
                for i in range(5)  # type: ignore
            ]
        )

        # ==================== 5. 技术指标 mock ====================
        adapter.ctx.calc_indexes.side_effect = lambda symbols, indexes: [  # type: ignore
            f"mock_calc_index: {s}_{str(i)}"  # type: ignore
            for s in symbols  # type: ignore
            for i in indexes  # type: ignore
        ]

        # ==================== 6. 市场结构 mock ====================
        adapter.ctx.trading_session.side_effect = const_list_factory("mock_session")
        adapter.ctx.trading_days.side_effect = lambda market, begin, end: (  # type: ignore
            f"mock_trading_days: {market}_{begin.isoformat()}_{end.isoformat()}"  # type: ignore
        )
        adapter.ctx.capital_flow.side_effect = lambda symbol: [  # type: ignore
            f"mock_capital_flow: {symbol}_1",
            f"mock_capital_flow: {symbol}_2",
        ]
        adapter.ctx.capital_distribution.side_effect = lambda symbol: (  # type: ignore
            f"mock_capital_distribution: {symbol}"
        )
        adapter.ctx.market_temperature.side_effect = (
            lambda market: 7.5 if market == Market.US else 6.8  # type: ignore
        )
        adapter.ctx.history_market_temperature.side_effect = (
            lambda market, start, end: (  # type: ignore
                f"mock_history_market_temperature: {market}_{start.isoformat()}_{end.isoformat()}"  # type: ignore  # noqa: E501
            )
        )

        return adapter
