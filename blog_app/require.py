from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime

def render_to_pdf(template, content_dic={}):
    t = get_template(template)
    send_data = t.render(content_dic)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(send_data.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return None

# from io import StringIO
# from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# from django.http import HttpResponse
# from cgi import escape
# import datetime

# def render_to_pdf(template_src, context_dict={}):
#     print(type(context_dict))
#     template = get_template(template_src)
#     # context = Context(context_dict)
#     html = template.render(context_dict)
#     result = StringIO()

#     # pdf name generate with date
#     date = datetime.date.today()
#     tmpName = template_src.split('.')[0]
#     pdfName = tmpName+'-'+str(date)

#     pdf = pisa.pisaDocument(StringIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         response = HttpResponse(result.getvalue(), content_type='application/pdf')
#         response['Content-Disposition']='attachment; filename='+pdfName+'.pdf'
#         return response
#     return None
#     # return HttpResponse("We had some errors<pre>%s</pre>" %escape(html))