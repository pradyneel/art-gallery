from django.shortcuts import render, redirect
from django.http import HttpResponse 
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import requests
import json
import time
import uuid


# Azure connection
# connect_str = os.environ['AZURE_STORAGE_CONNECTION_STRING'] # retrieve the connection string from the environmental variable
connect_str = "DefaultEndpointsProtocol=https;AccountName=artgallery;AccountKey=/pDidMtFw0i2pLRGE2WYBWamvP/cQbHD5uB1pIsl2SU3C1Gz3BQqM29bpeBY9a5i8wO8mCZtP6eU+ASt5nNH3A==;EndpointSuffix=core.windows.net"
container_name = "artgallery" # container name in which images will be stored in the storage account


#Generate QRCode
def GenerateQRcode(markdown_card_id, name):
    url = "https://api.beaconstac.com/api/2.0/qrcodes/"
 
    payload = {
    "name": name,
    "organization": 26724,
    "qr_type": 2,
    "campaign": {
        "content_type": 2,
        "markdown_card": markdown_card_id
    },
    "location_enabled": False,
    "attributes":{
        "color": "#f10e0e",
        "colorDark":"#f10e0e",
        "margin":80,
        "isVCard": False,
        "frameText": "ART GALLERY",
        "logoImage": "https://artgallery.blob.core.windows.net/artgallery/146-removebg-preview.png",
        "logoScale":0.1992,
        "frameColor": "#DB4D4D",
        "frameStyle":"box-bottom",
        "logoMargin":10,
        "dataPattern":"circle",
        "eyeBallShape":"circle",
        "gradientType": "none",
        "eyeFrameColor": "#000000",
        "eyeFrameShape": "circle"
    }
    }

    headers = {
    'Authorization': 'Token bd2149fd3ad6748f72ebae26c7ceed035af67084',
    'Content-Type': 'application/json'
    }

    payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


# Create your views here.

# Dashboard View
def dashboard(request):
    return render(request, "home/dashboard.html")


# Create Landing Page
def pageGenerator(request):
    if request.method == "POST":  
        title = request.POST.get('title')
        image = request.FILES['image']
        artist = request.POST.get('artist')
        location = request.POST.get('location')
        creation = request.POST.get('created')
        dimension = request.POST.get('dimension')
        medium = request.POST.get('medium')
        summary = request.POST.get('summary')
        ref_url = request.POST.get('url')

        try:
            blob = BlobClient.from_connection_string(conn_str= connect_str, container_name= container_name, blob_name= image.name + str(uuid.uuid1()))
            blob.upload_blob(image.read()) # upload the file to the container using the filename as the blob name
        except Exception as e:
            print(e)

        url = "https://api.beaconstac.com/api/2.0/markdowncards/"
        payload = {
            "organization":26724,
            "title": title,
            "markdown_body":"",
            "html_body":"<!DOCTYPE html> <html lang=\"en\"><head><meta charset=\"UTF-8\"><meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"> <title>Art Gallery</title></head><body><div class=\"header\"><h1>ART Gallery</h1></div><div class=\"info\"><figure><img src=\"{url}\" width=\"300\" height=\"400\"><figcaption>{title}</figcaption></figure><br><table><tbody><tr><td><b>Artist</b></td><td><b>:</b></td><td>{artist}</td></tr><tr><td><b>Location</b></td><td><b>:</b></td><td>{location}</td></tr><tr><td><b>Created</b></td><td><b>:</b></td><td>{creation}</td></tr><tr><td><b>Dimension</b></td><td><b>:</b></td><td>{dimension}</td></tr><tr><td><b>Medium</b></td><td><b>:</b></td><td>{medium}</td></tr></tbody></table><br><p>{summary}</p><br><a href=\"{ref_url}\" style=\"color:cornflowerblue\"><i>READ MORE</i></a></div></body></html>".format(url = blob.url, title = title, artist = artist, location = location, creation = creation, dimension = dimension, medium = medium, summary = summary, ref_url = ref_url),
            "css_body":"*{margin: 0;}body{align-items: center;text-align: center;font-family: sans-serif;}.header{ width: 100%;background-color: #FCF8F8;padding-top: 21px;padding-bottom: 21px;}.info{margin-top: 25px;}table{margin-left: auto;margin-right: auto;padding: 5px;}th, td{padding: 10px;}"
        }

        headers = {
            "Authorization" : 'Token bd2149fd3ad6748f72ebae26c7ceed035af67084'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        dictResponse = json.loads(response.text)
        markdown_card_id = dictResponse["id"]

        # Once Markdown is created "Generating QR code for the Markdown Page"
        GenerateQRcode(markdown_card_id, title)
        return redirect("/qrcodes/")

    else:
        return render(request, "home/pageGenerator.html")


# Get QRCode image URL
def getQRcode_url(images_id):
    payload={}
    headers = {
    'Authorization': 'Token bd2149fd3ad6748f72ebae26c7ceed035af67084'
    }

    images_info = []

    for image_id in images_id:
        url = "https://api.beaconstac.com/api/2.0/qrcodes/{image_id}/download/?size=1024&error_correction_level=5&canvas_type=png".format(image_id = image_id)
        response = requests.request("GET", url, headers=headers, data=payload)
        dictResponse = json.loads(response.text)

        image_url = dictResponse['urls']['png']
        image_name = dictResponse['name']

        image_info = {
            "image_id" : image_id,
            "image_url" :  image_url,
            "image_name" : image_name
        }

        images_info.append(image_info)
    return images_info


# Get all QR code ids
def getAllQRcodeId():
    url = "https://api.beaconstac.com/api/2.0/qrcodes/"

    payload={}
    headers = {
    'Authorization': 'Token bd2149fd3ad6748f72ebae26c7ceed035af67084'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    dictResponse = json.loads(response.text)

    ids = []
    urls = []
    markdown_ids = []

    for dict in dictResponse['results']:
        #  To get ID of only Active QR codes
        if(dict['state'] == 'A'):
            ids.append(dict['id'])
            urls.append(dict['url'])
            markdown_ids.append(dict["campaign"]["markdown_card"])
            # print(dict['id'],dict['state'])
    
    dict = {
        "image_id": ids,
        "urls": urls,
        "markdown_ids": markdown_ids
    }
    return dict


# View all generated QR codes
def QRcodes(request):
    image_dict = getAllQRcodeId()
    images_info = getQRcode_url(image_dict["image_id"])

    for i, image_info in enumerate(images_info):
        image_info["url"] = image_dict["urls"][i]
        image_info["markdown_id"] = image_dict["markdown_ids"][i]
        
    context = {
        "QRcodes": images_info
    }
    
    return render(request, "home/QRcodes.html", context=context)


# View all Generated Landing Pages
def landPage(request):
    image_dict = getAllQRcodeId()

    context = {
        "markdowns": image_dict["urls"]
    }
    return render(request, "home/landingPages.html", context = context)


# # Edit a QR codes
# def update


# # status Success
# def sucess(request):
#     time.sleep(5)
#     return redirect('/')