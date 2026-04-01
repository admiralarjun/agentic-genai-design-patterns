from google.adk.agents.llm_agent import Agent
import yfinance as yf

async def get_stock_data(ticker: str) -> dict:
    """
    Get stock price and basic info using yfinance
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "status": "success",
            "ticker": ticker,
            "price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}

async def get_financials(ticker: str) -> dict:
    """
    Get financial metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "status": "success",
            "ticker": ticker,
            "revenue_growth": info.get("revenueGrowth"),
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


async def get_news(ticker: str) -> dict:
    """
    Get latest news using yfinance
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.get_news()

        headlines = [n.get("title") for n in news[:5]]

        return {
            "status": "success",
            "ticker": ticker,
            "headlines": headlines
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


# -----------------------------
# AGENT
# -----------------------------
root_agent = Agent(
    model='gemini-2.5-flash',
    name='financial_async_agent',
    description='Parallel financial analysis using real-world data sources.',
    instruction="""
You are a financial analysis agent.

Step 0: Extract the stock ticker from user input.
- Example: Tesla → TSLA, Apple → AAPL

Step 1: You MUST call ALL tools:
- get_stock_data
- get_financials
- get_news

IMPORTANT:
- These tools are independent
- Execute ALL tool calls in parallel
- Do NOT skip tool calls
- Do NOT answer without calling tools first

Step 2: Analyze:
- Market performance (price + change)
- Financial strength (growth + margins)
- News signals (based on headlines)

Step 3: Output:
- Summary (2-3 lines)
- Risk level (low / medium / high)
- Key insights
- 2 recommendations
""",
    tools=[
        get_stock_data,
        get_financials,
        get_news
    ],
)
