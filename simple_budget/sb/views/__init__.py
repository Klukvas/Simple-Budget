from .login import CustomerLoginView
from .signup import CustomerSignUpView
from .category import CategoryListView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView
from .subcategory import SubCategoryCreateView, SubcategoryListView, GetSubcategoriesView, SubCategoryUpdateView, SubcategoryDeleteView
from .spend import SpendListView, SpendCreateView
from .dashboard import spends_by_category_compare_prev_month, CurrentMonthSpendsView
from .account import AccountUpdateView
