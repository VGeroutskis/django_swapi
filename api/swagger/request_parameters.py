from drf_yasg import openapi

# For FilterByNameMixin
NAME_PARAMETER = openapi.Parameter(
    'name',
    openapi.IN_QUERY,
    description="Search by name",
    type=openapi.TYPE_STRING
)

# For FilterByTitleMixin
TITLE_PARAMETER = openapi.Parameter(
    'title',
    openapi.IN_QUERY,
    description="Search by title",
    type=openapi.TYPE_STRING
)
