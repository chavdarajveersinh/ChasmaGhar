from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage, Order, Product, UserAccount
from django.contrib import messages


# ---------------------- AUTH SYSTEM ----------------------

def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not fullname or not email or not password or not confirm_password:
            messages.error(request, "⚠️ All fields are required!")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "❌ Passwords do not match!")
            return render(request, "register.html")

        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, "⚠️ Email already registered! Please login.")
            return render(request, "register.html")

        UserAccount.objects.create(username=fullname, email=email, password=password)
        messages.success(request, f"🎉 Welcome {fullname}! Your account has been created successfully.")
        return redirect("login")

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "⚠️ Both Username and Password are required!")
            return render(request, "login.html")

        try:
            user = UserAccount.objects.get(username=username, password=password)
            request.session["username"] = user.username
            request.session["email"] = user.email

            messages.success(request, f"✅ Welcome back, {user.username}!")
            return redirect("home")

        except UserAccount.DoesNotExist:
            messages.error(request, "❌ Invalid credentials! Please register first.")
            return render(request, "login.html")

    return render(request, "login.html")


def logout(request):
    request.session.flush()
    storage = messages.get_messages(request)
    storage.used = True
    messages.success(request, "👋 You have been logged out successfully.")
    return redirect("login")


# ---------------------- MAIN PAGES ----------------------

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


# ---------------------- ORDERS ----------------------

def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        payment = request.POST.get('payment', '').strip()

        if name and email and address and payment:
            Order.objects.create(
                product=product,
                customer_name=name,
                email=email,
                address=address,
                payment=payment
            )
            return render(request, 'thankyou.html', {'product': product, 'name': name})

    return render(request, 'checkout.html', {'product': product})


def instant_buy(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Order.objects.create(
        product=product,
        customer_name="Guest",
        email="N/A",
        address="N/A",
        payment="COD"
    )
    return render(request, 'thankyou.html', {'product': product})


# ---------------------- EXTRA PAGES ----------------------

def offer(request):
    return render(request, 'offer.html')


def thankyou(request):
    return render(request, 'thankyou.html')
