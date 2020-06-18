from django.contrib.admin import ModelAdmin


class EmailModelAdmin(ModelAdmin):
    list_display  = ['full_name', 'created_at']
    list_filter   = ['created_at', 'updated_at']
    search_fields = ['full_name', 'email']
    list_per_page = 10

    fieldsets     = (
        ("Basic Information", {
            "classes" : ["extrapretty"],
            "fields" : ["full_name"]
        }),
        ("Contact information", {
            "classes" : ["collapse", "extrapretty"],
            "fields" : ["email"]
        }),
        ("Message", {
            "classes" : ["collapse", "extrapretty"],
            "fields" : ["content"]
        })
    )