In order to train the reference parsing model the training data should be prepared considering the following guideline.
This document further elaborates on the guideline for annotation different bibliographic elements found in a reference.


*  **\<author>**: All authors found in the reference must be enclosed within the <author> </author> tag.
*  **\<given-names>**: First name, middle names, or maiden name of every author found in the reference. 
*  **\<surname>**: Surname of every author found in the reference.
*  **\<lpage>**: Denotes the last page of the article.
*  **\<fpage>**: Denotes the first page of the article.
*  **\<title>**: Describes the article-title.
*  **\<editor>**: Denotes all editors of the reference.
*  **\<identifier>**: Denotes the unique identifier of the reference.
*  **\<url>**: Denotes the url found in the reference.
*  **\<issue>**: Denotes the issue number of the journal.
*  **\<volume>**: Denotes the volume number of the journal.
*  **\<publisher>**: Denotes the publisher of the journal.
*  **\<year>**: Denotes the year in which the article was published.
*  **\<other>**: Part of the reference which are not related to the tags mentioned above should be tagged as other.


Example of annotating a reference:

*Ademczyk, Grzegorz; Gostmann, Peter (2007): Polen zwischen Nation und Europa. Zur Konstruktion kollektiver Identität im polnischen Parlament. Wiesbaden: DUV.*

Annotated reference:

`<author><surname>Ademczyk</surname>, <given-names>Grzegorz</given-names></author>; <author><surname>Gostmann,</surname> <given-names>Peter</given-names></author> (<year>2007</year>): <title>Polen zwischen Nation und Europa. Zur Konstruktion kollektiver Identität im polnischen Parlament</title>. <other>Wiesbaden</other>: <publisher>DUV</publisher>`

**Note** :While annotating bibliographical elements just include the text representing that element and other characters and punctuation marks should be left out. 
For e.g. Characters ';' used as a seperating authors must be left out.
