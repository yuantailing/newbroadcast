from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import *

from models import *

def test_user(req):
	t = get_template("ajaxtest/getUser.html");
	c = RequestContext(req);
	return HttpResponse(t.render(c));