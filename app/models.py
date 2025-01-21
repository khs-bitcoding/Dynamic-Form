from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class FieldList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    input_field_type = models.CharField(
        max_length=50, 
        help_text="e.g., number, text, password, radio, checkbox"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Form(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FormFields(models.Model):
    id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='fields')
    field = models.ForeignKey(FieldList, on_delete=models.CASCADE, related_name='form_fields')
    default_val = models.CharField(max_length=255, blank=True, null=True)
    min = models.CharField(max_length=255, blank=True, null=True)
    max = models.CharField(max_length=255, blank=True, null=True)
    is_null = models.BooleanField(default=False)
    is_blank = models.BooleanField(default=False)
    is_unique = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)
    pattern_match = models.CharField(max_length=255, blank=True, null=True)
    field_name = models.CharField(max_length=255)
    placeholder = models.CharField(max_length=255, default="")    
    index = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.field_name} ({self.form.name})"


class FormAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    form_field = models.ForeignKey(FormFields, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer for {self.form_field.field_name}"
