from .models import Jobs,JobDetail,Location,Type,JobFunctions,Industries
from .serializers import JobSerializer,JobDetailSerializer,JobFunctionSerializer,JobLocationSerializer,JobTimeSerializer,IndustriesSerializer
from bs4 import BeautifulSoup
import requests
from rest_framework import viewsets
from rest_framework.response import Response

# Create your views here.
url='https://www.brightermonday.co.ke/jobs'

job_soup=BeautifulSoup()
page = requests.get(url)
if page.status_code==200:
        soup=BeautifulSoup(page.content,'html.parser')
        select_functions = soup.find('select', class_='w-full h-10 pl-2 text-gray-500 rounded-md border border-gray-300 hover:border-gray-400 focus:border-gray-400 placeholder-gray-400 focus:placeholder-gray-900 mb-3 w-full md:mb-0 md:mr-3', attrs={'aria-label': 'Select a job function'})
        option_functions = select_functions.find_all('option')
        # options = [option.get('value') for option in option_functions]
        for option in option_functions:
            scrapped_functions=JobFunctions()
            scrapped_functions.jobFunction=option.get('value')
            scrapped_functions.save()
        
        select_industries = soup.find('select', class_='w-full h-10 pl-2 text-gray-500 rounded-md border border-gray-300 hover:border-gray-400 focus:border-gray-400 placeholder-gray-400 focus:placeholder-gray-900 mb-3 w-full md:mb-0 md:mr-3', attrs={'aria-label': 'Select an industry'})
        option_industries = select_industries.find_all('option')
        # options = [option.get('value') for option in option_industries]
        for option in option_industries:
            scrapped_industries=Industries()
            scrapped_industries.industry=option.get('value')
            scrapped_industries.save()
        
        select_locations = soup.find('select', class_='w-full h-10 pl-2 text-gray-500 rounded-md border border-gray-300 hover:border-gray-400 focus:border-gray-400 placeholder-gray-400 focus:placeholder-gray-900 mb-3 w-full md:mb-0 md:mr-3', attrs={'aria-label': 'Select a location'})
        option_locations = select_locations.find_all('option')
        # options = [option.get('value') for option in option_locations]
        for option in option_locations:
            scrapped_location=Location()
            scrapped_location.location=option.get('value')
            scrapped_location.save()
        
        # job_type=soup.find('div',class_='flex flex-wrap mt-3 text-sm text-gray-500 md:py-0')
        # span_elements = job_type.find_all('span')
        # # if len(span_elements) >= 1:
        # #     first_span_text = span_elements[0].get_text(strip=True)
        # #     print(first_span_text)
        # if len(span_elements) >= 2:
        #     scrapped_type=Type()
        #     second_span_text = span_elements[1].get_text(strip=True)
        #     scrapped_type.time=second_span_text
        #     scrapped_type.save()
            
            
        soup = BeautifulSoup(page.content, 'html.parser')
        wens = soup.find_all('div', class_='flex-1 flex items-center justify-between px-5 py-3 rounded-tr-md w-full pr-5 rounded-t1-md px-5')

        # for wen in wens:
        #     jobss = Jobs()
        #     jobss.link = wen.find('a',class_='relative mb-3 text-lg font-medium break-words focus:outline-none metrics-apply-now text-link-500 text-loading-animate')['href']
        #     jobss.title = wen.find('p').text.strip()
        #     jobss.Job_function = wen.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').get_text(strip=True)  
        #     jobss.save()

        #     functio = JobFunctions()
        #     functio.function = jobss
        #     functio.jobFunction = wen.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block').get_text(strip=True)       
        #     functio.save()
        
            
        wens = soup.find_all('div', class_='flex-1 flex items-center justify-between px-5 py-3 rounded-tr-md w-full pr-5 rounded-t1-md px-5')
    
        for wen in wens:
            job_link = wen.find('a',class_='relative mb-3 text-lg font-medium break-words focus:outline-none metrics-apply-now text-link-500 text-loading-animate')['href']
            job_title = wen.find('p').text.strip()
             # Find the paragraph element by class name
            job_response = requests.get(job_link)
            job_soup = BeautifulSoup(job_response.content, 'html.parser')
            paragraph = job_soup.find('p', class_='text-sm text-gray-500 text-loading-animate inline-block')
            paragraph_text = paragraph.get_text()
            colon_index = paragraph_text.find(':')
            extracted_text = paragraph_text[colon_index + 1:].strip()
            Job_function_name=extracted_text
            
            jtype=job_soup.find('div',class_='mt-3')
            job_type_name = jtype.find('span',class_='text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block').find('a').get_text(strip=True)
            new_job_type = Type(time=Job_function_name)
            new_job_type.save()
            location_name=jtype.find('a',class_='text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block').get_text(strip=True)
            jtyp=job_soup.find('div',class_='w-full text-gray-500')
            Industry_name=jtyp.find_all('div')[1].find('a',class_='text-sm font-normal px-3 rounded bg-brand-secondary-50 mr-2 mb-3 inline-block').get_text(strip=True)
            
            location, _ = Location.objects.get_or_create(location=location_name)
            job_type, _ = Type.objects.get_or_create(time=job_type_name)
            job_function, _ = JobFunctions.objects.get_or_create(jobFunction=Job_function_name)
            industry, _ = Industries.objects.get_or_create(industry=Industry_name)
            
            new_job = Jobs(
            title=job_title,
            link=job_link,
            location=location,
            job_type=job_type,
            job_function=job_function,
            industries=industry)
            
            new_job.save()
                  
            # job_response = requests.get(job_link)
            # job_soup = BeautifulSoup(job_response.content, 'html.parser')
            summary=job_soup.find('div',class_='py-5 px-4 border-b border-gray-300 md:p-5')
            if summary.find('h3').get_text():
                det=JobDetail()
                det.job=new_job
                det.details=summary.find('h3').get_text()
                det.save()
            if summary.find('p').get_text():
                det=JobDetail()
                det.job=new_job
                det.details=summary.find('p').get_text()
                det.save()
            qualification = summary.find('ul')
            if qualification:
                # qualifications = []
                qualifications_elements = qualification.find_all('li')
                for qual_element in qualifications_elements:
                    det = JobDetail()
                    det.job = new_job
                    det.details=qual_element.get_text()
                    det.save()
            descrip = job_soup.find('div', class_='text-sm text-gray-500')
            paragraphs=descrip.find_all('p')
            for paragraph in paragraphs:
                bold_tag =paragraph.find_all('b')
                content=paragraph.get_text()     
                if bold_tag:
                    job_detail = JobDetail(job=new_job, details=content,bold=True)
                else:
                    job_detail = JobDetail(job=new_job, details=content,bold=False)                
                job_detail.save()
                
                next_sibling = paragraph.find_next_sibling()
                    
                if next_sibling and next_sibling.name == 'ul':
                    ul_tag = paragraph.find_next_sibling('ul')
                    if ul_tag:
                        cont1 = ''
                        for li in ul_tag.find_all('li'):
                            cont1 = li.text.strip()
                            # content+=cont1
                            # content += ' :   ' + cont1
                            content = cont1
                            job_detail1 = JobDetail(job=new_job, details=content,)
                            job_detail1.save()
                            
class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_queryset(self):
        fields = ['id', 'title','link']
        queryset = Jobs.objects.values(*fields)

        return queryset

class JobsViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    def list(self, request):
        data = request.query_params.dict()
        # data = request.data
        queryset = Jobs.objects.filter(**data)
        serialized_data = JobSerializer(queryset, many=True).data
        return Response({'data': serialized_data})

class JobsLocationViewSet(viewsets.ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__location=location)
        return queryset
    
class JobDetailViewSet(viewsets.ModelViewSet):
    queryset=JobDetail.objects.all()
    serializer_class=JobDetailSerializer
class JobLocationViewSet(viewsets.ModelViewSet):
    queryset=Location.objects.all()
    serializer_class=JobLocationSerializer
class JobFunctionsViewSet(viewsets.ModelViewSet):
    queryset=JobFunctions.objects.all()
    serializer_class=JobFunctionSerializer
class JobTimeViewSet(viewsets.ModelViewSet):
    queryset=Type.objects.all()
    serializer_class=JobTimeSerializer