import dash_html_components as html
import dash_bootstrap_components as dbc

p_1 = html.P([
    "Orange Learning est la plateforme d'apprentissage utilisée pour former les quelques 150.000 employés "
    "que ce soit un nouvel arrivant, un collaborateur souhaitant évoluer ou un autre qui souhaiterait être formé ou "
    "informé sur une nouvelle technologie.",
    html.Br(),
    html.Br(),
    "Cette plateforme est construite \"au-dessus\" de ",
    html.A(" C.S.O.D.", href="https://www.cornerstoneondemand.com"),
    " qui est le ",
    html.A(" L.M.S. (Learning Management System = Système de Gestion de l'Apprentissage)",
           href="https://en.wikipedia.org/wiki/Learning_management_system"),
    " leader du marché mondial."
])

p_2 = html.P("""
Orange a défini 128 métiers et pour chacun d'entre eux, l'ensemble des compétences nécessaires pour les exercer.
""")

p_3 = html.P("""
Pour chaque compétence, il existe une définition globale ainsi que 4 niveaux d'expertise pouvant être atteints.'
""")

p_4 = html.P("""
Un "Learning Object" (objet d'apprentissage) peut être une vidéo, une session de formation, en direct ou non, 
virtuelle ou non, un document texte, une présentation, un atelier, un MOOC etc ...
""")

p_5 = html.P("""
Les objets d'apprentissage sont répertoriés dans une base de données et doivent, en théorie avoir au moins un Titre 
et une Description.
""")

p_6 = html.P([
    "\u00ABDOCUMENTS\u00BB:",
    html.Br(),
    "Ensemble des \"Titre + Description\" des LEARNING OBJECTS.",
    html.Br(),
    html.Br(),
    "\u00ABVOCABULAIRE\u00BB:",
    html.Br(),
    "Ensemble des mots que l'on retrouve dans l'ensemble des documents.",
    html.Br(),
    html.Br(),
    "\u00ABSTOPWORDS\u00BB: Mots qui ne sont pas \"porteurs de sens\" comme les pronoms, les articles, les conjoànctiosn "
    " etc... Ils sont "
    "intégrés 'manuellement' (sous forme de liste personnalisable en fonction es besoins de l'analyse) et sont par "
    "conséquent soustraits automatiquement du vocabulaire. "
    "Les mots 'UTILES' (i.e. sans  \u00AB stopwords \u00BB comme les pronoms, les conjonctions ...) les plus "
    "fréquents ne sont pas forcément les plus "
    "pertinents en raison du contexte. Un moyen de faire ressortir les mots clés est de supprimer les n "
    "mots les plus fréquents du \u00AB vocabulaire \u00BB"
])

p_7 = html.Div(
    [
        html.P(
            "Orange Learning search engine is based on the TITLES of Learning Objects"
            "That is why TITLES should contain the most relevant keywords "
        ),
        html.P(
            "In this part we will compare automatically extracted keywords with words used "
            "in the titles and score the matches",
            className="lead",
        ),
        html.Div(
            [
                "The first algorithm is called   ",
                dbc.Button([" TF/IDF "], id='tfidf_modal_btn', size='sm', color='primary'),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Term Frequency/Inverse Document Frequency"),
                        dbc.ModalBody(
                            "In information retrieval, tf–idf or TFIDF, short for term"
                            " frequency–inverse document frequency, is a numerical "
                            "statistic that is intended to reflect how important a word "
                            "is to a document in a collection or corpus. It is often '"
                            "'used as a weighting factor in searches of information '"
                            "'retrieval, text mining, and user modeling. The tf–idf value'"
                            "' increases proportionally to the number of times a word "
                            "appears in the document and is offset by the number of "
                            "documents in the corpus that contain the word, which helps "
                            "to adjust for the fact that some words appear more "
                            "frequently in general. tf–idf is one of the most popular "
                            "term-weighting schemes today."),
                        dbc.ModalFooter(
                            [html.A(['(WIKIPEDIA)'],
                                    href='https://en.wikipedia.org/wiki/Tf%E2%80%93idf'),
                             dbc.Button("Close", id="tfidf_modal_close_btn", className="ml-auto")]
                        ),
                    ],
                    id="tfidf_modal",
                    centered=True
                ),
                "  which compares occurrences of every term in each descriptions to the occurrences "
                "of those terms amongst all the document"
            ]
        ),
        html.P(
            "As a consequence, words like 'le', 'la', 'du' and so on are so frequent in every "
            "documents that they end at the bottom of the ranking"
        ),
        html.P(
            "On the other hand, 'context-obvious' words ('formation', 'client', 'service') "
            "are on the top of the ranking whereas in this analysis, they shouldn't be "
            "considered as keywords "
        ),
        html.P(
            "That is why you will find a counter widget to eliminate the Top N words of the "
            "analysis to highlight more relevant keywords"
        )
    ]
)

p_8 = html.H6(
    [
        "Vue séparée:".upper(),
        html.Hr(),
        "Les répartitions des \u00ABTYPE\u00BB et \u00ABSTATUT\u00BB sont représentées sur 2 diagrammes différents.",
        html.Hr(),
        "Vue combinée:".upper(),
        html.Hr(),
        "Les répartitions des \u00ABTYPE\u00BB et \u00ABSTATUT\u00BB sont représentées sur le même diagramme (type "
        "\u00ABsunburst\u00BB ce qui réunit les 2 informations. Dans ce cas l'ordre de tri est personnalisable.",
        html.Br(),
        "Vous pouvez choisir de classer d'abord par \u00ABTYPE\u00BB d'objet puis de diviser chaque type par "
        "\u00ABSTATUT\u00BB Actif ou Inactif ou inversement, d'abord séparer les objets Actifs/Inactifs, puis pour "
        "chaque \u00ABSTATUT\u00BB, subdiviser par \u00ABTYPE\u00BB.",
        html.Hr(),
        "Vous pouvez également zoomer/dézoomer sur chaque \u00ABcatégorie/sous-catégories\u00BB en cliquant sur "
        "la partie du disque intérieur que vous souhaitez détailler "
    ]
)
