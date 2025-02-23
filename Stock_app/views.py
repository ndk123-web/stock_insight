from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf

def home(request):
    stock_name = ""  
    if request.method == 'POST':
        stock_name = request.POST.get('stockSymbol', '')  
    return render(request, 'index.html', {'stock_name': stock_name})

def get_stock(request, stock_name):
    print("Fetching data for:", stock_name)

    if not stock_name:
        return JsonResponse({"error": "Stock name is required"}, status=400)

    try:
        # **Check if it's an Indian Stock**
        is_indian_stock = not stock_name.endswith((".NS", ".BO"))

        if is_indian_stock:
            test_stock = yf.Ticker(stock_name)
            hist = test_stock.history(period="1mo")

            if hist.empty:  # Agar US market se nahi mila, to NSE try karo
                stock_name += ".NS"
        
        stock = yf.Ticker(stock_name)
        hist = stock.history(period="1mo")

        if hist.empty:
            return JsonResponse({"error": f"No data found for {stock_name}"}, status=404)

        prices = hist["Close"].tolist()
        timestamps = hist.index.strftime('%Y-%m-%d').tolist()

        return JsonResponse({"timestamps": timestamps, "prices": prices})
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
