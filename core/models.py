from django.db import models

# Customer Model
# -------------------------
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name

# -------------------------
# Tailor Model
# -------------------------
class Tailor(models.Model):
    name = models.CharField(max_length=100)
    shop_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"{self.shop_name} ({self.name})"

# -------------------------
# Fabric Model
# -------------------------
class Fabric(models.Model):
    name = models.CharField(max_length=100)
    quantity_in_meters = models.FloatField()
    price_per_meter = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.quantity_in_meters}m"

# -------------------------
# Measurement Model
# -------------------------
class Measurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shoulder = models.FloatField()
    chest = models.FloatField()
    waist = models.FloatField()
    hip = models.FloatField()
    height = models.FloatField()
    visual_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.customer.name}'s Measurements"

# -------------------------
# Order Model
# -------------------------
ORDER_STATUS_CHOICES = [
    ("Received", "Received"),
    ("Cutting", "Cutting Started"),
    ("Stitching", "Stitching"),
    ("Trial", "Trial Ready"),
    ("Delivery", "Out for Delivery"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
]

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True)
    tailor = models.ForeignKey(Tailor, on_delete=models.SET_NULL, null=True)
    style_notes = models.TextField()
    measurement = models.ForeignKey(Measurement, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="Received")
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField()
    created_at = models.DateTimeField (auto_now_add=True)
    design_image = models.ImageField(upload_to='designs/', null=True, blank=True,  help_text="Customer uploaded design sketch or reference image")
    def __str__(self):
        return f"Order #{self.id} for {self.customer.name} - {self.status}"
