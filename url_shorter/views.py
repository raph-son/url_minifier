"""
App view
"""
import requests

from requests.exceptions import MissingSchema, ConnectionError
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from url_shorter.models import Url
from url_shorter.serializers import UrlSerializer

def remainder_list(value):
    """
    value: int
    work through value until 0
    storing remaider each time
    return remainder
    """
    x = value
    quotient = 0
    remainder = []
    while (x > 0):
        quotient = int(x/62)
        temp =  int(x % 62)
        remainder.append(temp)
        x = int(quotient)

    return remainder

def reverse_order(arr):
    """
    arr: list
    return values in array in reverse order
    """
    value_reverse = []
    count = len(arr)
    while ( count > 0 ):
        value_reverse.append(arr[count - 1])
        count -= 1

    return value_reverse


def base62_hash(id):
    """
    id: int
    convert id to base62 which will
    be use as minified URL
    """

    # Base 62 char to form minified url
    base62_char = ["a", "b", "c", "d", "e", "f", "g", "h", "i",
            "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
            "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E",
            "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
            "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", 0, 1,
            2, 3, 4, 5, 6, 7, 8, 9
    ]

    remainder = remainder_list(id)
    # Store remainder variable in reverse order
    value_reverse = reverse_order(remainder)

    hash = ""
    # Map each index from value_reverse to base62_char var
    for key, value in enumerate(value_reverse):
        hash += base62_char[value]

    return hash

def index(request):
    """
    Index page
    """
    return render(request, "url_shorter/index.html")

@api_view(["GET", "POST"])
def submit_url(request):
    """
    View for processing submitted url
    """
    if request.method == "POST":

        domain = request.META['HTTP_HOST']
        
        input_url = f"{request.data.get('url')}"
	# See if link is already stored
        try:
            url = Url.objects.get(url=input_url)
        except Url.DoesNotExist:
            # Proceed to validate link	
            url = input_url
            try:
                r = requests.get(url)
            except MissingSchema:
                # user url has no schema so add "http://"
                url = f"http://{url}"
                try:
                    r = requests.get(url)
                except ConnectionError:
                    # An exception that will typically be thrown if link isn't valid
                    # Can still be thrown if network error and not server but unlikly
                    # here
                    # An invalid domain/link
                        
                    return Response({
                        "success": "Check Your URL and retry"
                    })

            # Try checking one more time if link already exsited in db
            # This is possible if link already existed but new link
            # came in with different format like "http" vs "https"
            # or with/without "www" prefix
            try:
                url = Url.objects.get(url=r.url)
            except Url.DoesNotExist:
                # Finally add to db
                # First add URL to db and get back id for
                # generting minified
                data = {
                    "url": r.url
                }
                serializer = UrlSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                # Get back id of the newly stored url
                # then generate minified url
                url = Url.objects.get(url=r.url)    
                serializer = UrlSerializer(url)
                id = serializer.data.get("id")
                hash_id = base62_hash(id)

                # Update data with new hash
                hash_update = {
                    "url": r.url,
                    "hash": hash_id
                }
                # Add hash
                update_serializer = UrlSerializer(url, data=hash_update)
                if update_serializer.is_valid():
                    update_serializer.save()
                # query newly created minified to return minified url 
                url = Url.objects.get(url=r.url)
                serializer = UrlSerializer(url)
                return Response({
                    "success": f"{domain}/{serializer.data['hash']}"
                })
            # Url already existed return it hash
            # This time, it already existed because of 
            # db re-query -  after requesting the url
            # from host
            serializer = UrlSerializer(url)
        
            return Response({
                "success": f"{domain}/{serializer.data['hash']}"
            })
        # Url already existed, just go ahead and return it hash
        serializer = UrlSerializer(url)
        return Response({
            "success": f"{domain}/{serializer.data.hash}"
        })
    else:
        return Response({
            "status": "success"
        })

def redirect_out(request, hash):
    """
    View to redirect minified link to destination
    """
    try:
        url = Url.objects.get(hash=hash)
    except Url.DoesNotExist:
        # Invalid hash link, just redirect
        # to home page
        return redirect("/")
    serializer = UrlSerializer(url)
    return redirect(serializer.data["url"])
