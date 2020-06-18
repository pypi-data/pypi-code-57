import unittest
import os
import io

from lxml import etree

from converter import converters

APP_PATH = os.path.dirname(os.path.realpath(__file__))


class TestEruditPS2HTMLCSSLoading(unittest.TestCase):

    def setUp(self):

        self.conv = converters.EruditPS2HTML(
            source=APP_PATH + '/fixtures/eruditps/document_eruditps.xml'
        )

    def test_load_templates_base_templates(self):

        result = self.conv._prepare_templates(custom_templates=None)

        expected = [
            'static/templates/default/pagedmedia.css',
            'static/templates/default/style.css'
        ]

        self.assertEqual(result, expected)

    def test_load_templates_clean_one_column(self):

        custom_templates = [
            'clean-one-column'
        ]

        result = self.conv._prepare_templates(custom_templates=custom_templates)

        expected = [
            'static/templates/clean-one-column/pagedmedia.css',
            'static/templates/default/style.css',
            'static/templates/clean-one-column/style.css'
        ]

        self.assertEqual(result, expected)

    def test_load_templates_documentation(self):

        custom_templates = [
            'documentation'
        ]

        result = self.conv._prepare_templates(custom_templates=custom_templates)

        expected = [
            'static/templates/default/pagedmedia.css',
            'static/templates/default/style.css',
            'static/templates/documentation/style.css'
        ]

        self.assertEqual(result, expected)

class TestEruditPS2HTML(unittest.TestCase):

    def setUp(self):

        self.conv = converters.EruditPS2HTML(
            source=APP_PATH + '/fixtures/eruditps/document_eruditps.xml'
        )

        self.xml = self.conv.transform(lxml_etree=True)

    def test_text_encadre(self):
        inputxml = """
            <article xml:lang="fr" xmlns:xlink="http://www.w3.org/1999/xlink">
                <body>
                    <sec>
                        <boxed-text content-type="frame" id="en1">
                            <label>Encadré 1</label>
                            <caption xml:lang="fr">
                                <title>Pierre Harvey</title>
                            </caption>
                            <sec>
                                <fig id="fi4">
                                    <caption xml:lang="fr">
                                        <title>PIERRE HARVEY, Président de la .</title>
                                    </caption>
                                    <graphic id="im6" xlink:href="1861201n.jpg" position="float" content-type="figure"/>
                                </fig>
                                <p>Paragraph 1</p>
                                <p>Paragraph 2</p>
                                <p>Paragraph 3</p>
                            </sec>
                        </boxed-text>
                    </sec>
                </body>
            </article>
        """

        conv = converters.EruditPS2HTML(io.BytesIO(inputxml.encode('utf-8')))
        self.xml = conv.transform(lxml_etree=True)

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="body">
              <div class="sec">
                <div class="boxed-text">
                  <div class="boxed-header">
                    <div class="label">Encadr&#233; 1</div>
                    <div class="caption">
                      <div class="title">Pierre Harvey</div>
                    </div>
                  </div>
                  <div class="boxed-content">
                    <div class="sec">
                      <div class="fig" id="fi4">
                        <div class="fig-header">
                          <div class="title">PIERRE HARVEY, Pr&#233;sident de la .</div>
                        </div>
                        <div class="fig-content">
                          <div class="image-float">
                            <img src="1861201n.jpg"/>
                          </div>
                        </div>
                      </div>
                      <p>Paragraph 1</p>
                      <p>Paragraph 2</p>
                      <p>Paragraph 3</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        """

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']")
        self.maxDiff = None
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_sub_sections(self):
        inputxml = """
            <article>
                <body>
                    <sec>
                        <title>Section 1</title>
                        <p>Text</p>
                        <sec>
                            <title>Section 2</title>
                            <p>Text</p>
                            <sec>
                                <title>Section 3</title>
                                <p>Text</p>
                                <sec>
                                    <title>Section 4</title>
                                    <p>Text</p>
                                    <sec>
                                        <title>Section 5</title>
                                        <p>Text</p>
                                        <sec>
                                            <title>Section 6</title>
                                            <p>Text</p>
                                        </sec>
                                    </sec>
                                </sec>
                            </sec>
                        </sec>
                    </sec>
                </body>
            </article>
        """

        conv = converters.EruditPS2HTML(io.BytesIO(inputxml.encode('utf-8')))
        self.xml = conv.transform(lxml_etree=True)

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="body">
              <div class="sec">
                <div class="title">Section 1</div>
                <p>Text</p>
                <div class="sec">
                  <div class="title">Section 2</div>
                  <p>Text</p>
                  <div class="sec">
                    <div class="title">Section 3</div>
                    <p>Text</p>
                    <div class="sec">
                      <div class="title">Section 4</div>
                      <p>Text</p>
                      <div class="sec">
                        <div class="title">Section 5</div>
                        <p>Text</p>
                        <div class="sec">
                          <div class="title">Section 6</div>
                          <p>Text</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        """

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']")
        self.maxDiff = None
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_text_formating(self):
        inputxml = """
            <article>
                <body>
                    <sec>
                        <title>Testing text formating convertions</title>
                        <p>
                            <bold>bold</bold>
                            <italic>italic</italic>
                            <underline>underline</underline>
                            <overline>overline</overline>
                            <strike>strike</strike>
                            <sc>smallcaps</sc>
                            <styled-content style-type="text-uppercase">uppercase</styled-content>
                            <styled-content style-type="text-boxed">boxed</styled-content>
                            <styled-content style-type="text-bigger">bigger</styled-content>
                            <styled-content style-type="text-smaller">smaller</styled-content>
                            <monospace>monospace</monospace>
                            <sub>sub</sub>
                            <sup>sup</sup>
                        </p>
                    </sec>
                </body>
            </article>
        """

        conv = converters.EruditPS2HTML(io.BytesIO(inputxml.encode('utf-8')))
        self.xml = conv.transform(lxml_etree=True)

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="body">
              <div class="sec">
                <div class="title">Testing text formating convertions</div>
                <p>
                  <b>bold</b>
                  <i>italic</i>
                  <u>underline</u>
                  <span class="text-overline">overline</span>
                  <span class="text-strike">strike</span>
                  <small>smallcaps</small>
                  <span class="text-uppercase">uppercase</span>
                  <span class="text-boxed">boxed</span>
                  <big>bigger</big>
                  <small>smaller</small>
                  <span class="text-monospace">monospace</span>
                  <sub>sub</sub>
                  <sup>sup</sup>
                </p>
              </div>
            </div>
        """

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']")
        self.maxDiff = None
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_journal_title(self):

        result = self.xml.find("head/meta[@name='journal-title']").get('content')

        self.assertEqual(result, 'Approches inductives : Travail intellectuel et construction des connaissances')

    def test_article_page_title(self):

        result = self.xml.find("head/title").text

        self.assertEqual(result, 'Approches inductives: « Chantez au Seigneur un chant nouveau... » (Ps.95.1) : le portrait de la musique rock chrétienne')

    def test_article_meta_article_id_doi(self):

        result = self.xml.find("head/meta[@name='doi']").get('content')

        self.assertEqual(result, 'https://doi.org/10.7202/1025748ar')

    def test_article_meta_title_group_title(self):

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='title-group']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="title-group">
              <div class="article-title">« Chantez au Seigneur un chant nouveau... » (Ps.95.1) : le portrait de la musique <i>rock</i> chrétienne</div>
              <div class="subtitle">Article <i>Subtitle</i></div>
              <div class="reviewed-product"><small>Bornand</small>, Marie, <i>Témoignage et fiction. Les récits de rescapés dans la littérature de langue française (1945-2000)</i>, Genève, Librairie Droz, 2004.</div>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_article_meta_product(self):

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='title-group']/div[@class='reviewed-product']")

        expected = '<div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="reviewed-product"><small>Bornand</small>, Marie, <i>Témoignage et fiction. Les récits de rescapés dans la littérature de langue française (1945-2000)</i>, Genève, Librairie Droz, 2004.</div>'

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_article_meta_title_group_subtitle(self):

        result = self.xml.find(
            "body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='title-group']/div[@class='subtitle']"
        )

        expected = '<div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="subtitle">Article <i>Subtitle</i></div>'

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_article_meta_title_group_translated_title(self):

        result = self.xml.find(
            "body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='trans-title-group']"
        )

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="trans-title-group">
              <div class="trans-title">Translated title in <i>english</i></div>
              <div class="trans-subtitle">Translated subtitle in <i>english</i></div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )


    def test_article_meta_title_group_translated_subtitle(self):

        result = self.xml.find(
            "body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='trans-title-group']/div[@class='trans-subtitle']"
        )

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="trans-subtitle">Translated subtitle in <i>english</i></div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_article_meta_contrib_group_num_authors(self):

        result = len(self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='contrib-group']//div[@class='contrib']"))

        self.assertEqual(result, 5)

    def test_article_meta_contrib_group(self):

        result = self.xml.find(
            "body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='contrib-group']"
        )

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="contrib-group">
              <div class="contrib">
                <div class="name">Marie-Chantal <span class="surname">Falardeau</span></div>
                <div class="institution">Université du Québec à Trois-Rivières</div>
                <div class="email">falardeau_fake@email.com</div>
              </div>
              <div class="contrib">
                <div class="name">Stéphane Marie <span class="surname">Perreault</span></div>
                <div class="institution">Test Affiliation</div>
              </div>
              <div class="contrib">
                <div class="name">Rémy <span class="surname">François</span></div>
              </div>
              <div class="contrib-collab">
                <div class="collab-name">Théâtre Deuxième Réalité</div>
                <div class="contrib">
                  <div class="name">Alexandre <span class="surname">Marine</span></div>
                  <div class="institution">Test Affiliation</div>
                  <div class="email">alexandre_fake@email.com</div>
                </div>
                <div class="contrib">
                  <div class="name">Joseph <span class="surname">Joseph</span></div>
                  <div class="institution">Test Affiliation</div>
                  <div class="email">joseph_fake@email.com</div>
                </div>
              </div>
              <div class="contrib-collab">
                <div class="collab-name">ACME</div>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )


    def test_article_meta_contrib_group_content_surname(self):

        nomsfamille = self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='front']//div[@class='contrib-group']//span[@class='surname']")

        result = [i.text for i in nomsfamille]

        self.assertEqual(sorted(result), sorted(['Falardeau', 'Perreault', 'François', 'Marine', 'Joseph']))

    def test_article_meta_contrib_group_content_given_names(self):

        givennames = self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='front']//div[@class='contrib-group']//div[@class='name']")

        result = [i.text.strip() for i in givennames]

        self.assertEqual(result, ['Marie-Chantal', 'Stéphane Marie', 'Rémy', 'Alexandre', 'Joseph'])

    def test_article_meta_contrib_group_content_nomorg(self):

        result = [i.text for i in self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='contrib-group']//div[@class='collab-name']")]

        self.assertEqual(result, ['Théâtre Deuxième Réalité', 'ACME'])

    def test_article_meta_contrib_group_content_membre(self):
        result = [i.text for i in self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='contrib-group']/div[@class='contrib-collab']/div[@class='contrib']/div[@class='name']/span[@class='surname']")]

        self.assertEqual(result, ['Marine', 'Joseph'])

    def test_article_meta_contrib_email(self):

        result = [i.text for i in self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='contrib-group']//div[@class='email']")]

        self.assertEqual(result, ['falardeau_fake@email.com', 'alexandre_fake@email.com', 'joseph_fake@email.com'])

    def test_article_meta_contrib_bio(self):

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='back']/div[@class='bio-notes']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="bio-notes">
              <div class="title">Notes biographiques</div>
              <div class="bio">
                <p><b><small>Nancy R. Lange </small></b>a publié quatre recueils de poésie aux Écrits des Forges : <i>Annabahébec, Femelle Faucon</i>, <i>Reviens chanter rossignol </i>et <i>Au seuil du bleu </i>(voir p. 95). Elle a publié des poèmes dans des collectifs (<i>Château Bizarre</i>; voir p. 104) et en revue (<i>Brèves littéraires </i>79, 80<i>, Exit, Arcade, Estuaire, Moebius</i>). Elle a collaboré à <i>Macadam tribu</i> et à des spectacles multimédia, dont <i>Au seuil du bleu</i> (JMLDA et Sainte-Rose en Bleu 2009, des productions de la SLL; <i>Brèves littéraires</i> 80). Elle a participé à deux autres activités de la SLL en 2010 : Journées de la culture (voir p. 36) et Sainte-Rose en Bleu (voir p. 15).</p>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    @unittest.skip("to fix encode problem")
    def test_article_head(self):

        result = self.xml.find("head")

        expected = """
            <head xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
              <title>Approches inductives: « Chantez au Seigneur un chant nouveau... » (Ps.95.1) : le portrait de la musique rock chrétienne</title>
              <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
              <meta name="journal-title" content="Approches inductives : Travail intellectuel et construction des connaissances"/>
              <meta name="issue-label" content="Approches inductives en communication sociale, 1(1) automne 2014"/>
              <meta name="license" content="Tous droits réservés © Approches inductives, 2014"/>
              <meta name="doi" content="https://doi.org/10.7202/1025748ar"/>
            </head>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.maxDiff = None

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )


    def test_abstract_group_and_keywords(self):

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='abstract-group']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="abstract-group">
              <div class="abstract">
                <div class="title">Resume</div>
                <p>Le but de cet article est de présenter les raisons du choix d’une approche inductive, plutôt qu’une approche déductive, afin d’étudier la musique rock chrétienne. Cette étude dresse un portrait des chansons les plus populaires de la musique rock chrétienne tout en décrivant quantitativement les éléments structurels de ces dernières. Afin de réaliser ce projet, nous avons répertorié tous les numéros un du palmarès américain <i>Christian Songs</i> depuis sa création en 2003 jusqu’à la fin de l’année 2011, soit 65 chansons. Le portrait de la musique rock chrétienne se décline en onze catégories dont les plus récurrentes sont la dévotion, la présence de Dieu et l’espoir. Cette musique est aussi chantée majoritairement par des hommes et se caractérise par un rythme lent.</p>
                <div class="kwd-group">
                  <div class="title">Motclés</div>
                  <ul>
                    <li>Étude mixte</li>
                    <li>méthodologie inductive</li>
                    <li>musique rock chrétienne</li>
                    <li>analyse de contenu</li>
                  </ul>
                </div>
              </div>
              <div class="abstract">
                <div class="title">Abstract</div>
                <p>Abstract translation sample.</p>
                <div class="kwd-group">
                  <div class="title">Keywords</div>
                  <ul>
                    <li>keyword in english</li>
                  </ul>
                </div>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.maxDiff = None

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_ack(self):

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='back']/div[@class='ack-group']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="ack-group">
              <div class="ack">
                <div class="title">Merci</div>
                <p>Cet <i>article</i> est une version modifiée d’un texte présenté au séminaire HPES du CLERSE (Université Lille I). Nous remercions Vincent Duwicquet, Jordan Melmiès et Jonathan Marie pour leurs commentaires, Malika Riboudt pour l’assistance technique sur Maple, Marc Lavoie et Louis-Philippe Rochon pour leurs conseils. Nous tenons également à faire part de notre gratitude aux rapporteurs de la revue pour leurs remarques pertinentes. Néanmoins, nous demeurons seuls responsables des erreurs pouvant subsister.</p>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_xref_fn(self):

        xref_fns = self.xml.findall("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//a[@class='xref']")

        result = ['-'.join([i.get('href'), i.get('id'), i.text]) for i in xref_fns]

        expected = ['#no1-relno1-1', '#no2-relno2-2', '#no3-relno3-3', '#no4-relno4-4', '#no5-relno5-5', '#no6-relno6-6']

        self.assertEqual(result, expected)

    def test_table(self):
        result = self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='table-wrap' and @id='ta1']")[0]

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="table-wrap" id="ta1">
              <div class="table-wrap-header">
                <div class="label">Tableau 1</div>
                <div class="title">Synthèse des analyses de contenu aux États-Unis, 1969-2006</div>
              </div>
              <div class="table-wrap-content">
                <div class="image-float">
                  <img src="image_tableau_1.png"/>
                </div>
              </div>
              <div class="table-notes">
                <div class="note">
                  <div class="label">1</div>
                  <div class="content">
                    <p>Sample of table notes</p>
                  </div>
                </div>
              </div>
              <div class="attrib">Sample of source data</div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_table_wrap_with_text_table(self):

        result = self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='table-wrap' and @id='ta6']")[0]

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="table-wrap" id="ta6">
              <div class="table-wrap-header">
                <div class="label">Tableau 4</div>
                <div class="title">Statistiques des édifices et de leur destruction à Lamaria</div>
              </div>
              <div class="table-wrap-content">
                <table>
                  <colgroup>
                    <col align="left" valign="middle"/>
                    <col align="center"/>
                    <col align="center"/>
                    <col align="center"/>
                  </colgroup>
                  <thread>
                    <tr>
                      <th align="center" valign="middle">Maisons</th>
                      <th align="center">Secteur urbain</th>
                      <th align="center">Secteur rural</th>
                      <th align="center">Total</th>
                    </tr>
                  </thread>
                  <tfoot>
                    <tr>
                      <td align="right" valign="middle">Total</td>
                      <td align="right">4834</td>
                      <td align="right">2686</td>
                      <td align="right">7520</td>
                    </tr>
                  </tfoot>
                  <tbody>
                    <tr>
                      <td align="left" valign="middle">Détruites</td>
                      <td align="center">1888</td>
                      <td align="center">1198</td>
                      <td align="center">3086</td>
                    </tr>
                    <tr>
                      <td align="left" valign="middle">Endommagées</td>
                      <td align="center">1342</td>
                      <td align="center">297</td>
                      <td align="center">1639</td>
                    </tr>
                    <tr>
                      <td align="left" valign="middle">Sous-total</td>
                      <td align="center">3230</td>
                      <td align="center">1495</td>
                      <td align="center">4725</td>
                    </tr>
                    <tr>
                      <td align="left" valign="middle">Intactes</td>
                      <td align="center">1604</td>
                      <td align="center">1191</td>
                      <td align="center">2795</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_figure_label(self):

        result = self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='fig' and @id='fi1']")[0]

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="fig" id="fi1">
              <div class="fig-header">
                <div class="label">Figure 1</div>
                <div class="title">Modèle des valeurs de Schwartz (1992)</div>
              </div>
              <div class="fig-content">
                <div class="image-float">
                  <img src="image_figure_1.png"/>
                </div>
              </div>
              <div class="attrib">Sample of source data</div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_epigraph(self):

        result = self.xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']/div[@class='epigraph']")
        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="epigraph">
              <p>Un jour, tout sera bien, voilà notre espérance :</p>
              <p>Tout est bien aujourd’hui, voilà l’illusion.</p>
              <div class="attrib">Voltaire, <i>Le désastre de Lisbonne</i></div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_refbiblio_first(self):

        result = self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='back']/div[@class='ref-list']/ul/li")[0]

        expected = """<li xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="ref">Abu-Haidar, F. (1995). The linguistic content of Iraqi popular songs. <i>Studia Orientalia, 75</i>, 9-23.\n        </li>"""

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_refbiblio_last(self):

        result = self.xml.xpath("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='back']/div[@class='ref-list']/ul/li")[-1]

        expected = """<li xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="ref">Zhao, S. (1991). Metatheory, metamethod, meta-data-analysis : what, why, and how? <i>Sociological Perspectives, 34</i>, 377-390.\n        <div class="doi">doi : <a href="https://doi.org/10.2307/1389517">https://doi.org/10.2307/1389517</a></div></li>"""

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_bio_in_sample_corpus(self):
        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/bio/erudit:erudit.cuizine102.cuizine2503.019372ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='back']/div[@class='bio-notes']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="bio-notes">
              <div class="title">Biographic notes</div>
              <div class="bio">
                <p><b>Lisa Harris</b> is a Commonwealth Scholar in the English Department at the University of British Columbia.</p>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_block_citation_in_sample_corpus(self):
        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/block-citation/erudit:erudit.ae49.ae03128.1040505ar.xml',
            lxml_etree=True
        )

        result = xml.findall("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='block-citation']")[0]

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="block-citation">
                <p>Le rôle de l’économiste est d’aider à pallier les défaillances du marché. </p>
                <div class="attrib">Jean Tirole, <i>Économie du bien commun</i> :           383</div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_boxed_text_in_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/boxed-text/erudit:erudit.ae49.ae03070.1039880ar.xml',
            lxml_etree=True
        )

        result = xml.findall("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='boxed-text']")[0]

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="boxed-text">
              <div class="boxed-header">
                <div class="label">Encadré</div>
                <div class="caption">
                  <div class="title">Le jeu de contribution volontaire à un bien public</div>
                </div>
              </div>
              <div class="boxed-content">
                <div class="sec">
                  <p>Le jeu de contribution volontaire (<i>voluntary             contribution mechanism</i>, VCM) a été développé afin de mesurer l’étendue             effective du problème de passager clandestin dans le financement des biens publics.             Chaque joueur <i>i</i> reçoit une dotation initiale             qu’il peut choisir d’allouer à un bien public ou à un bien privé. Pour ce faire, chacun             des <i>N</i> joueurs reçoit au début du jeu une             dotation monétaire <i>e</i><sub><i>i</i></sub>. Ensuite, les participants choisissent             simultanément combien ils souhaitent investir dans le bien public; <i>c</i><sub><i>i</i></sub><i>, </i>0 ≤<i> c</i><sub><i>i</i></sub><i> ≤ e</i><sub><i>i</i></sub>, le reste de la dotation étant investi dans le             bien privé. Le rendement individuel du bien privé pour l’investisseur est de <i>p</i> par unité investie. Le bien public bénéficie quant à             lui à l’ensemble des membres du groupe, à hauteur de <i>m</i> par unité investie par l’un des joueurs. Le gain d’un joueur est donc :             <i>p</i>(<i>e</i><sub><i>i</i></sub>- <i>c</i><sub><i>i</i></sub>) + <i>m</i>(Σ<sub><i>j</i></sub><i>c</i><sub><i>j</i></sub>)/<i>N</i>. D’un point de vue collectif, l’usage efficace des             ressources disponibles implique d’investir l’intégralité des dotations individuelles             dans le bien public dès lors que <i>m &gt; p</i> soit             encore <i>m/(pN) &gt; </i>1<i>/N</i>, puisqu’alors chaque unité investie dans le bien             public produit une richesse supérieure à l’investissement de cette même unité dans le             bien privé. </p>
                  <p>D’un point de vue individuel, l’investissement est gouverné par la comparaison des             rendements, c’est-à-dire le bénéfice individuel associé à chacun des deux             investissements. Or, le rendement marginal privé de l’investissement dans le bien public             est <i>m/N</i>, puisque le bénéfice de             l’investissement est réparti entre tous les membres du groupe. La décision             d’investissement individuellement rationnelle consiste donc à investir l’ensemble de la             dotation dans le bien privé dès lors que <i>m/N &lt;             p</i>, soit encore <i>m/(pN) &lt; </i>1. Si les             rendements sont choisis de telle sorte que 1<i>/N &lt; m/(pN)             &lt; </i>1, cette situation constitue un archétype dilemme social. La solution             collectivement souhaitable d’investissement dans le bien public est en contradiction             avec les décisions individuelles décentralisées en raison de l’incitation individuelle à             se comporter en passage clandestin du financement consenti par les autres membres du             groupe. </p>
                  <p>Dans l’expérience de Dulleck, Koessler et Page (2014), les participants reçoivent             une somme de 20 unités monétaires expérimentales (<i>e             </i>= 20) et forment des groupes de 4 (<i>N             </i>= 4). Le multiplicateur des sommes investies est de 4 pour le bien public             (<i>m </i>= 4) et le multiplicateur des sommes             investies dans le bien privé est égal à 1 (<i>p </i>=             1). </p>
                </div>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_contrib_collab_in_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/contrib-collab/erudit:erudit.dss29.dss1042.012602ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='front']/div[@class='contrib-group']/div[@class='contrib-collab']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="contrib-collab">
              <div class="collab-name">Centre de        santé et des services sociaux de la communauté de Nutashkuan</div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_dedication_in_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/dedication/erudit:erudit.arbo139.arbo01600.1027428ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']/div[@class='dedication']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="dedication">
              <p>En souvenir de Catherine Viollet</p>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_disp_formula_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/disp-formula-1/erudit:erudit.cgq70.cgq03211.1041222ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='disp-formula']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="disp-formula">
              <div class="image-float">
                <img src="2022233n.jpg"/>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_disp_formula_inline_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/disp-formula-1/erudit:erudit.cgq70.cgq03211.1041222ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//span[@class='inline-graphic']/img")

        expected = """
            <img xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" src="2022243n.jpg"/>
        """

        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_epigraph_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/epigraph/erudit:erudit.annuaire130.annuaire01550.1027010ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='epigraph']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="epigraph">
              <p>La voie d’accès au présent a nécessairement la forme d’une archéologie.</p>
              <div class="attrib">Giorgio Agamben, <i>Qu’est-ce que le\n          contemporain ?</i></div>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_example_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/example/erudit:erudit.meta15.meta02462.1036144ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='example']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="example">
              <div class="label">1</div>
              <p>
                <i>This was an ancient battle </i>
                <i>
                  <u>between</u>
                </i>
                <i> the two women (GN1)</i>
                <sup>
                  <a href="#no7" id="relno7" class="xref">7</a>
                </sup>
              </p>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_fig_group_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/fig-group/erudit:erudit.crimino12.crimino02155.1033845ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='fig-group']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="fig-group" id="">
              <div class="fig-group-header">
                <div class="label">Figure 1</div>
                <div class="caption">
                  <div class="title">Exemples de chaque émotion à l’aide des différents personnages de l’ensemble de               stimuli virtuels</div>
                </div>
              </div>
              <div class="fig-group-content">
                <div class="fig" id="fi1">
                  <div class="fig-header"/>
                  <div class="fig-content">
                    <div class="image-float">
                      <img src="1961453n.jpg"/>
                    </div>
                  </div>
                  <div class="figure-notes">
                    <p>Joie 60 % </p>
                  </div>
                </div>
                <div class="fig" id="fi2">
                  <div class="fig-header"/>
                  <div class="fig-content">
                    <div class="image-float">
                      <img src="1961454n.jpg"/>
                    </div>
                  </div>
                  <div class="figure-notes">
                    <p>Tristesse 60 %</p>
                  </div>
                </div>
                <div class="fig" id="fi3">
                  <div class="fig-header"/>
                  <div class="fig-content">
                    <div class="image-float">
                      <img src="1961455n.jpg"/>
                    </div>
                  </div>
                  <div class="figure-notes">
                    <p>Colère 60 %</p>
                  </div>
                </div>
                <div class="fig" id="fi4">
                  <div class="fig-header"/>
                  <div class="fig-content">
                    <div class="image-float">
                      <img src="1961456n.jpg"/>
                    </div>
                  </div>
                  <div class="figure-notes">
                    <p>Dégoût 100 %</p>
                  </div>
                </div>
                <div class="fig" id="fi5">
                  <div class="fig-header"/>
                  <div class="fig-content">
                    <div class="image-float">
                      <img src="1961457n.jpg"/>
                    </div>
                  </div>
                  <div class="figure-notes">
                    <p>Surprise 100 %</p>
                  </div>
                </div>
                <div class="fig" id="fi6">
                  <div class="fig-header"/>
                  <div class="fig-content">
                    <div class="image-float">
                      <img src="1961458n.jpg"/>
                    </div>
                  </div>
                  <div class="figure-notes">
                    <p>Peur 100 %</p>
                  </div>
                </div>
              </div>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_footnotes_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/footnotes/erudit:erudit.ae49.ae04492.1058592ar.xml',
            lxml_etree=True
        )

        result = xml.findall("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='back']/div[@class='footnotes']/div[@class='footnote']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="footnote" id="no1">
              <div class="label">\n            [<a href="#relno1">1</a>]\n        </div>
              <p>Le critère alimentaire devient de moins en moins pertinent dans les sociétés           développées. Il est néanmoins malaisé de distinguer l’ensemble des biens nécessaires de           leur complément, l’ensemble des consommations discrétionnaires, puisque celles-ci           différent d’une classe socioéconomique à l’autre et entre les pays. On notera néanmoins           que la dépense alimentaire était élevée au Canada en 1969 et que le temps de production           domestique lié à l’alimentation reste élevé encore aujourd’hui. On note sur les graphiques           du coefficient budgétaire de l’alimentation par rapport au revenu des ménages que la loi           de Engel joue pour toutes les cohortes, mais de manière différente et par ailleurs           amoindrie pour les plus jeunes. Une estimation de cette loi sur l’ensemble de la           population est donc biaisée par cette disparité entre générations.</p>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result[0]),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

        result = xml.findall("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='back']/div[@class='footnotes']/div[@class='footnote']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="footnote" id="no16">
              <div class="label">\n            [<a href="#relno16">16</a>]\n        </div>
              <p>On notera que les prix virtuels ont été générés ici par la seule dimension revenu           des variables latentes.</p>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.assertEqual(
            etree.tostring(result[-1]),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_list_relation_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/list-relation/erudit:erudit.rseau67.rseau1465.014422ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//table[@class='def-list']")

        expected = """
            <table xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="def-list">
              <tr>
                <td class="term">
                  <p>V<sub>i</sub></p>
                </td>
                <td class="def">
                  <p>le volume initial de la solution, V<sub>c</sub> (ou V<sub>r</sub>) : le volume du culot ou du rétentat, V<sub>p</sub> : le volume du surnageant ou du perméat.</p>
                </td>
              </tr>
              <tr>
                <td class="term">
                  <p>X<sub>i</sub>, X<sub>c</sub> (ou X<sub>r</sub>), X<sub>p</sub></p>
                </td>
                <td class="def">
                  <p>les valeurs de la DCO ou du COT respectivement dans la charge initiale, dans le culot (ou le rétentat) et le surnageant (ou le perméat moyen).</p>
                </td>
              </tr>
            </table>
        """
        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_media_audio_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/media-audio/erudit:erudit.fr90.fr2310.018371ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='media-audio-group']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="media-audio-group">
              <div class="media-audio-group-caption">
                <div class="label">1</div>
                <div class="caption">
                  <div class="title">In the blindage</div>
                  <p>chant soviétique. Musique : K. Listov ; paroles : A. Surkov ; 1942.</p>
                  <p><i>Durée</i> <i>: 2            min 58 s</i></p>
                </div>
              </div>
              <div class="media_print_note">media disponible au: <a href="http://id.erudit.org/iderudit/018371ar">http://id.erudit.org/iderudit/018371ar</a></div>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )


    def test_media_video_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/media-video/erudit:erudit.im118.im01309.1024116ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='media-video-group']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="media-video-group">
              <div class="media-video-group-caption">
                <div class="caption">
                  <p>Reproduction vidéo de l’extrait de la naissance de la créature tiré du film\n            <i>Frankenstein</i> écrit et réalisé par J. Searle\n            Dawley pour les productions Edison en 1910. </p>
                </div>
              </div>
              <div class="media_print_note">media disponible au: <a href="http://id.erudit.org/iderudit/1024116ar">http://id.erudit.org/iderudit/1024116ar</a></div>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_ordered_list_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/ordered-list/erudit:erudit.approchesind0522.approchesind01661.1028100ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//ol")

        expected = """
            <ol xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
              <li>
                <p>D’abord, les études portant sur les stratégies de coping des personnes atteintes             de schizophrénie sont beaucoup plus nombreuses que celles portant sur l’adaptation de             façon plus globale. Il semblerait, selon la plupart des auteurs, que la mesure de             stratégies de coping est plus précise que d’examiner l’adaptation comme phénomène plus             large. </p>
              </li>
              <li>
                <p>Il y a une certaine homogénéité dans les échantillons de participants : ces             derniers sont souvent recrutés dans les établissements de soins où ils sont hospitalisés             ou en suivi externe au moment de la collecte des données. Ils ont aussi une certaine             stabilité psychosociale (état mental, statut résidentiel, soutien social, absence de             comorbidité, etc.). Ils sont donc peu représentatifs de la réelle population de             personnes atteintes de schizophrénie.</p>
              </li>
              <li>
                <p>Les études se regroupent autour des thèmes suivants : les facteurs influençant le             coping, les stratégies de coping pour faire face aux symptômes, les stratégies de coping             pour faire face aux évènements stressants de la vie et les changements dans les             stratégies de coping au fil du temps. On retrouve des recherches en sciences             infirmières, mais la plupart sont publiées dans des revues du domaine des neurosciences,             de la psychologie et de la psychiatrie. </p>
              </li>
              <li>
                <p>Bien que le modèle de Roy ait été utilisé comme cadre de référence dans plusieurs             études dans le domaine de la santé mentale ou de la psychiatrie, aucune, à notre             connaissance, ne porte précisément sur le processus d’adaptation des personnes touchées             par la schizophrénie. Le modèle dominant appliqué à ce sujet de recherche est celui de             Lazarus et Folkman (1984), centré sur l’adaptation au stress.</p>
              </li>
              <li>
                <p>Les études portant sur l’adaptation comme un résultat mesurent des indicateurs             d’adaptation (comme le fonctionnement social). Par exemple, dans l’étude de Clinton,             Lunney, Edwards, Weir et Barr (1998), on évalue l’adaptation à l’aide d’instruments             mesurant les symptômes psychiatriques, le fonctionnement dans la communauté (par             exemple, se vêtir convenablement, avoir un contact visuel adéquat, etc.) ainsi que les             insatisfactions et problèmes quotidiens. Ces indicateurs, établis par les chercheurs et             autres experts, sont censés démontrer ce que signifie « être adapté ». Qu’en est-il des             indicateurs du point de vue des personnes étudiées?</p>
              </li>
              <li>
                <p>On observe une volonté certaine de tenter de catégoriser les innombrables             stratégies de coping. Les catégories sont souvent dichotomiques, donc étiquetées en             termes « bonnes » vs « mauvaises » (ou « adaptées » vs « non adaptées ») : actives ou             passives, centrées sur le problème ou centrées sur les émotions, d’évitement ou de             confrontation, etc.</p>
              </li>
              <li>
                <p>Enfin, l’adaptation des personnes atteintes de schizophrénie n’est pas étudiée             selon une représentation sociale dont une meilleure compréhension pourrait aider à             interpréter les actions de ces personnes.</p>
              </li>
            </ol>
        """
        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_unordered_list_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/unordered-list/erudit:erudit.ae49.ae01086.1021504ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//ul")

        expected = """
            <ul xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">
              <li>
                <p><i>Les fumeurs </i>– La majorité des expériences           montre une relation entre l’usage de tabac et la fonction d’actualisation, établissant que           les fumeurs sont caractérisés par un prix psychologique du temps plus important (Backer           <i>et al.</i>, 2003; Kirby et Perty, 2004; Ohmura           <i>et al.,</i> 2005).</p>
              </li>
              <li>
                <p><i>Les alcooliques </i>– Les études font           apparaître que les alcooliques ont un prix psychologique du temps plus élevé. À titre           d’exemple, les alcooliques sérieux actualisent davantage les gains que les alcooliques           abstinents (Petry, 2001, 2002). Les alcooliques-dépendants désintoxés ont aussi un prix           psychologique du temps plus important que les alcooliques contrôlés (Bjork <i>et al.</i>, 2004).</p>
              </li>
              <li>
                <p><i>Les utilisateurs de drogues illicites </i>–           Selon des études récentes (Bretteville-Jensen, 1999; Kirby et Petry, 2004), il existe une           relation positive entre le prix psychologique du temps et les usages de drogues illicites           principalement la cocaïne, l’héroïne et les amphétamines.</p>
              </li>
              <li>
                <p><i>Les joueurs </i>– Les joueurs pathologiques ont           aussi un prix psychologique du temps plus élevés que la population. Petry (2004) montre           notamment que les joueurs avec une grande fréquence de jeux au cours des trois mois           précédent l’expérience ont un taux d’actualisation très élevé.</p>
              </li>
              <li>
                <p><i>L’âge</i> – Les expériences appliquées montrent           que la patience augmente avec l’âge, les jeunes accordant un prix psychologique du temps           très faible en comparaison avec une population plus âgée (Green <i>et al.</i>, 1994). Toutefois, Read et Read (2004) mettent en           évidence que les adultes les plus âgés (en moyenne 75 ans) représentent le groupe de           population le plus patient lorsque les délais de temps sont inférieurs à 1 an. Cependant,           cette étude montre aussi que les plus âgés sont aussi le groupe de population le moins           patient lorsqu’il s’agit de délais de 3 à 10 ans. Ces résultats laissent apparaître que           les individus les plus âgés sont particulièrement sensibles à un risque de mortalité à           l’horizon de 3 à 10 ans.</p>
              </li>
              <li>
                <p>Les <i>aptitudes cognitives</i> – Elles ont un           rôle singulièrement souligné par Frederick (2005). Il utilise dans un test expérimental un           indice de réflexion cognitive (CRT « <i>Cognitive reflection           test</i> ») qui oppose des individus qui formulent des réponses intuitives sans           réfléchir à ceux qui font des choix ou prennent des décisions réfléchies. Cet indice est           croisé sur un échantillon de 3 428 répondants avec deux dimensions importantes des choix :           la préférence temporelle et l’attitude envers le risque (aversion ou attrait). Le premier           résultat est de montrer que l’indice de réflexion cognitive est lié à la patience : plus           les individus sont réfléchis et ont une capacité d’analyse, plus ils sont alors patients.           Le lien entre le CRT et l’attitude envers le risque est aussi établi. Les individus avec           un fort CRT sont plus tolérants au risque<sup><a href="#no36" id="relno36" class="xref">36</a></sup>.</p>
              </li>
              <li>
                <p>Le <i>genre</i> est aussi un trait fondamental           dans l’évaluation psychologique du temps. Frederick (2005) a montré que le niveau de CRT           dépend du genre. Les femmes ont un CRT plus bas 1,01 que celui des hommes 1,47. Le score           CRT est ici très corrélé avec la préférence temporelle pour les femmes.</p>
              </li>
              <li>
                <p><i>Être riscophobe </i>semble aussi exercer une           influence. Pour Frederick (2005), il existe un facteur commun derrière la préférence pour           le temps et le risque. « <i>Les préférences pour le temps et le           risque sont parfois liées si fortement dans la mesure des capacités cognitives qu’ils en           constituent en eux-mêmes une mesure directe</i> »<sup><a href="#no37" id="relno37" class="xref">37</a></sup>. Cette piste intéressante conduit à se poser la question de savoir si les           deux dimensions de l’aversion au risque et de la structure de préférence temporelle           seraient liées.</p>
              </li>
            </ul>
        """
        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_verbatim_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/verbatim/erudit:erudit.alterstice02303.alterstice03139.1040609ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='verbatim']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="verbatim">
              <p>[...] même si le travailleur immigrant est syndiqué, souvent il ne sait pas qu’il               peut recourir à son syndicat pour négocier son retour au travail, son aménagement de               poste.</p>
              <div class="attrib">Charlie, 34, conseiller en réadaptation</div>
            </div>
        """
        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_styled_content_center_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/styled-content-center/erudit:erudit.cuizine102.cuizine0566.1015495ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//center")

        expected = """<center xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML">***</center>"""

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_table_as_image_center_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/table-as-images/erudit:erudit.ipme114.ipme3878.044029ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='table-wrap']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="table-wrap" id="ta1">
              <div class="table-wrap-header">
                <div class="label">Tableau 1</div>
                <div class="title">Définitions et concepts</div>
              </div>
              <div class="table-wrap-content">
                <div class="image-float">
                  <img src="044029art001n.png"/>
                </div>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_table_as_text_center_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/table-as-text/erudit:erudit.rseau67.rseau3590.038923ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='table-wrap']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="table-wrap" id="ta1">
              <div class="table-wrap-header">
                <div class="label">Tableau 1</div>
                <div class="title">Structure et propriétés chimiques des composés étudiés au cours de ce travail.</div>
                <div class="title">Chemical structure and properties of the compounds studied in the present work.</div>
              </div>
              <div class="table-wrap-content">
                <table>
                  <colgroup>
                    <col align="center"/>
                    <col align="center"/>
                    <col align="center"/>
                    <col align="center"/>
                    <col align="center"/>
                    <col align="center"/>
                    <col align="center"/>
                  </colgroup>
                  <thread>
                    <tr>
                      <th align="center">Nom</th>
                      <th align="center">Estradiol</th>
                      <th align="center">Ethinylestradiol</th>
                      <th align="center">Progestérone</th>
                      <th align="center">Testostérone</th>
                      <th align="center">Diclofénac</th>
                      <th align="center">Naproxen</th>
                    </tr>
                  </thread>
                  <tbody>
                    <tr>
                      <td align="center">Structure chimique</td>
                      <td align="center">
                        <span class="inline-graphic">
                          <img src="038923aro010n.png"/>
                        </span>
                      </td>
                      <td align="center">
                        <span class="inline-graphic">
                          <img src="038923aro011n.png"/>
                        </span>
                      </td>
                      <td align="center">
                        <span class="inline-graphic">
                          <img src="038923aro012n.png"/>
                        </span>
                      </td>
                      <td align="center">
                        <span class="inline-graphic">
                          <img src="038923aro013n.png"/>
                        </span>
                      </td>
                      <td align="center">
                        <span class="inline-graphic">
                          <img src="038923aro014n.png"/>
                        </span>
                      </td>
                      <td align="center">
                        <span class="inline-graphic">
                          <img src="038923aro015n.png"/>
                        </span>
                      </td>
                    </tr>
                  </tbody>
                  <tbody>
                    <tr>
                      <td align="center">Abréviation</td>
                      <td align="center">
                        <b>E2</b>
                      </td>
                      <td align="center">
                        <b>EE2</b>
                      </td>
                      <td align="center">
                        <b>PR</b>
                      </td>
                      <td align="center">
                        <b>TE</b>
                      </td>
                      <td align="center">
                        <b>DF</b>
                      </td>
                      <td align="center">
                        <b>NAP</b>
                      </td>
                    </tr>
                  </tbody>
                  <tbody>
                    <tr>
                      <td align="center">Masse molaire</td>
                      <td align="center">272,4 g•mol<sup>‑1</sup></td>
                      <td align="center">296,4 g•mol<sup>‑1</sup></td>
                      <td align="center">314,4 g•mol<sup>‑1</sup></td>
                      <td align="center">288,4 g•mol<sup>‑1</sup></td>
                      <td align="center">296,4 g•mol<sup>‑1</sup></td>
                      <td align="center">230,2 g•mol<sup>‑1</sup></td>
                    </tr>
                    <tr>
                      <td align="center">Solubilité dans l’eau</td>
                      <td align="center">13 mg•L<sup>‑1</sup></td>
                      <td align="center">4,8 mg•L<sup>‑1</sup></td>
                      <td align="center">7 mg•L<sup>‑1</sup></td>
                      <td align="center">18 - 25 mg•L<sup>‑1</sup></td>
                      <td align="center">ND</td>
                      <td align="center">ND</td>
                    </tr>
                    <tr>
                      <td align="center">pKa</td>
                      <td align="center">10,4</td>
                      <td align="center">10,4</td>
                      <td align="center">Aucun</td>
                      <td align="center">17,4</td>
                      <td align="center">4,0 ‑ 4,2</td>
                      <td align="center">4,15 ‑ 4,70</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_table_group_center_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/table-group/erudit:erudit.ipme114.ipme01875.1030479ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//div[@class='table-wrap-group']")

        expected = """
            <div xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" class="table-wrap-group">
              <div class="table-wrap-group-content">
                <div class="table-wrap" id="ta1">
                  <div class="table-wrap-header">
                    <div class="label">Tableau 1</div>
                    <div class="title">Les publications sur le thème du capital social par revue</div>
                  </div>
                  <div class="table-wrap-content">
                    <div class="image-float">
                      <img src="5031289n.jpg"/>
                    </div>
                  </div>
                </div>
                <div class="table-wrap" id="ta2">
                  <div class="table-wrap-content">
                    <div class="image-float">
                      <img src="5031290n.jpg"/>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        """

        parser = etree.XMLParser(remove_blank_text=True)

        self.assertEqual(
            etree.tostring(result),
            etree.tostring(etree.fromstring(expected, parser=parser))
        )

    def test_text_bigger_sample_corpus(self):

        xml = converters.eruditarticle2html(
            source=APP_PATH + '/fixtures/sample_corpus/text-bigger/erudit:erudit.meta15.meta0694.1017083ar.xml',
            lxml_etree=True
        )

        result = xml.find("body/div[@class='document']/div[@class='article']/div[@class='body_back']/div[@class='body']//big").text

        self.assertEqual(result, "contractus")