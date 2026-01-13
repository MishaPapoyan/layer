from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.conf import settings
import json
import os
from .models import ApplicationType, ApplicationField, ApplicationTemplate, GeneratedApplication
from .forms import DynamicApplicationForm


@login_required
def application_generator(request):
    """Application Generator home page"""
    application_types = ApplicationType.objects.filter(is_active=True).order_by('order')
    
    context = {
        'application_types': application_types,
    }
    return render(request, 'applications/generator.html', context)


@login_required
def create_application(request, app_type_id):
    """Create application form"""
    application_type = get_object_or_404(ApplicationType, pk=app_type_id, is_active=True)
    
    if request.method == 'POST':
        form = DynamicApplicationForm(application_type, request.POST)
        if form.is_valid():
            # Store form data
            field_data = {}
            for field_name, value in form.cleaned_data.items():
                field_data[field_name] = str(value) if value is not None else ''
            
            # Generate document
            try:
                generated_file = generate_document(application_type, field_data)
                
                # Save to database
                generated_app = GeneratedApplication.objects.create(
                    user=request.user,
                    application_type=application_type,
                    field_data=field_data,
                    generated_file=generated_file
                )
                
                messages.success(request, 'Application generated successfully!')
                return redirect('applications:download', pk=generated_app.pk)
            except Exception as e:
                messages.error(request, f'Error generating document: {str(e)}')
    else:
        form = DynamicApplicationForm(application_type)
    
    context = {
        'application_type': application_type,
        'form': form,
    }
    return render(request, 'applications/create.html', context)


@login_required
def download_application(request, pk):
    """Download generated application"""
    generated_app = get_object_or_404(GeneratedApplication, pk=pk, user=request.user)
    
    if generated_app.generated_file:
        file_path = generated_app.generated_file.path
        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )
    
    messages.error(request, 'File not found.')
    return redirect('applications:generator')


@login_required
def my_applications(request):
    """User's generated applications"""
    applications = GeneratedApplication.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'applications': applications,
    }
    return render(request, 'applications/my_applications.html', context)


def generate_document(application_type, field_data):
    """Generate PDF or DOCX document from template"""
    try:
        template = ApplicationTemplate.objects.get(application_type=application_type, is_active=True)
    except ApplicationTemplate.DoesNotExist:
        raise Exception('Template not found for this application type.')
    
    # Get template content
    template_content = template.template_content
    
    # Replace placeholders with actual data
    for field_name, value in field_data.items():
        placeholder = f'{{{{{field_name}}}}}'
        template_content = template_content.replace(placeholder, str(value))
    
    # For now, create a simple text file
    # In production, use libraries like reportlab for PDF or python-docx for DOCX
    import tempfile
    from django.core.files.base import ContentFile
    
    file_extension = 'txt'  # Default to txt for now
    if template.template_format == 'pdf':
        file_extension = 'pdf'
    elif template.template_format == 'docx':
        file_extension = 'docx'
    
    filename = f"{application_type.name.replace(' ', '_')}_{template.template_format}.{file_extension}"
    
    # Create file content
    file_content = ContentFile(template_content.encode('utf-8'))
    
    return file_content
