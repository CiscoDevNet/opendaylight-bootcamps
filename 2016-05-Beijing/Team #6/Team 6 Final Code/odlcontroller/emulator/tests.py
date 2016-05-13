from django.test import TestCase

# Create your tests here.
Nodes.objects.all().filter(name='iosxrv-1').update(xpos="450", ypos="50")
Nodes.objects.all().filter(name='iosxrv-2').update(xpos="700", ypos="175")
Nodes.objects.all().filter(name='iosxrv-3').update(xpos="500", ypos="175")
Nodes.objects.all().filter(name='iosxrv-4').update(xpos="150", ypos="300")
Nodes.objects.all().filter(name='iosxrv-5').update(xpos="850", ypos="100")
Nodes.objects.all().filter(name='iosxrv-6').update(xpos="300", ypos="150")
Nodes.objects.all().filter(name='iosxrv-7').update(xpos="450", ypos="50")
Nodes.objects.all().filter(name='iosxrv-8').update(xpos="300", ypos="175")