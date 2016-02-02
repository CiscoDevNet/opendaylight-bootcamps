from django.db import models

# Create your models here.


class BackendServer(models.Model):
    ipaddr = models.CharField(max_length=60)
    macaddr = models.CharField(max_length=60)
    ofport = models.CharField(max_length=60)


class VirtualService(models.Model):
    virtual_ip = models.CharField(max_length=60)
    virtual_port = models.CharField(max_length=60)
    l4_protocol = models.CharField(max_length=60)
    # store multi backend servers id with the format
    # id1,id2,id3
    bs_pool = models.CharField(max_length=60)


class ClientInfo(models.Model):
    mac_addr = models.CharField(max_length=60)
    ip_addr = models.CharField(max_length=60)
