from django.contrib import admin
from .models import Article
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Article import_export
class ArticleAdmin(ImportExportModelAdmin):
    pass


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article
        fields = ('id', 'title', 'author', 'tags', 'body', 'date', 'archive', )  # These are the fields I want to import
        export_order = ('id', 'title', 'author', 'tags', 'body', 'date', 'archive', )  # This is the order for export
        # Let me know what's happening
        skip_unchanged = True
        report_skipped = True

admin.site.register(Article, ArticleAdmin)
