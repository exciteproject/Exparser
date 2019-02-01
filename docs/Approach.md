The proposed method of extraction references from PDF documents operates in two correlated phases: reference line classiffcation and reference segmentation & identification.

## Features
A set of features has been extracted from each line and each token to classify lines and segment reference strings, respectively. 
### Line-based (ln)
#### get_cc(ln):
*Description*: The ratio of Uppercase characters to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_cc(ln):
*Description*: The ratio of Lowercase characters to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_cw(ln):
*Description*: The ratio of tokens that begings with Uppercase characters to the total number of tokens <br/>
*Output*: Numeric, in the range [0,1]

#### get_sw(ln):
*Description*: The ratio of tokens that begings with Lowercase characters to the total number of tokens <br/>
*Output*: Numeric, in the range [0,1]

#### get_yr(ln):
*Description*: Whether a **year** format (from 1800 to 2029) appears in the line<br/>
*Output*: Boolean value (0 or 1)

#### get_qm(ln):
*Description*: The ratio of quotations **(' | " | \` | « | »)** to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_cl(ln):
*Description*: The ratio of double colon **(:)** to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_sl(ln):
*Description*: The ratio of slash and backslash **(\\ | \/)** to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_bs(ln):
*Description*: The ratio of slash and brackets, including: parentheses, braces and quare brackets **((|)|{|}|\[|\])**, to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_dt(ln):
*Description*: The ratio of full points, or full stop **(.)**, to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_cm(ln):
*Description*: The ratio of comma **(,)**, to the total number of charachters (Whitespace characters are not counted)<br/>
*Output*: Numeric, in the range [0,1]

#### get_cd(ln):
*Description*: The ratio of initials **(e.g. A. | C.D.)**, to the total number of token<br/>
*Output*: Numeric, in the range [0,1]

#### get_lh(ln):

#### get_ch(ln):

#### get_pg(ln):
*Description*: Whether the line contains page format **(58 -- 78)**<br/>
*Output*: Numeric, in the range [0,1]

#### get_hc(ln):

#### get_pb(ln):

#### get_wc(ln):

#### get_ll(ln):

#### get_llw(ln):

#### get_lv(ln):
*Description*: The vertical position of the line w.r.t the entire file<br/>
*Output*: Numeric, in the range [0,1]

#### get_lex1(ln):
*Description*: Whether the line contains: **In: | In | in:**<br/>
*Output*: Boolean value (0 or 1)

#### get_lex2(ln):
*Description*: Whether the line contains: **hg. | hrsg. | ed. | eds.** (Uppercase is not preserved)<br/>
*Output*: Boolean value (0 or 1)

#### get_lex3(ln):
*Description*: Whether the line contains: **verlag | press | university | universität | publication(s) | publishing | publisher(s) | book | institut(e)** (Uppercase is not preserved)<br/>
*Output*: Boolean value (0 or 1)


#### get_lex4(ln):
*Description*: Whether the line contains an ampersand **(&)**<br/>
*Output*: Boolean value (0 or 1)

#### get_lex5(ln):
*Description*: Whether the line contains: **Journal**<br/>
*Output*: Boolean value (0 or 1)

#### get_lex6(ln):
*Description*: Whether the line contains: **bd. | band** (Uppercase is not preserved)<br/>
*Output*: Boolean value (0 or 1)

#### get_lex7(ln):
*Description*: Whether the line contains: **S. | PP. | pp. | ss. | SS. | pages.**<br/>
*Output*: Boolean value (0 or 1)

#### get_lnk(ln):
*Description*: Whether the line contains a link format **(http://xyz.com)**<br/>
*Output*: Boolean value (0 or 1)

#### get_vol(ln):
*Description*: Whether the line contains: **vol. | jg.** (Uppercase is not preserved)<br/>
*Output*: Boolean value (0 or 1)


#### get_und(ln):
*Description*: Whether the line contains: **u. | and | und**<br/>
*Output*: Boolean value (0 or 1)

#### get_amo(ln):

#### get_num(ln):
*Description*: Whether the line contains: **No(.,:) | Nr(.,:)**<br/>
*Output*: Boolean value (0 or 1)


#### get_db(ln):
### Token-based
