from django.contrib import admin

from .models.knowledge import Disease, Prevention, Reference, Treatment


class TreatmentInline(admin.StackedInline):
    model = Treatment
    extra = 1


class PreventionInline(admin.StackedInline):
    model = Prevention
    extra = 1


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("name", "crop", "severity", "version", "created_at")
    list_filter = ("crop", "severity", "version")
    search_fields = ("name", "crop", "symptoms")
    inlines = [TreatmentInline, PreventionInline, ReferenceInline]


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("disease", "type")
    list_filter = ("type",)
    search_fields = ("disease__name", "method")


@admin.register(Prevention)
class PreventionAdmin(admin.ModelAdmin):
    list_display = ("disease", "timing")
    search_fields = ("disease__name", "measure")


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ("disease", "source_name")
    search_fields = ("disease__name", "source_name")
