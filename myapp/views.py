from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess, os, json
from django.http import JsonResponse
from django.conf import settings
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create view.
def home(request):
    return render(request, 'index.html')

# Helper function to run deep learning script
def run_deeplearning(url,sumarize):
    logger.debug(f"Running deep learning script for URL: {url}")
    logger.debug(f"Running deep learning script for sumarize: {sumarize}")


    # Paths for script and output files
    script = 'myapp/scripts/deeplearning/main.py'
    output_file = "myapp/static/json_result/results.json"

    # Check if script path exists
    if not os.path.exists(script):
        logger.error(f"The script does not exist: {script}")
        raise FileNotFoundError(f"The script does not exist.")

    output = []
    try:
        # Run script with subprocess
        result = subprocess.run(['python', script, url,sumarize], check=True, capture_output=True, text=True, timeout=2500)
        logger.debug(f"Script output: {result.stdout}")
        logger.debug(f"Script errors (if any): {result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running the script: {e.stderr}")
        raise e
    except subprocess.TimeoutExpired as e:
        logger.error(f"Script timeout expired: {e}")
        raise e    
    
    # Read output file
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            output.append(json.load(f))
    else:
        logger.error(f"The output file does not exist: {output_file}")
        raise FileNotFoundError(f"The output file does not exist.")
    return output

# View for handling deep learning request
@csrf_exempt
def dl_url_from_view(request):
    if request.method == 'POST':
        url = request.POST.get('myurl')
        sumarize = request.POST.get('sum-approach')
        
        logger.debug(f"Received URL: {url}")
        logger.debug(f"Received sumarize: {sumarize}")
        
        try:
            output = run_deeplearning(url,sumarize)
            return render(request, 'result.html', {'output': output})
        except Exception as e:
            logger.error(f"Error processing URL: {e}")
            return HttpResponse(f"An error occurred: {e}", status=500)
    
    return render(request, 'index.html')

# Helper function to run traditional script
def run_traditional(url,num_clusters,driver,sumarize):

    # Paths for scripts and output files
    script = 'myapp/scripts/traditionalway+evaluation/main.py'
    script_screen = 'myapp/scripts/capture_screenshot.py'
    output_file = "myapp/static/json_result_tr/results.json"

    # Check if script path exists
    if not os.path.exists(script):
        raise FileNotFoundError(f"The script does not exist.")

    output = []

    try:
        # Run scripts with subprocess
        result = subprocess.run(['python', script, url,num_clusters,driver,sumarize], check=True, capture_output=True, text=True, timeout=1000)
        subprocess.run(['python', script_screen], check=True, capture_output=True, text=True, timeout=1000)
        logger.debug(f"Script output: {result.stdout}")
        logger.debug(f"Script errors (if any): {result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running the script: {e.stderr}")
        raise e
    except subprocess.TimeoutExpired as e:
        logger.error(f"Script timeout expired: {e}")
        raise e
    
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            output.append(json.load(f))
    else:
        logger.error(f"The output file does not exist: {output_file}")
        raise FileNotFoundError(f"The output file does not exist.")
    
    return output

# View for handling traditional method request
@csrf_exempt
def tr_url_from_view(request):
    
    if request.method == 'POST':
        url = request.POST.get('myurl')
        num_clusters = request.POST.get('num_clusters')
        driver = request.POST.get('driver')
        sumarize =  request.POST.get('sum-approach')
        
        logger.debug(f"Received URL: {url}")
        logger.debug(f"Received num_clusters: {num_clusters}")
        logger.debug(f"Received driver: {driver}")
        logger.debug(f"Received sumarize: {sumarize}")

        try:
            output = run_traditional(url,num_clusters,driver,sumarize)
            return render(request, 'result_tr.html', {'output': output})
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    
    return render(request, 'index.html')

# Helper function to run find number of clusters script
def run_findnumberofclusters(url):
    logger.debug(f"Find number of clusters script for URL: {url}")

    # Paths for scripts and output files
    scripttext = 'myapp/scripts/findnumofclusterstextbased/main.py'
    scriptimage = 'myapp/scripts/deeplearning/findnumofcluster.py'
    
    # Check if script path exists
    if not os.path.exists(scripttext):
        logger.error(f"The script does not exist: {scripttext}")
        raise FileNotFoundError(f"The script does not exist.")
    
    if not os.path.exists(scriptimage):
        logger.error(f"The script does not exist: {scriptimage}")
        raise FileNotFoundError(f"The script does not exist.")
    
    try:
        # Run scripts with subprocess
        resulttext = subprocess.run(['python', scripttext, url], check=True, capture_output=True, text=True, timeout=1000)
        resultimage = subprocess.run(['python', scriptimage, url], check=True, capture_output=True, text=True, timeout=1000)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running the script: {e.stderr}")
        raise e
    except subprocess.TimeoutExpired as e:
        logger.error(f"Script timeout expired: {e}")
        raise e
    
    return  resulttext.stdout.strip(), resultimage.stdout.strip()

# View for handling number of clusters request
@csrf_exempt
def num_url_from_view(request):
    if request.method == 'POST':
        url = request.POST.get('myurl')
        
        logger.debug(f"Received URL: {url}")

        try:
            resulttext,resultimage = run_findnumberofclusters(url)
            response_data = {
                'resulttext': resulttext,
                'resultimage': resultimage
            }
            return JsonResponse(response_data)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}", status=500)
    return render(request, 'index.html')

# View for deleting static files
@csrf_exempt 
def delete_static_files(request):
    if request.method == 'POST':
        # Define the paths of the directories want to clear
        folders_to_clear = [
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_audios'),
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_audios_tr'),
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_audios_summary'),
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_audios_summary_tr'),
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_images'),
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_audios_description'),
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_audios_description_tr'),
            os.path.join(settings.BASE_DIR, 'myapp/static/cropped_images_tr')
        ]
        
        # Delete files in each folder
        for folder in folders_to_clear:
            if os.path.isdir(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})











