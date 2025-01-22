from django.contrib import admin
from django import forms
from app.models import *
import json
# Register your models here.
# admin.site.register(FieldList)
# admin.site.register(Form)
# admin.site.register(FormFields)
# admin.site.register(FormAnswer)


class FormFieldsForm(forms.ModelForm):
    class Meta:
        model = FormFields
        fields = '__all__'

    def clean_option_value(self):
        option_value = self.cleaned_data.get('option_value')
        input_field_type = self.cleaned_data.get('field').input_field_type

        # Check if the input field type is 'radio' or 'checkbox'
        if input_field_type in ['radio', 'checkbox']:
            # Expect a user-friendly input like: "true, false" or "bike, car, boat"
            if not option_value:
                raise forms.ValidationError(
                    "You must enter options for radio or checkbox fields."
                )

            # Ensure it's a valid JSON format
            try:
                # Parse input and validate structure
                parsed_value = json.loads(option_value)

                if not isinstance(parsed_value, list) or not all(
                    isinstance(item, dict) and 'val' in item and 'is_check' in item
                    for item in parsed_value
                ):
                    raise forms.ValidationError(
                        "Invalid format. Example: "
                        '[{"val": true, "is_check": true}, {"val": false, "is_check": false}]'
                    )
            except json.JSONDecodeError:
                raise forms.ValidationError(
                    "Invalid JSON format. Provide valid JSON input."
                )

        return option_value
    
class FormFieldsInline(admin.TabularInline):
    model = FormFields
    extra = 1 
    fields = (
        'field', 
        'default_val', 
        'min', 
        'max', 
        'is_null', 
        'is_blank', 
        'is_unique', 
        'is_required', 
        'pattern_match', 
        'field_name', 
        'placeholder', 
        'index',
        'option_value'
    )
    show_change_link = True
    
    def save_model(self, request, obj, form, change):
        # Check if the input field type is radio or checkbox, then auto-format the `option_value`
        if obj.field.input_field_type in ['radio', 'checkbox']:
            user_input = form.cleaned_data.get('option_value')
            # Convert input string into the desired JSON format
            parsed_input = json.loads(user_input)

            # Example transformation: Ensure all items have 'is_check' and 'val' keys
            formatted_input = [
                {"val": item["val"], "is_check": item.get("is_check", False)}
                for item in parsed_input
            ]
            obj.option_value = formatted_input  # Save the formatted JSON
        super().save_model(request, obj, form, change)

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    inlines = [FormFieldsInline]

@admin.register(FieldList)
class FieldListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'input_field_type', 'created_at', 'updated_at')
    search_fields = ('name', 'input_field_type')  # Added to support autocomplete in FormFieldsAdmin

@admin.register(FormFields)
class FormFieldsAdmin(admin.ModelAdmin):
    list_display = ('id', 'form', 'field', 'field_name', 'index', 'created_at', 'updated_at')
    list_filter = ('form', 'field', 'is_required', 'is_unique')
    search_fields = ('field_name',)
    autocomplete_fields = ('form', 'field')  # Depends on search_fields in FormAdmin and FieldListAdmin

@admin.register(FormAnswer)
class FormAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'form_field', 'answer', 'created_at', 'updated_at')
    search_fields = ('answer',)
    autocomplete_fields = ('form_field',)
