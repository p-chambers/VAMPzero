<?xml version="1.0" encoding="utf-8"?>
<!--toolspecific Input Mapping for VAMPzero written by Daniel Boehnke-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="cpacs_schema.xsd">
	<xsl:output method="xml" media-type="text/xml"/>
	<!--get the UID from the toolspecific Block-->
	<xsl:variable name="aircraftModelUID" select="/cpacs/toolspecific/vampZero/aircraftModelUID"/>
	<xsl:variable name="engineUID" select="/cpacs/toolspecific/vampZero/engineUID"/>
	<xsl:template match="/">
		<cpacs>
			<xsl:copy-of select="/cpacs/header"/>
			<vehicles>
				<aircraft>
					<xsl:copy-of select="/cpacs/vehicles/aircraft/model[@uID=$aircraftModelUID]"/>
				</aircraft>
				<engines>
					<xsl:copy-of select="/cpacs/vehicles/engines/engine[@uID=$engineUID]"/>
				</engines>
				<profiles>
					<xsl:copy-of select="/cpacs/vehicles/profiles/wingAirfoils"/>
					<xsl:copy-of select="/cpacs/vehicles/profiles/fuselageProfiles"/>
				</profiles>
			</vehicles>
			<toolspecific>
				<xsl:copy-of select="/cpacs/toolspecific/vampZero"/>
			</toolspecific>
		</cpacs>
	</xsl:template>
</xsl:stylesheet>