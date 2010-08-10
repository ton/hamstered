<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h1>Uren overzicht</h1>
  <xsl:for-each select="report/day">
  <h2><xsl:value-of select="@date"/></h2>
  <table width="75%">
    <tr>
      <th width="25%">Activiteit</th>
      <th>Start tijd</th>
      <th>Eind tijd</th>
      <th>Uren</th>
    </tr>
    <xsl:for-each select="activity">
    <tr>
      <td><xsl:value-of select="@name"/></td>
      <td><xsl:value-of select="@start_time"/></td>
      <td><xsl:value-of select="@end_time"/></td>
      <td><xsl:value-of select="@duration"/></td>
    </tr>
    </xsl:for-each>
    <tr>
      <td>Totaal:</td>
      <td colspan="3"></td>
    </tr>
  </table>
  </xsl:for-each>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
