<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" version = "1.0" >
<xsl:output omit-xml-declaration="no" method="html" indent="yes" encoding="UTF-8" />
<xsl:template match = "/icestats" >
<xsl:text disable-output-escaping="yes">&lt;!DOCTYPE html></xsl:text>

<html>
<head>
	<meta charset="UTF-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" user-scalable="no"/>
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>

	<title>ICESNAP RadioMopidy</title>
	<link rel="stylesheet" type="text/css" href="boilerplate.min.css" />
	<link rel="stylesheet" type="text/css" href="style.css" />
	<script src="modernizr.min.js"></script>
	<link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,200,700&amp;subset=latin,latin-ext&#8217;" rel="stylesheet" type="text/css" />
</head>

<body>
<div id="container">
	<header role="banner">
		<span>
			<h1 id="site-title">ICESNAP RadioMopidy</h1>
		</span>
	</header>

<xsl:for-each select="source">
<xsl:choose>
<xsl:when test="listeners">

	<section class="mount-point">
		<div class="mount-point-data">
			<xsl:if test="server_name"><span class="server-name mount-header">Playing</span></xsl:if>
		</div>

		<div class="mount-point-data">
			<xsl:if test="title">
				<p class="current-song" title="Current Song"><xsl:if test="artist"><xsl:value-of select="artist" /> - </xsl:if><xsl:value-of select="title" /></p>
			</xsl:if>
		</div>
		<div>
			<figure>
				<audio controls="" src="{@mount}"></audio>
			</figure>
		</div>
	</section>

</xsl:when>
<xsl:otherwise>
<section class="mount-point">
	<header class="mount-point-header clearfix">
		<h1><xsl:value-of select="@mount" /> - Not Connected</h1>
	</header>
</section>
</xsl:otherwise>
</xsl:choose>
</xsl:for-each>

</div>

</body>
</html>
</xsl:template>
</xsl:stylesheet>