import os
import whisper
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from dotenv import load_dotenv # Run: pip install python-dotenv
from .forms import AudioUploadForm
from .models import TeamMember
from .processor import advanced_ai_processor 

load_dotenv()

def task_assignment_view(request):
    results = []
    error_message = None
    # Securely get key from .env
    API_KEY = os.getenv("OPENAI_API_KEY")

    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio_file']
            path = default_storage.save('temp_audio.mp3', ContentFile(audio_file.read()))
            tmp_file_path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, path))
            
            try:
                model = whisper.load_model("base") 
                stt_result = model.transcribe(tmp_file_path, fp16=False)
                transcript = stt_result['text']
                
                team_data = list(TeamMember.objects.all().values('name', 'role', 'skills'))
                # Call processor
                results = advanced_ai_processor(transcript, team_data, API_KEY)

            except Exception as e:
                error_message = f"Processing Error: {str(e)}"
            finally:
                if os.path.exists(tmp_file_path):
                    os.remove(tmp_file_path)
    else:
        form = AudioUploadForm()

    return render(request, 'tasks/results.html', {'form': form, 'tasks': results, 'error_message': error_message})