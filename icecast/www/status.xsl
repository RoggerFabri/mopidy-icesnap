<xsl:stylesheet xmlns:xsl = "http://www.w3.org/1999/XSL/Transform" version = "1.0" >
	<xsl:output omit-xml-declaration="no" method="html" indent="yes" encoding="UTF-8" />
	<xsl:template match = "/icestats" >
		<xsl:text disable-output-escaping="yes">&lt;!DOCTYPE html></xsl:text>

		<html>
			<head>
				<meta charset="UTF-8" />
				<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" user-scalable="no"/>
				<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>

				<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>
				<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png"/>
				<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png"/>
				<link rel="manifest" href="/site.webmanifest"/>
				<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5"/>
				<meta name="msapplication-TileColor" content="#da532c"/>
				<meta name="theme-color" content="#ffffff"/>

				<title>ICESNAP Radio</title>
				<link rel="stylesheet" type="text/css" href="app.css"/>
				<script src="jquery.min.js"></script>
				<script src="playingnow.js"></script>
				<script src="base.js"></script>
			</head>

			<body>
				<div id="container" class="modal modal--kiosk-mode">
					<div id="sleeping" class="sleeping" style="display:none">
						<img src="./sleeping.gif"></img>
					</div>
					<xsl:for-each select="source">
						<div class="content">
							<div class="thumbnail thumbnail--loaded background">
								<div id="album-cover-background" class="thumbnail__image">
								</div>
							</div>

							<div class="player player--without-lyrics">
								<div class="track">
									<div class="track__artwork">
										<div class="thumbnail thumbnail--loaded">
											<i class="icon icon--material thumbnail__placeholder"></i>
											<img id="album-cover" class="thumbnail__image thumbnail__image--use-image-tag" src="album-placeholder.png"></img>
										</div>
									</div>

									<div class="track__info">
										<span class="undefined links-sentence">
											<span id="playing-now">
												Tuning in...
											</span>
										</span>
									</div>
								</div>
								<div class="playback">
									<figure>
										<audio id="player" autoplay="true" controls="" preload="auto" src="{@mount}"></audio>
									</figure>
								</div>
							</div>
						</div>
					</xsl:for-each>
				</div>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>