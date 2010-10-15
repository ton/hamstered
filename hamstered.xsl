<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/report">
        <html>
            <head>
                <link rel="stylesheet" href="hamstered.css" type="text/css" />
            </head>
            <body>
                <h1>Uren overzicht (<xsl:value-of select="@start_date"/> - <xsl:value-of select="@end_date"/>)</h1>
                <xsl:for-each select="day">
                    <div class="daybox">
                        <h2>
                            <xsl:choose>
                                <xsl:when test="@week_day=0">
                                    maandag
                                </xsl:when>
                                <xsl:when test="@week_day=1">
                                    dinsdag
                                </xsl:when>
                                <xsl:when test="@week_day=2">
                                    woensdag
                                </xsl:when>
                                <xsl:when test="@week_day=3">
                                    donderdag
                                </xsl:when>
                                <xsl:when test="@week_day=4">
                                    vrijdag
                                </xsl:when>
                                <xsl:when test="@week_day=5">
                                    zaterdag
                                </xsl:when>
                                <xsl:when test="@week_day=6">
                                    zondag
                                </xsl:when>
                            </xsl:choose>
                            <xsl:value-of select="@date"/>
                        </h2>
                        <table width="40%">
                            <tr>
                                <td>Activiteit</td>
                                <td>Start tijd</td>
                                <td>Eind tijd</td>
                                <td>Uren</td>
                            </tr>
                            <xsl:for-each select="activity">
                                <tr>
                                    <td><xsl:value-of select="@name"/></td>
                                    <td width="15%"><xsl:value-of select="@start_time"/></td>
                                    <td width="15%"><xsl:value-of select="@end_time"/></td>
                                    <td width="15%"><xsl:value-of select="@duration"/></td>
                                </tr>
                            </xsl:for-each>
                            <tr>
                                <td colspan="3" align="right"><b>Totaal:</b></td>
                                <td><xsl:value-of select="sum(activity/@duration)"/></td>
                            </tr>
                        </table>
                    </div>
                    <xsl:if test="position() > 0 and position() mod 10 = 0">
                        <div class="pagebreak"></div>
                    </xsl:if>
                </xsl:for-each>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>
