# PowerShell script to create a clean, ultra-compact 25-page DOCX file from Markdown
param(
    [string]$mdPath = "c:\Users\naim2\Codebase\CP\CP_Cheatsheet_Hoffnang.md",
    [string]$docxPath = "c:\Users\naim2\Codebase\CP\CP_Cheatsheet_Hoffnang.docx"
)

Add-Type -AssemblyName System.IO.Compression.FileSystem

$tempDir = Join-Path $env:TEMP ("docx_gen_" + [System.Guid]::NewGuid().ToString("N"))
$wordDir = Join-Path $tempDir "word"
$relsDir = Join-Path $tempDir "_rels"
$wordRelsDir = Join-Path $wordDir "_rels"

New-Item -ItemType Directory -Path $wordRelsDir -Force | Out-Null
New-Item -ItemType Directory -Path $relsDir -Force | Out-Null

# 1. [Content_Types].xml
$contentTypes = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>
'@
[System.IO.File]::WriteAllText((Join-Path $tempDir "[Content_Types].xml"), $contentTypes, [System.Text.Encoding]::UTF8)

# 2. _rels/.rels
$topRels = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
'@
[System.IO.File]::WriteAllText((Join-Path $relsDir ".rels"), $topRels, [System.Text.Encoding]::UTF8)

# 3. word/_rels/document.xml.rels
$docRels = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
'@
[System.IO.File]::WriteAllText((Join-Path $wordRelsDir "document.xml.rels"), $docRels, [System.Text.Encoding]::UTF8)

# 4. word/styles.xml (Ultra-compact typography)
$stylesXml = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
        <w:sz w:val="18"/>
        <w:color w:val="111827"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:after="40" w:line="220" w:lineRule="auto"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:pPr>
      <w:spacing w:before="160" w:after="60"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="26"/>
      <w:color w:val="1E3A8A"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:pPr>
      <w:spacing w:before="120" w:after="40"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="22"/>
      <w:color w:val="1D4ED8"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:pPr>
      <w:spacing w:before="90" w:after="30"/>
    </w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="19"/>
      <w:color w:val="0369A1"/>
    </w:rPr>
  </w:style>
</w:styles>
'@
[System.IO.File]::WriteAllText((Join-Path $wordDir "styles.xml"), $stylesXml, [System.Text.Encoding]::UTF8)

function Escape-Xml([string]$str) {
    if ([string]::IsNullOrEmpty($str)) { return "" }
    return $str.Replace('&', '&amp;').Replace('<', '&lt;').Replace('>', '&gt;').Replace('"', '&quot;').Replace("'", '&apos;')
}

$lines = [System.IO.File]::ReadAllLines($mdPath, [System.Text.Encoding]::UTF8)
$bodyXml = New-Object System.Text.StringBuilder
[void]$bodyXml.Append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$bodyXml.Append('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">')
[void]$bodyXml.Append('<w:body>')

$inCode = $false
foreach ($line in $lines) {
    if ($line -match '^```') {
        $inCode = -not $inCode
        continue
    }

    if ($inCode) {
        $esc = Escape-Xml $line
        [void]$bodyXml.Append('<w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/><w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="auto"/><w:ind w:left="80" w:right="80"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="15"/><w:color w:val="0F172A"/></w:rPr><w:t xml:space="preserve">' + $esc + '</w:t></w:r></w:p>')
        continue
    }

    if ($line -match '^#\s+(.+)$') {
        $text = Escape-Xml $matches[1]
        [void]$bodyXml.Append('<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="1E3A8A"/></w:rPr><w:t>' + $text + '</w:t></w:r></w:p>')
    } elseif ($line -match '^##\s+(.+)$') {
        $text = Escape-Xml $matches[1]
        [void]$bodyXml.Append('<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="1D4ED8"/></w:rPr><w:t>' + $text + '</w:t></w:r></w:p>')
    } elseif ($line -match '^###\s+(.+)$') {
        $text = Escape-Xml $matches[1]
        [void]$bodyXml.Append('<w:p><w:pPr><w:pStyle w:val="Heading3"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="19"/><w:color w:val="0369A1"/></w:rPr><w:t>' + $text + '</w:t></w:r></w:p>')
    } elseif ($line.Trim() -eq '---') {
        [void]$bodyXml.Append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="CBD5E0"/></w:pPr></w:p>')
    } elseif ($line.Trim() -eq '') {
        # keep minimal whitespace
    } else {
        $cleanLine = $line
        $isBullet = $false
        if ($cleanLine -match '^\s*[-*]\s+(.+)$') {
            $isBullet = $true
            $cleanLine = $matches[1]
        }
        $esc = Escape-Xml $cleanLine
        if ($isBullet) {
            [void]$bodyXml.Append('<w:p><w:pPr><w:ind w:left="200"/><w:spacing w:after="20"/></w:pPr><w:r><w:rPr><w:color w:val="2563EB"/></w:rPr><w:t xml:space="preserve">• </w:t></w:r><w:r><w:t>' + $esc + '</w:t></w:r></w:p>')
        } else {
            [void]$bodyXml.Append('<w:p><w:r><w:t>' + $esc + '</w:t></w:r></w:p>')
        }
    }
}

# 2-Column Section layout with tight 0.4-inch (576 dxa) margins
[void]$bodyXml.Append('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="576" w:right="576" w:bottom="576" w:left="576"/><w:cols w:num="2" w:space="288"/></w:sectPr>')
[void]$bodyXml.Append('</w:body></w:document>')

[System.IO.File]::WriteAllText((Join-Path $wordDir "document.xml"), $bodyXml.ToString(), [System.Text.Encoding]::UTF8)

if (Test-Path $docxPath) { Remove-Item $docxPath -Force }
[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $docxPath)
Remove-Item -Recurse -Force $tempDir

Write-Host "Generated compact 2-column DOCX file at: $docxPath"
