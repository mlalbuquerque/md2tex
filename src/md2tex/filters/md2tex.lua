-- Filtro Pandoc para adequações específicas do md2tex.

local landscape_mode = "auto"
local wrap_tables = true
local table_font = "small"
local table_width = "auto"

local function meta_to_string(value)
  if value == nil then return "" end
  return pandoc.utils.stringify(value)
end


local function update_lengths_from_rows(rows, lengths)
  if rows == nil then return end
  for _, row in ipairs(rows) do
    for index, cell in ipairs(row.cells) do
      local text = pandoc.utils.stringify(cell.contents)
      local length = #text
      if length > lengths[index] then lengths[index] = length end
    end
  end
end

local function apply_widths(tbl)
  local columns = #tbl.colspecs
  if columns < 2 or table_width == "natural" then return tbl end

  if table_width == "equal" then
    local width = 1.0 / columns
    for index, colspec in ipairs(tbl.colspecs) do
      tbl.colspecs[index] = {colspec[1], width}
    end
    return tbl
  end

  local lengths = {}
  for index = 1, columns do lengths[index] = 8 end
  update_lengths_from_rows(tbl.head.rows, lengths)
  for _, body in ipairs(tbl.bodies) do
    update_lengths_from_rows(body.head, lengths)
    update_lengths_from_rows(body.body, lengths)
  end
  update_lengths_from_rows(tbl.foot.rows, lengths)

  local weighted_total = 0
  local weights = {}
  for index, length in ipairs(lengths) do
    local weight = math.sqrt(length)
    weights[index] = weight
    weighted_total = weighted_total + weight
  end
  if weighted_total <= 0 then return tbl end

  local minimum = columns >= 6 and 0.09 or 0.12
  if minimum * columns >= 0.95 then minimum = 0.95 / columns end
  local remaining = 1.0 - (minimum * columns)

  for index, colspec in ipairs(tbl.colspecs) do
    local proportional = weights[index] / weighted_total
    local width = minimum + (remaining * proportional)
    tbl.colspecs[index] = {colspec[1], width}
  end
  return tbl
end

local function latex_inline_delimited(command, text)
  local delimiters = {"|", "!", "+", ";", ":", "?", "@", "#"}
  for _, delimiter in ipairs(delimiters) do
    if not text:find(delimiter, 1, true) then
      return "\\protect\\" .. command .. delimiter .. text .. delimiter
    end
  end
  -- Caso raro: deixa o Pandoc escapar o conteúdo como texttt.
  return nil
end

local function is_url(text)
  return text:match("^https?://") ~= nil or text:match("^ftp://") ~= nil or
         text:match("^mailto:") ~= nil or text:match("^www%.") ~= nil
end

local function is_path(text)
  return text:match("^/") ~= nil or text:match("^~[/\\]") ~= nil or
         text:match("^%./") ~= nil or text:match("^%.%./") ~= nil or
         text:match("^[A-Za-z]:[/\\]") ~= nil or text:match("^\\\\") ~= nil
end

local function looks_like_command(text)
  if not text:find("%s") then return false end
  local first = text:match("^%s*([^%s]+)") or ""
  local commands = {
    git=true, docker=true, podman=true, kubectl=true, helm=true, npm=true,
    npx=true, yarn=true, pnpm=true, pip=true, pipx=true, python=true,
    python3=true, php=true, composer=true, java=true, mvn=true, gradle=true,
    go=true, cargo=true, rustc=true, make=true, cmake=true, curl=true,
    wget=true, ssh=true, scp=true, rsync=true, sudo=true, apt=true,
    ["apt-get"]=true, systemctl=true, journalctl=true, grep=true, sed=true,
    awk=true, find=true, chmod=true, chown=true, cp=true, mv=true, rm=true,
    mkdir=true, tar=true, unzip=true, zip=true, pandoc=true, xelatex=true,
    lualatex=true, pdflatex=true, latexmk=true, ["md2tex"]=true,
  }
  return commands[first] == true or text:match("^%$%s+") ~= nil
end

local function handle_code(code)
  local text = code.text
  local rendered = nil
  if is_url(text) then
    rendered = latex_inline_delimited("url", text)
  elseif is_path(text) then
    rendered = latex_inline_delimited("path", text)
  elseif looks_like_command(text) then
    rendered = latex_inline_delimited("lstinline", text)
  end
  if rendered then return pandoc.RawInline("latex", rendered) end
end

local function handle_table(tbl)
  tbl = apply_widths(tbl)
  local columns = #tbl.colspecs
  local landscape = landscape_mode == "always" or
    (landscape_mode == "auto" and columns >= 6)

  local before = {}
  local after = {}
  if landscape then table.insert(before, pandoc.RawBlock("latex", "\\begin{landscape}")) end
  if table_font ~= "normalsize" then
    table.insert(before, pandoc.RawBlock("latex", "\\" .. table_font))
  end
  if wrap_tables then
    table.insert(before, pandoc.RawBlock("latex", "\\mdtexStartTable"))
    table.insert(after, 1, pandoc.RawBlock("latex", "\\mdtexEndTable"))
  end
  if landscape then table.insert(after, pandoc.RawBlock("latex", "\\end{landscape}")) end

  local blocks = {}
  for _, block in ipairs(before) do table.insert(blocks, block) end
  table.insert(blocks, tbl)
  for _, block in ipairs(after) do table.insert(blocks, block) end
  return blocks
end


local function latex_from_inlines(inlines)
  local document = pandoc.Pandoc({pandoc.Plain(inlines)})
  local rendered = pandoc.write(document, "latex")
  return rendered:gsub("%s+$", "")
end

local function image_dimension(value, base, fallback)
  if value == nil or value == "" then return fallback end
  local percent = value:match("^([%d%.]+)%%$")
  if percent then
    return string.format("%.4f\\%s", tonumber(percent) / 100, base)
  end
  -- Dimensões LaTeX explícitas podem ser informadas no Markdown.
  if value:match("^[%d%.]+\\[A-Za-z]+$") or value:match("^[%d%.]+(cm|mm|in|pt|em|ex)$") then
    return value
  end
  return fallback
end

local function image_latex(image, block_image)
  local width = image_dimension(image.attributes.width, "linewidth", "0.95\\linewidth")
  local height_default = block_image and "0.78\\textheight" or "0.45\\textheight"
  local height = image_dimension(image.attributes.height, "textheight", height_default)
  local source = image.src:gsub("}", "\\}")
  return "\\adjustbox{max width=" .. width .. ",max height=" .. height .. ",center}" ..
         "{\\includegraphics{\\detokenize{" .. source .. "}}}"
end

local function handle_image_paragraph(para)
  if #para.content ~= 1 or para.content[1].tag ~= "Image" then return nil end
  local image = para.content[1]
  local parts = {
    "\\begin{figure}[htbp]",
    "\\centering",
    image_latex(image, true),
  }
  local caption = latex_from_inlines(image.caption)
  if caption ~= "" then
    table.insert(parts, "\\caption{" .. caption .. "}")
  end
  if image.identifier and image.identifier ~= "" then
    table.insert(parts, "\\label{" .. image.identifier .. "}")
  end
  table.insert(parts, "\\end{figure}")
  return pandoc.RawBlock("latex", table.concat(parts, "\n"))
end

local function handle_inline_image(image)
  return pandoc.RawInline("latex", image_latex(image, false))
end

local div_map = {
  warning = "mdtexWarning",
  decision = "mdtexDecision",
  note = "mdtexNote",
  info = "mdtexNote",
}

local function handle_div(div)
  for _, class in ipairs(div.classes) do
    local environment = div_map[class]
    if environment then
      local result = {pandoc.RawBlock("latex", "\\begin{" .. environment .. "}")}
      for _, block in ipairs(div.content) do table.insert(result, block) end
      table.insert(result, pandoc.RawBlock("latex", "\\end{" .. environment .. "}"))
      return result
    end
  end
end

local function handle_horizontal_rule()
  return pandoc.RawBlock(
    "latex",
    "\\ifcsname mdtexDivider\\endcsname\\mdtexDivider\\else\\par\\noindent\\rule{\\linewidth}{0.4pt}\\par\\fi"
  )
end

local function handle_code_block(block)
  for _, class in ipairs(block.classes) do
    if class == "mermaid" then
      block.identifier = ""
      block.attributes = {}
      return block
    end
  end

  local raw_language = (block.classes[1] or ""):lower()
  local language_map = {
    bash="bash", sh="bash", shell="bash", zsh="bash",
    python="Python", py="Python",
    java="Java", javascript="JavaScript", js="JavaScript",
    php="PHP", sql="SQL", xml="XML", html="HTML",
    c="C", cpp="C++", ["c++"]="C++", csharp="[Sharp]C",
    tex="TeX", latex="TeX", make="make",
  }
  local language = language_map[raw_language] or ""
  local options = "breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true"
  if language ~= "" then options = options .. ",language=" .. language end
  local content = "\\begin{lstlisting}[" .. options .. "]\n" .. block.text .. "\n\\end{lstlisting}"
  return pandoc.RawBlock("latex", content)
end


function Pandoc(doc)
  local meta = doc.meta
  local value = meta["md2tex-landscape-tables"] or meta["netra-landscape-tables"]
  if value then landscape_mode = meta_to_string(value) end

  local wrap = meta["md2tex-wrap-tables"] or meta["netra-wrap-tables"]
  if wrap ~= nil then
    local raw = meta_to_string(wrap):lower()
    wrap_tables = not (raw == "false" or raw == "0" or raw == "no")
  end

  local font = meta["md2tex-table-font"] or meta["netra-table-font"]
  if font then table_font = meta_to_string(font) end

  local width = meta["md2tex-table-width"] or meta["netra-table-width"]
  if width then table_width = meta_to_string(width) end

  -- Primeiro transforma imagens de bloco em figuras completas. Depois trata
  -- imagens realmente inline, evitando que o walker converta a imagem antes
  -- de o parágrafo ser reconhecido como figura.
  doc = doc:walk({Para = handle_image_paragraph})
  return doc:walk({
    Code = handle_code,
    Image = handle_inline_image,
    CodeBlock = handle_code_block,
    Table = handle_table,
    Div = handle_div,
    HorizontalRule = handle_horizontal_rule,
  })
end
