from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from .forms import CSVFileForm
from .models import CSVFile
from django.contrib.auth.decorators import login_required
import pandas as pd
import xlsxwriter
import os
from django.conf import settings

def uploadDataInDB(file_obj):
    file_path = os.path.join("media/" , file_obj.csv_path.name)
    data = pd.read_csv(file_path)
    data.isna().sum()
    data.drop_duplicates()
    # coloums = list(data.columns)
    for i, row in data.iterrows():
        file_obj.all_apps.append(row)
    file_obj.save()

@login_required
def upload_csv(request):
    user = request.user
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = user
            file_obj = form.save()
            uploadDataInDB(file_obj)
            return redirect('/')
    else:
        form = CSVFileForm()
    prev_uploads = CSVFile.objects.filter(user=user).all()
    return render(request, 'index.html', {
        'form': form, 'prev_uploads': prev_uploads
    })

def setDataInWorksheet(data, worksheet, row, header_format1, header_format2):
    # Setting Coloumns
    worksheet.write(row, 0, "App", header_format1)
    worksheet.write(row, 1, "Category", header_format1)
    worksheet.write(row, 2, "Rating", header_format1)
    worksheet.write(row, 3, "Reviews", header_format1)
    worksheet.write(row, 4, "Size", header_format1)
    worksheet.write(row, 5, "Installs", header_format1)
    worksheet.write(row, 6, "Type", header_format1)
    worksheet.write(row, 7, "Price", header_format1)
    worksheet.write(row, 8, "Content Rating", header_format1)
    worksheet.write(row, 9, "Genres", header_format1)
    worksheet.write(row, 10, "Last Updated", header_format1)
    worksheet.write(row, 11, "Current Ver", header_format1)
    worksheet.write(row, 12, "Android Ver", header_format1)

    row+=1

    for row_data in data:
        try:
            worksheet.write(row, 0, row_data[0], header_format2)
            worksheet.write(row, 1, row_data[1], header_format2)
            worksheet.write(row, 2, row_data[2], header_format2)
            worksheet.write(row, 3, row_data[3], header_format2)
            worksheet.write(row, 4, row_data[4], header_format2)
            worksheet.write(row, 5, row_data[5], header_format2)
            worksheet.write(row, 6, row_data[6], header_format2)
            worksheet.write(row, 7, row_data[7], header_format2)
            worksheet.write(row, 8, row_data[8], header_format2)
            worksheet.write(row, 9, row_data[9], header_format2)
            worksheet.write(row, 10, row_data[10], header_format2)
            worksheet.write(row, 11, row_data[11], header_format2)
            worksheet.write(row, 12, row_data[12], header_format2)
            row+=1
        except:
            pass
    row+=2
    return worksheet, row

def createWorksheetByType(file):
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', 'filter_by_type.xlsx'))
    workbook = xlsxwriter.Workbook(wbpath)
    worksheet = workbook.add_worksheet('Filtered by Type')
    merge_format1 = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'bg_color': 'black',
        'font_size': 20
    })
    header_format1 = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'black',
        'bg_color': 'gray'
    })
    header_format2 = workbook.add_format({
        'bold': 0,
        'align': 'left',
        'valign': 'vcenter',
        'font_color': 'black',
        'bg_color': 'white'
    })
    worksheet.merge_range('A1:M1', 'Paid Apps', merge_format1)
    row=2
    worksheet, row = setDataInWorksheet(file.paid_apps, worksheet, row, header_format1, header_format2)
    
    worksheet.merge_range(f'A{row}:M{row}', 'Free Apps', merge_format1)
    worksheet, row = setDataInWorksheet(file.free_apps, worksheet, row, header_format1, header_format2)
   
    workbook.close()

    file_path = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', 'filter_by_type.xlsx'))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return Http404

@login_required
def filter_by_type(request, fileid):
    user = request.user
    if CSVFile.objects.filter(user=user, id=fileid).exists():
        file = CSVFile.objects.get(user=user, id=fileid)
        if(request.user == file.user):
            # Read Data
            data = pd.read_csv(file.csv_path.path)

            for i, row in data.iterrows():
                # a = row in file.free_apps
                # b = row in file.paid_apps
                if row["Type"] == "Free":
                    # if a is False:
                    file.free_apps.append(row)
                elif row["Type"] == "Paid":
                    # if b is False:
                    file.paid_apps.append(row)
            file.save()
            
            response = createWorksheetByType(file)
            return response
        else:
            return HttpResponse("You are not the owner of this file")
    else:
        return Http404

def createWorksheetByContentRating(file):
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', 'filter_by_contentrating.xlsx'))
    workbook = xlsxwriter.Workbook(wbpath)
    worksheet = workbook.add_worksheet('Filtered by Content Rating')
    merge_format1 = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'bg_color': 'black',
        'font_size': 20
    })
    header_format1 = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'black',
        'bg_color': 'gray'
    })
    header_format2 = workbook.add_format({
        'bold': 0,
        'align': 'left',
        'valign': 'vcenter',
        'font_color': 'black',
        'bg_color': 'white'
    })
    row=1

    worksheet.merge_range(f'A{row}:M{row}', 'Everyone', merge_format1)
    row+=1
    worksheet, row = setDataInWorksheet(file.everyone, worksheet, row, header_format1, header_format2)
    
    worksheet.merge_range(f'A{row}:M{row}', 'Teen', merge_format1)
    row+=1
    worksheet, row = setDataInWorksheet(file.teen, worksheet, row, header_format1, header_format2)

    worksheet.merge_range(f'A{row}:M{row}', 'Mature 17+', merge_format1)
    row+=1
    worksheet, row = setDataInWorksheet(file.mature_17_plus, worksheet, row, header_format1, header_format2)

    worksheet.merge_range(f'A{row}:M{row}', 'Everyone 10+', merge_format1)
    row+=1
    worksheet, row = setDataInWorksheet(file.everyone_10_plus, worksheet, row, header_format1, header_format2)

    worksheet.merge_range(f'A{row}:M{row}', 'Adults 18+', merge_format1)
    row+=1
    worksheet, row = setDataInWorksheet(file.adults_18_plus, worksheet, row, header_format1, header_format2)

    worksheet.merge_range(f'A{row}:M{row}', 'Unrated', merge_format1)
    row+=1
    worksheet, row = setDataInWorksheet(file.unrated, worksheet, row, header_format1, header_format2)
    
    workbook.close()

    file_path = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', 'filter_by_contentrating.xlsx'))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return Http404

@login_required
def filter_by_contentRating(request, fileid):
    user = request.user
    if CSVFile.objects.filter(user=user, id=fileid).exists():
        file = CSVFile.objects.get(user=user, id=fileid)
        if(request.user == file.user):
            # Read Data
            data = pd.read_csv(file.csv_path.path)

            for i, row in data.iterrows():
                if row["Content Rating"] == "Everyone":
                    file.everyone.append(row)
                elif row["Content Rating"] == "Teen":
                    file.teen.append(row)
                elif row["Content Rating"] == "Mature 17+":
                    file.mature_17_plus.append(row)
                elif row["Content Rating"] == "Everyone 10+":
                    file.everyone_10_plus.append(row)
                elif row["Content Rating"] == "Adults only 18+":
                    file.adults_18_plus.append(row)
                elif row["Content Rating"] == "Unrated":
                    file.unrated.append(row)
            file.save()
            
            response = createWorksheetByContentRating(file)
            return response
        else:
            return HttpResponse("You are not the owner of this file")
    else:
        return Http404

def createWorksheetByRoundedRating(file):
    wbpath = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', 'rounded_rating.xlsx'))
    workbook = xlsxwriter.Workbook(wbpath)
    worksheet = workbook.add_worksheet('Rounded Rating')
    merge_format1 = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'bg_color': 'black',
        'font_size': 20
    })
    header_format1 = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'black',
        'bg_color': 'gray'
    })
    header_format2 = workbook.add_format({
        'bold': 0,
        'align': 'left',
        'valign': 'vcenter',
        'font_color': 'black',
        'bg_color': 'white'
    })
    row=1
    worksheet.merge_range(f'A{row}:N{row}', 'All Data with Rounded Rating', merge_format1)
    row+=1

    # Setting Coloumns
    worksheet.write(row, 0, "App", header_format1)
    worksheet.write(row, 1, "Category", header_format1)
    worksheet.write(row, 2, "Rating", header_format1)
    worksheet.write(row, 3, "Reviews", header_format1)
    worksheet.write(row, 4, "Size", header_format1)
    worksheet.write(row, 5, "Installs", header_format1)
    worksheet.write(row, 6, "Type", header_format1)
    worksheet.write(row, 7, "Price", header_format1)
    worksheet.write(row, 8, "Content Rating", header_format1)
    worksheet.write(row, 9, "Genres", header_format1)
    worksheet.write(row, 10, "Last Updated", header_format1)
    worksheet.write(row, 11, "Current Ver", header_format1)
    worksheet.write(row, 12, "Android Ver", header_format1)
    worksheet.write(row, 13, "Rounded Rating", header_format1)

    row+=1

    for row_data in file.all_apps:
        try:
            worksheet.write(row, 0, row_data[0], header_format2)
            worksheet.write(row, 1, row_data[1], header_format2)
            worksheet.write(row, 2, row_data[2], header_format2)
            worksheet.write(row, 3, row_data[3], header_format2)
            worksheet.write(row, 4, row_data[4], header_format2)
            worksheet.write(row, 5, row_data[5], header_format2)
            worksheet.write(row, 6, row_data[6], header_format2)
            worksheet.write(row, 7, row_data[7], header_format2)
            worksheet.write(row, 8, row_data[8], header_format2)
            worksheet.write(row, 9, row_data[9], header_format2)
            worksheet.write(row, 10, row_data[10], header_format2)
            worksheet.write(row, 11, row_data[11], header_format2)
            worksheet.write(row, 12, row_data[12], header_format2)
            worksheet.write(row, 13, int(row_data[2]), header_format2)
            row+=1
        except:
            pass

    workbook.close()
    file_path = os.path.join(settings.MEDIA_ROOT, os.path.join('workbooks', 'rounded_rating.xlsx'))
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    return Http404

@login_required
def rounded_rating(request, fileid):
    user = request.user
    if CSVFile.objects.filter(user=user, id=fileid).exists():
        file = CSVFile.objects.get(user=user, id=fileid)
        if(request.user == file.user):          
            response = createWorksheetByRoundedRating(file)
            return response
        else:
            return HttpResponse("You are not the owner of this file")
    else:
        return Http404