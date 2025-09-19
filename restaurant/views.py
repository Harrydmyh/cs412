# File: restaurant/views.py
# Author: Yihang Duanmu (harrydm@bu.edu), 9/16/2025
# Description: Views for the restaurant application

from django.shortcuts import render
import time
import random

# Special dish list
special = [
    "Strawberry cheesecake $10",
    "Blueberry cheesecake $10",
    "Raspberry cheesecake $10",
]


# Create your views here.
def main(request):
    """return the main page for the restaurant application"""
    template_name = "restaurant/main.html"
    context = {"time": time.ctime()}
    return render(request, template_name, context)


def order(request):
    """return the order page for the restaurant application"""
    template_name = "restaurant/order.html"
    context = {"time": time.ctime()}

    # choose special dish
    special_index = random.randint(0, 2)
    special_dish = special[special_index]
    context["special"] = special_dish

    return render(request, template_name, context)


def confirmation(request):
    """handle the order submission"""
    template_name = "restaurant/confirmation.html"

    if request.POST:
        reply = request.POST
        print(reply)

        # Pick a random order-done time
        now = time.time()
        offset = random.randint(30 * 60, 60 * 60)
        future = now + offset
        future_str = time.ctime(future)

        # a list for all the food
        food_list = [
            "Ratatouille",
            "Add-on: beef",
            "Add-on: chicken",
            "Add-on: sausage",
            "Linguini's Soup Special",
            "Salmon on Caesar Salad",
        ]

        # find all the ordered food and the total price
        total = 0
        ordered_list = []
        for food in food_list:
            if food in reply and reply[food] != "":
                ordered_list.append(food)
                total += int(reply[food])

        if "special" in reply and reply["special"] != "":
            ordered_list.append(reply["special"].split("$")[0].strip())
            total += 10
        print(ordered_list)
        # find special instruction
        print(reply["special_instructions"])
        if reply["special_instructions"] != "":
            instructions = reply["special_instructions"]
        else:
            instructions = ""

        # finalize the context variable
        context = {
            "time": time.ctime(),
            "ready_time": future_str,
            "orders": ordered_list,
            "special_request": instructions,
            "total": f"${total}",
            "name": f"Name: {reply["name"]}",
            "phone": f"Phone: {reply["phone"]}",
            "email": f"Email: {reply["email"]}",
        }

        return render(request, template_name, context)
    else:
        return order(request)
