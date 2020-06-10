<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" version = "1.0" >
	<xsl:output omit-xml-declaration="yes" method="text" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" indent="no" encoding="UTF-8" media-type="application/json" />
	<xsl:strip-space elements="*"/>

	<xsl:template match = "/icestats" >
	{
		"server": {
			<xsl:for-each select="*">
				<xsl:if test = "name()!='source'">
					"<xsl:value-of select="name()" />": "<xsl:value-of select="." />",
				</xsl:if>
			</xsl:for-each>

			"streams": {
				<xsl:for-each select="source">
					"<xsl:value-of select="@mount" />": {
						"name" : "<xsl:value-of select="server_name"/>",
						"listeners" : "<xsl:value-of select="listeners" />",
						"peak_listeners" : "<xsl:value-of select="listener_peak" />",
						"description" : "<xsl:value-of select="server_description" />",
						"title" : "<xsl:value-of select="title" />",
						"genre" : "<xsl:value-of select="genre" />",
						"url" : "<xsl:value-of select="server_url" />"
					}<xsl:if test="position() != last()"><xsl:text>,</xsl:text></xsl:if>
				</xsl:for-each>
			}
		}
	}
	</xsl:template>
</xsl:stylesheet>

