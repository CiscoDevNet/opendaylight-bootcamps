# Source code from http://www.leancrew.com/all-this/2012/04/one-more-text-tables-bundle-improvement/
# Published by Dr. Drang, April 14, 2012 
#
# Minor modifications made by Ken Jarrad, 2014-11-14.

from lxml import etree

_acl_xsl_text = '''\
<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:acl="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-acl-cfg">

<xsl:output method="html" encoding="UTF-8" omit-xml-declaration="yes"/>

<xsl:template match="/">
  <xsl:namespace/>
  <table border="1" >
    <thead>
        <tr style="background-color:lightgray;">
          <th style="text-align:left;" rowspan="2">list</th>
          <th style="text-align:right;" rowspan="2">entry</th>
          <th style="text-align:center;" rowspan="2">grant</th>
          <th style="text-align:center;" rowspan="2">protocol</th>
          <th style="text-align:center;" colspan="4">source</th>
          <th style="text-align:center;" colspan="4">destination</th>
        </tr>
        <tr style="background-color:lightgray;">
          <th style="text-align:center;">address</th>
          <th style="text-align:right;">oper.</th>
          <th style="text-align:right;">port 1</th>
          <th style="text-align:right;">port 2</th>
          <th style="text-align:center;">address</th>
          <th style="text-align:right;">oper.</th>
          <th style="text-align:right;">port 1</th>
          <th style="text-align:right;">port 2</th>
        </tr>
    </thead>
    <tbody>
        <style>
          tr:nth-of-type(even) {background-color:#eee;}
        </style>
    <xsl:for-each select=".//acl:access">
        <xsl:apply-templates select="./acl:access-list-entries/acl:access-list-entry">
            <xsl:sort select="acl:sequence-number"/>
        </xsl:apply-templates>
    </xsl:for-each>
    </tbody>
  </table>
</xsl:template>

<xsl:template match="acl:access-list-entry">
    <tr>
    <xsl:if test="(position() = 1)">
        <th style="text-align:left; background-color:white;" rowspan="{count(../acl:access-list-entry)}"><xsl:value-of select="../../acl:access-list-name"/></th>
    </xsl:if>
          <td style="text-align:right;"><xsl:value-of select="acl:sequence-number"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:grant"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:protocol"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:source-network/acl:source-address"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:source-operator"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:first-source-port"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:second-source-port"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:destination-network/acl:destination-address"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:destination-operator"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:first-destination-port"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:second-destination-port"/></td>
    </tr>
</xsl:template>

<xsl:template match="acl:access-list-entry[position() > 11111]">
          <td style="text-align:right;"><xsl:value-of select="acl:sequence-number"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:grant"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:protocol"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:source-network/acl:source-address"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:source-operator"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:first-source-port"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:second-source-port"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:destination-network/acl:destination-address"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:destination-operator"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:first-destination-port"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:second-destination-port"/></td>
</xsl:template>

</xsl:stylesheet>
'''

backup_acl_xsl_text = '''\
<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:acl="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-acl-cfg">
<xsl:template match="/">
  <xsl:namespace/>
  <table border="1">
    <thead bgcolor="lightgray">
        <tr>
          <th style="text-align:left;" rowspan="2">list</th>
          <th style="text-align:right;" rowspan="2">entry</th>
          <th style="text-align:center;" rowspan="2">grant</th>
          <th style="text-align:center;" rowspan="2">protocol</th>
          <th style="text-align:center;" colspan="4">source</th>
          <th style="text-align:center;" colspan="4">destination</th>
        </tr>
        <tr>
          <th style="text-align:center;">address</th>
          <th style="text-align:right;">oper.</th>
          <th style="text-align:right;">port 1</th>
          <th style="text-align:right;">port 2</th>
          <th style="text-align:center;">address</th>
          <th style="text-align:right;">oper.</th>
          <th style="text-align:right;">port 1</th>
          <th style="text-align:right;">port 2</th>
        </tr>
    </thead>
    <tbody>
    <xsl:for-each select=".//acl:access-list-entry">
        <xsl:sort select="../../acl:access-list-name"/>
        <xsl:sort select="acl:sequence-number"/>
        <tr>
          <td style="text-align:left;"><xsl:value-of select="../../acl:access-list-name"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:sequence-number"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:grant"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:protocol"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:source-network/acl:source-address"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:source-operator"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:first-source-port"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:source-port/acl:second-source-port"/></td>
          <td style="text-align:center;"><xsl:value-of select="acl:destination-network/acl:destination-address"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:destination-operator"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:first-destination-port"/></td>
          <td style="text-align:right;"><xsl:value-of select="acl:destination-port/acl:second-destination-port"/></td>
        </tr>
    </xsl:for-each>
    </tbody>
  </table>
</xsl:template>

</xsl:stylesheet>
'''

# ACL XSL parsed and compiled.
_acl_xslt = etree.XSLT(etree.fromstring(_acl_xsl_text))
 
_namespaces = {'acl':'http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-acl-cfg',
      'nni':'urn:opendaylight:netconf-node-inventory'}

def acl_table(acl_xml):
    return unicode(_acl_xslt(acl_xml))
