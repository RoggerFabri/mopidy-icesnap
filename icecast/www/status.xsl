<xsl:stylesheet xmlns:xsl = "https://www.w3.org/1999/XSL/Transform" version = "1.0" >
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
	<script src="jquery.min.js"></script>
	<script src="playingnow.js"></script>
	<link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,200,700&amp;subset=latin,latin-ext" rel="stylesheet" type="text/css" />
	<link href="https://fonts.googleapis.com/css?family=Fira+Sans:300,300i,400,500,600,700,800&amp;subset=latin,latin-ext" rel="stylesheet" type="text/css" />
</head>

<body>
<div id="container">
	<header role="banner">
		<span>
			<h1 id="site-title">ICESNAP RadioMopidy</h1>
		</span>
	</header>

<xsl:for-each select="source">
	<section class="mount-point">
		<div class="mount-point-data">
			<div id="album-cover" style="display:none;" class="album-cover"></div>
			<p id="playing-now" class="current-song" title="Playing Now">...</p>
		</div>
		<div>
			<figure>
				<audio autoplay="true" controls="" src="{@mount}"></audio>
			</figure>
		</div>
	</section>
</xsl:for-each>

</div>

</body>
</html>
</xsl:template>
</xsl:stylesheet>