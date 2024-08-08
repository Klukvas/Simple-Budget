from django.urls import path 
from .views import (
    CustomerSignUpView, CustomerLoginView,

    CategoryListView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView,

    SubcategoryListView, SubCategoryCreateView, GetSubcategoriesView, SubcategoryDetailView, SubcategoryDeleteView,

    SpendListView, SpendCreateView,

    spends_by_category_compare_prev_month, CurrentMonthSpendsView,

    AccountUpdateView
    
)

app_name = 'blog'

urlpatterns = [
    path('signup/', CustomerSignUpView.as_view(), name='signup'),
    path('login/', CustomerLoginView.as_view(), name='login'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/<int:pk>/', CategoryUpdateView.as_view(), name='category_detail'),


    
    path('get-subcategories/<int:category_id>/', GetSubcategoriesView.as_view(), name='get_subcategories'),


    path('subcategories/', SubcategoryListView.as_view(), name='subcategories'),
    path('subcategory/create/', SubCategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategory/<int:pk>/', SubcategoryDetailView.as_view(), name='subcategory_detail'),
    path('subcategory/<int:pk>/delete/', SubcategoryDeleteView.as_view(), name='subcategory_delete'),



    path('spends/', SpendListView.as_view(), name='spends'),
    path('spend/create/', SpendCreateView.as_view(), name='spend_create'),

    path('dashboard/compare_previous_month', spends_by_category_compare_prev_month,  name='compare_previous_month'),
    path('dashboard/current_month_spends', CurrentMonthSpendsView.as_view(),  name='current_month_spends'),


    path('account/info/', AccountUpdateView.as_view(), name='account_info'),
]
