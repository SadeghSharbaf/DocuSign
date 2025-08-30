from django.shortcuts import render, redirect,get_object_or_404
from .models import Contract
from django.views.generic import CreateView,DetailView,ListView,TemplateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .dropbox_service import Create_Embedded_Signature_Request
from django.urls import reverse_lazy



class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    fields = ['recipient_name' ,'recipient_email']
    template_name = "contract/contract_create.html"
    success_url = reverse_lazy("contract_list")
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
    
    

class ContractListView(LoginRequiredMixin,ListView):
    model = Contract
    template_name = "contract/contract_list.html"
    
    
    def get_queryset(self):
        return Contract.objects.filter(creator = self.request.user)
    
    

class ContractDetailView(LoginRequiredMixin,DetailView):
    model = Contract
    template_name = "contract/contract_detail.html"
    
    
    def get_queryset(self):
        return Contract.objects.filter(creator = self.request.user)
    
    
    
    
def Register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("contract_list")
        
    else:
        form = UserCreationForm()
    
    return render(request, "registration/register.html", {"form": form})




from django.http import JsonResponse
from django.conf import settings
from dropbox_sign import ApiClient,Configuration,apis


def test_dropbox(request):
    config = Configuration(username=settings.DROPBOX_SIGN["api_key"])
    client = ApiClient(configuration=config)
    signature_api = apis.SignatureRequestApi(client)

    try:
        result = signature_api.signature_request_list()
        return JsonResponse(result.to_dict())
    except Exception as e:
        return JsonResponse({"error": str(e)})
    
    

# this view for signing 
def ContractSignView(request, pk):
    contract = get_object_or_404(Contract, pk=pk, creator = request.user)
    
    
    if contract.signing_url:
        return redirect(contract.signing_url)
    
    signature_request_id, signing_url = Create_Embedded_Signature_Request(
        signer1_name=request.user.username,
        signer1_email=request.user.email,
        signer2_name=contract.recipient_name,
        signer2_email=contract.recipient_email,
        file_url= None,
        test_mode= True
    )
    
    contract.envelope_id = signature_request_id
    contract.signing_url = signing_url
    contract.save()
    
    return redirect(signing_url)




class ContractSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "contract/success.html"
    
    
class ContractDeleteView(LoginRequiredMixin, DeleteView):
    model = Contract
    template_name = "contract/contract_confirm_delete.html"
    success_url = reverse_lazy("contract_list")
    
    
    
    
from django.http import JsonResponse
import requests
from django.conf import settings

def test_account(request):
    api_key = settings.DROPBOX_SIGN["api_key"]
    base = settings.DROPBOX_SIGN.get("base_url", "https://api.hellosign.com/v3")
    r = requests.get(f"{base}/account", auth=(api_key, ""))
    return JsonResponse({
        "status": r.status_code,
        "headers": dict(r.headers),
        "body": r.text[:1000],
    })

def test_embedded_raw(request):
    api_key = settings.DROPBOX_SIGN["api_key"]
    base = settings.DROPBOX_SIGN.get("base_url", "https://api.hellosign.com/v3")
    client_id = settings.DROPBOX_SIGN.get("client_id")

    data = {
        "client_id": client_id,
        "test_mode": "1",
        "signers[0][name]": "Alice Test",
        "signers[0][email_address]": "alice@example.com",
        "signers[1][name]": "Bob Test",
        "signers[1][email_address]": "bob@example.com",
        "file_url[0]": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    }
    r = requests.post(f"{base}/signature_request/create_embedded", auth=(api_key, ""), data=data)
    return JsonResponse({
        "status": r.status_code,
        "headers": dict(r.headers),
        "body": r.text[:1000],
    })
