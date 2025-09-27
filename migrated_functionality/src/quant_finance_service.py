import gradio as gr
import yfinance as yf
import pandas as pd
import requests
import json
from datetime import datetime, timedelta

def get_stock_data(symbol, period="1mo"):
    """Get stock data using yfinance"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        return f"Stock data for {symbol}:\n{data.tail().to_string()}"
    except Exception as e:
        return f"Error fetching data for {symbol}: {str(e)}"

def analyze_portfolio(symbols, period="1mo"):
    """Analyze portfolio performance"""
    try:
        portfolio_data = {}
        for symbol in symbols.split(','):
            symbol = symbol.strip()
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            if not data.empty:
                portfolio_data[symbol] = {
                    'current_price': data['Close'].iloc[-1],
                    'change': data['Close'].iloc[-1] - data['Close'].iloc[0],
                    'change_pct': ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                }
        
        result = "Portfolio Analysis:\n"
        result += "=" * 50 + "\n"
        for symbol, data in portfolio_data.items():
            result += f"{symbol}: ${data['current_price']:.2f} "
            result += f"({data['change']:+.2f}, {data['change_pct']:+.2f}%)\n"
        
        return result
    except Exception as e:
        return f"Error analyzing portfolio: {str(e)}"

def ai_financial_advice(query):
    """Get AI financial advice using Ollama"""
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                               json={'model': 'llama3.1:8b', 
                                     'prompt': f"Provide financial advice for: {query}. Be concise and practical.", 
                                     'stream': False})
        if response.status_code == 200:
            return response.json().get('response', 'AI Response: ' + query)
        else:
            return f'AI Response: {query}'
    except:
        return f'AI Response: {query}'

def create_interface():
    with gr.Blocks(title='IZA OS Quantitative Finance Service') as demo:
        gr.Markdown('# 📈 IZA OS Quantitative Finance Service')
        gr.Markdown('**Powered by yfinance, pandas, and Ollama AI**')
        
        with gr.Tab("Stock Analysis"):
            with gr.Row():
                symbol_input = gr.Textbox(label='Stock Symbol', placeholder='AAPL, TSLA, etc.')
                period_input = gr.Dropdown(choices=['1d', '5d', '1mo', '3mo', '6mo', '1y'], value='1mo', label='Period')
                analyze_btn = gr.Button('Analyze Stock')
            stock_output = gr.Textbox(label='Stock Data', lines=10)
            analyze_btn.click(get_stock_data, inputs=[symbol_input, period_input], outputs=stock_output)
        
        with gr.Tab("Portfolio Analysis"):
            with gr.Row():
                portfolio_input = gr.Textbox(label='Portfolio Symbols', placeholder='AAPL,TSLA,MSFT,GOOGL')
                portfolio_period = gr.Dropdown(choices=['1d', '5d', '1mo', '3mo', '6mo', '1y'], value='1mo', label='Period')
                portfolio_btn = gr.Button('Analyze Portfolio')
            portfolio_output = gr.Textbox(label='Portfolio Analysis', lines=10)
            portfolio_btn.click(analyze_portfolio, inputs=[portfolio_input, portfolio_period], outputs=portfolio_output)
        
        with gr.Tab("AI Financial Advisor"):
            with gr.Row():
                advice_input = gr.Textbox(label='Financial Question', placeholder='Should I invest in tech stocks?')
                advice_btn = gr.Button('Get AI Advice')
            advice_output = gr.Textbox(label='AI Financial Advice', lines=8)
            advice_btn.click(ai_financial_advice, inputs=advice_input, outputs=advice_output)
    
    return demo

if __name__ == '__main__':
    demo = create_interface()
    demo.launch(server_port=8083, share=False)
