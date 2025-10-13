from django.contrib.auth import logout
from django.shortcuts import redirect


async def logout_view(request):
    logout(request)
    return redirect("login")
