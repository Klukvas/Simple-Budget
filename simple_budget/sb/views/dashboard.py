from sb.models import Spend

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render


def spends_by_category_compare_prev_month(request):
    spends = Spend.objects.spends_for_current_and_previous_months_by_category()

    data = [
        {
            'category': spend['category_name'],
            'month': f"{spend['year']}-{spend['month']:02d}",
            'total_amount': spend['total_amount']
        }
        for spend in spends
    ]

    # Transform data to match Plotly format
    categories = [item['category'] for item in data]
    months = [item['month'] for item in data]
    amounts = [item['total_amount'] for item in data]

    # Create the plot
    fig = px.bar(x=categories, y=amounts, color=months, labels={'x': 'Category', 'y': 'Total Amount'},
                 title='Monthly Comparison by Category', barmode='group')
    graph_div = fig.to_html(full_html=False)
    return render(request, 'sb/dashboard/tabs/compare_prev_month.html', {'graph_div': graph_div})


class ChartGenerator:

    @staticmethod
    def category_max_spend(spends):
        charts = []
        for spend in spends:
            fig = go.Figure(go.Indicator(
                domain={'x': [0, 1], 'y': [0, 1]},
                value=spend['current_spend'],
                mode="gauge+number+delta",
                title={'text': spend['category_name']},
                gauge={
                    'axis': {'range': [None, spend['max_spend']]},
                    'steps': [
                        {'range': [0, spend['max_spend'] * 0.5], 'color': "lightgray"},
                        {'range': [spend['max_spend'] * 0.5, spend['max_spend'] * 0.8], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': spend['max_spend'] * 0.98
                    }
                },
                number={'valueformat': '.0f'},
                delta={'valueformat': '.0f'}
            ))
            graph_div = pyo.plot(fig, output_type='div', include_plotlyjs=False)
            charts.append(graph_div)
        return charts

    @staticmethod
    def spends_by_category(spends):
        labels = [spend['category_name'] for spend in spends]
        data = [spend['total_amount'] for spend in spends]
        fig = px.bar(x=labels, y=data, labels={'x': 'Category', 'y': 'Total Amount'}, title='Spend by Category')
        chart = fig.to_html(full_html=False)
        return chart


class CurrentMonthSpendsView(LoginRequiredMixin, TemplateView):
    template_name = 'sb/dashboard/tabs/current_month.html'
    login_url = "/simple-budget/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        spends_by_category = Spend.objects.spends_for_current_month_by_category()
        category_max_spend = Spend.objects.current_month_spends_with_max_allowed_by_category()

        context['by_category_chart'] = ChartGenerator.spends_by_category(spends_by_category) if spends_by_category else None
        context['spends'] = spends_by_category

        context['max_spend_charts'] = ChartGenerator.category_max_spend(category_max_spend) if category_max_spend else None

        return context    
