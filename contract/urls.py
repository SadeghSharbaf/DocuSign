from django.urls import path
from .views import ContractCreateView,ContractDetailView,ContractListView,test_dropbox,ContractSignView,ContractSuccessView,ContractDeleteView

from .views import test_account, test_embedded_raw
urlpatterns = [
    path('new/', ContractCreateView.as_view(), name= "contract_create"),
    path('list/', ContractListView.as_view(), name= "contract_list"),
    path('detail/<int:pk>/', ContractDetailView.as_view(), name= "contract_detail"),
    path('sign/<int:pk>/', ContractSignView, name="contract_sign"),
    path("contract/success/", ContractSuccessView.as_view(), name="contract_success"),
    path('delete/<int:pk>/', ContractDeleteView.as_view(), name="contract_delete"),
    
    path('test-api/', test_dropbox, name= "test_api"),
    
    
]
urlpatterns += [
    path("test-account/", test_account, name="test_account"),
    path("test-embedded/", test_embedded_raw, name="test_embedded"),
]