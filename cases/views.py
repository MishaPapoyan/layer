from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LegalCase, CaseAnalysis
from .forms import CaseAnalysisForm


def cases_home(request):
    """Case laboratory home"""
    cases = LegalCase.objects.filter(is_active=True)
    
    context = {
        'cases': cases,
    }
    return render(request, 'cases/home.html', context)


@login_required
def case_detail(request, pk):
    """Case detail page"""
    case = get_object_or_404(LegalCase, pk=pk, is_active=True)
    
    # Check if user has already submitted analysis
    user_analysis = CaseAnalysis.objects.filter(case=case, user=request.user).first()
    
    context = {
        'case': case,
        'user_analysis': user_analysis,
    }
    return render(request, 'cases/case_detail.html', context)


@login_required
def submit_analysis(request, pk):
    """Submit case analysis"""
    case = get_object_or_404(LegalCase, pk=pk, is_active=True)
    
    # Check if already submitted
    existing = CaseAnalysis.objects.filter(case=case, user=request.user).first()
    if existing:
        messages.info(request, 'You have already submitted an analysis for this case.')
        return redirect('cases:case_detail', pk=pk)
    
    if request.method == 'POST':
        form = CaseAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.case = case
            analysis.user = request.user
            analysis.save()
            messages.success(request, 'Your analysis has been submitted successfully!')
            return redirect('cases:case_detail', pk=pk)
    else:
        form = CaseAnalysisForm()
    
    context = {
        'case': case,
        'form': form,
    }
    return render(request, 'cases/submit_analysis.html', context)

