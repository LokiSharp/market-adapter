from datetime import date
from typing import Type
import pytest
from modules.long_port_market_adapter import LongPortMarketAdapter
from longport.openapi import (
    Period,
    AdjustType,
    CalcIndex,
    TradeSessions,
    Market,
)


# 1. 基础数据查询测试类 - 参数化测试
class TestBasicDataQueries:
    @pytest.mark.parametrize(
        "method_name,args,expected",
        [
            # 单项查询方法
            ("fetch_static_info", ["AAPL.US"], "mock_static_info: AAPL.US"),
            ("fetch_quote", ["AAPL.US"], "mock_quote: AAPL.US"),
            ("fetch_depth", ["AAPL.US"], "mock_depth: AAPL.US"),
            ("fetch_brokers", ["AAPL.US"], "mock_broker: AAPL.US"),
        ],
    )
    def test_single_item_methods(
        self,
        mock_adapter: LongPortMarketAdapter,
        method_name: str,
        args: list[str],
        expected: str,
    ):
        """测试单项数据查询方法"""
        method = getattr(mock_adapter, method_name)
        result = method(*args)
        assert result == expected

    @pytest.mark.parametrize(
        "method_name,args,expected",
        [
            # 批量查询方法
            (
                "fetch_static_info_batch",
                [["AAPL.US", "TSLA.US"]],
                ["mock_static_info: AAPL.US", "mock_static_info: TSLA.US"],
            ),
            (
                "fetch_quote_batch",
                [["AAPL.US", "TSLA.US"]],
                ["mock_quote: AAPL.US", "mock_quote: TSLA.US"],
            ),
        ],
    )
    def test_batch_methods(
        self,
        mock_adapter: LongPortMarketAdapter,
        method_name: str,
        args: list[str],
        expected: str,
    ):
        """测试批量数据查询方法"""
        method = getattr(mock_adapter, method_name)
        result = method(*args)
        assert isinstance(result, list)
        assert result == expected

    def test_fetch_participants(self, mock_adapter: LongPortMarketAdapter):
        """测试获取做市商列表"""
        result = mock_adapter.fetch_participants()
        assert isinstance(result, list)
        assert result == ["mock_participant_1", "mock_participant_2"]

    def test_fetch_trades(self, mock_adapter: LongPortMarketAdapter):
        """测试获取成交记录"""
        result = mock_adapter.fetch_trades("AAPL.US", 10)
        assert isinstance(result, list)
        assert len(result) == 10
        assert result[0] == "mock_trades: AAPL.US_0"

    def test_fetch_quote_empty_symbol(self, mock_adapter: LongPortMarketAdapter):
        """测试传入空字符串的情况"""
        result = mock_adapter.fetch_depth("")
        assert result is None

    def test_fetch_quote_batch_empty_list(self, mock_adapter: LongPortMarketAdapter):
        """测试传入空列表的情况"""
        result = mock_adapter.fetch_quote_batch([])
        assert isinstance(result, list)
        assert len(result) == 0


# 2. 高级行情数据测试类
class TestAdvancedMarketData:
    def test_fetch_intraday(self, mock_adapter: LongPortMarketAdapter):
        """测试获取日内分时数据"""
        result = mock_adapter.fetch_intraday("AAPL.US")
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == "mock_intraday: AAPL.US_1"

    def test_fetch_candlesticks(self, mock_adapter: LongPortMarketAdapter):
        """测试获取K线数据"""
        result = mock_adapter.fetch_candlesticks(
            "AAPL.US", Period.Day, 5, AdjustType.NoAdjust, TradeSessions.All
        )
        assert isinstance(result, list)
        assert len(result) == 5
        assert result[0] == f"mock_candle: AAPL.US_{Period.Day}_0"

    def test_fetch_history_candlesticks_by_date(
        self, mock_adapter: LongPortMarketAdapter
    ):
        """测试获取历史K线数据"""
        result = mock_adapter.fetch_history_candlesticks_by_date(
            "AAPL.US", Period.Day, AdjustType.NoAdjust
        )
        assert isinstance(result, list)
        assert len(result) == 5
        assert result[0] == f"mock_history_candle: AAPL.US_{Period.Day}_0"

    @pytest.mark.parametrize(
        "period", [Period.Day, Period.Week, Period.Month, Period.Year]
    )
    def test_fetch_candlesticks_different_periods(
        self, mock_adapter: LongPortMarketAdapter, period: Type[Period]
    ):
        """测试不同K线周期参数"""
        result = mock_adapter.fetch_candlesticks(
            "AAPL.US", period, 5, AdjustType.NoAdjust, TradeSessions.All
        )
        assert result[0] == f"mock_candle: AAPL.US_{period}_0"


# 3. 市场结构和指标测试类
class TestMarketStructure:
    def test_fetch_trading_session(self, mock_adapter: LongPortMarketAdapter):
        """测试获取交易时段"""
        result = mock_adapter.fetch_trading_session()
        assert result[0] == "mock_session"

    def test_fetch_calc_indexes(self, mock_adapter: LongPortMarketAdapter):
        """测试获取技术指标"""
        indexes: list[Type[CalcIndex]] = [CalcIndex.LastDone, CalcIndex.ChangeValue]
        result = mock_adapter.fetch_calc_indexes(["AAPL.US", "GOOG.US"], indexes)
        assert isinstance(result, list)
        assert len(result) == 4
        assert "mock_calc_index: AAPL.US_CalcIndex.LastDone" in result
        assert "mock_calc_index: GOOG.US_CalcIndex.ChangeValue" in result

    def test_fetch_market_temperature(self, mock_adapter: LongPortMarketAdapter):
        """测试获取市场温度"""
        result = mock_adapter.fetch_market_temperature(Market.US)
        assert result == 7.5
        result_hk = mock_adapter.fetch_market_temperature(Market.HK)
        assert result_hk == 6.8

    def test_fetch_history_market_temperature(
        self, mock_adapter: LongPortMarketAdapter
    ):
        """测试获取历史市场温度"""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 5)
        result = mock_adapter.fetch_history_market_temperature(
            Market.US, start_date, end_date
        )
        assert (
            result == "mock_history_market_temperature: Market.US_2023-01-01_2023-01-05"
        )

    def test_fetch_trading_days(self, mock_adapter: LongPortMarketAdapter):
        """测试获取交易日历"""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 31)
        result = mock_adapter.fetch_trading_days(Market.US, start_date, end_date)

        # 验证返回的是交易日历对象
        assert result is not None
        assert (
            result
            == "mock_trading_days: "
            + f"{Market.US}_{start_date.isoformat()}_{end_date.isoformat()}"
        )

    def test_fetch_capital_flow(self, mock_adapter: LongPortMarketAdapter):
        """测试获取标的的资金流向数据"""
        result = mock_adapter.fetch_capital_flow("AAPL.US")

        # 验证返回的是资金流向数据列表
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == "mock_capital_flow: AAPL.US_1"
        assert result[1] == "mock_capital_flow: AAPL.US_2"

    def test_fetch_capital_distribution(self, mock_adapter: LongPortMarketAdapter):
        """测试获取标的的资金分布数据"""
        result = mock_adapter.fetch_capital_distribution("AAPL.US")

        # 验证返回的是资金分布数据对象
        assert result is not None
        assert result == "mock_capital_distribution: AAPL.US"
