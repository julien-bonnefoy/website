import numpy as np
import re
import pycountry


def adjust_status(df, status_column):
    df.loc[:, status_column] = np.where(df[status_column] == "N", 'inactif', 'actif')
    return df


def adjust_suppliers_names(df, suppliers_column):
    df[suppliers_column] = df[suppliers_column].apply(lambda supplier: re.sub("/Coopnet", "", supplier) if isinstance(supplier, str) else float('Nan'))
    df[suppliers_column] = df[suppliers_column].apply(
        lambda supplier: re.sub("Direction Formation et Professionnalisation DEF", "DFP DEF", supplier) if isinstance(supplier, str) else float('Nan'))
    return df


def adjust_types_names(df, type_column):
    df.set_index(type_column, drop=False, inplace=True)
    df.loc['Formation en ligne', type_column] = 'En ligne'
    df.loc['Parcours de formation', type_column] = 'Parcours'
    df.reset_index(drop=True, inplace=True)
    return df


def adjust_languages(df, languages_column):
    lg_dict = {}
    for lg in pycountry.languages:
        if hasattr(lg, "alpha_2"):
            lg_dict[f"{lg.alpha_2}"] = lg.name

    # "Galician" to "Spanish"
    lg_dict["gl"] = "Spanish"

    df[languages_column] = df[languages_column].apply(lambda language: lg_dict[language])

    return df

columns_dict = {
    'numero_de_reference_de_la_formation': {
        'name': 'Numéro de référence de la formation',
        'new_name': 'lo_nb',
        'type': 'object'
    },
    'type_de_formation': {
        'name': 'Type de formation',
        'new_name': 'lo_type',
         'type': 'object'
    },
    'titre_de_la_formation': {'name': 'Titre de la formation',
                              'new_name': 'lo_title',
                              'type': 'object'},
    'numero_d_evenement': {'name': 'Numéro d événement',
                           'new_name': 'event_nb',
                           'type': 'object'},
    'fournisseur_de_formations': {'name': 'Fournisseur de formations',
                                  'new_name': 'supplier',
                                  'type': 'object'},
    'heures_de_formation': {'name': 'Heures de formation',
                            'new_name': 'training_hours',
                            'type': 'float64'},
    'id_de_l_objet_de_formation': {'name': 'ID de l objet de formation',
                                   'new_name': 'lo_id',
                                   'type': 'object'},
    'description_de_la_formation': {'name': 'Description de la formation',
                                    'new_name': 'lo_description',
                                    'type': 'object'},
    'nom_du_type_de_ressource': {'name': 'Nom du type de ressource',
                                 'new_name': 'resource_type',
                                 'type': 'object'},
    'objectifs': {'name': 'Objectifs', 'new_name': 'goal', 'type': 'object'},
    'langue': {'name': 'Langue', 'new_name': 'language', 'type': 'object'},
    'approbation_requise_a_l_inscription': {'name': 'Approbation requise à l inscription',
                                            'new_name': 'need_approbation',
                                            'type': 'object'},
    'niveau': {'name': 'Niveau', 'new_name': 'level', 'type': 'object'},
    'type_d_action_de_formation': {'name': 'Type d action de formation',
                                   'new_name': 'action_type',
                                   'type': 'object'},
    'cette_formation_integre_t_elle_du_digital': {'name': 'Cette formation intègre-t-elle du digital ?',
                                                    'new_name': 'contains_digital',
                                                    'type': 'object'},
    'formation_certifiante': {'name': 'Formation certifiante',
                              'new_name': 'certifying',
                              'type': 'object'},
    'contenu_certifiant': {'name': 'Contenu certifiant',
                           'new_name': 'certifying_content',
                           'type': 'object'},
    'periode_de_validite': {'name': 'Période de validité',
                            'new_name': 'validity',
                            'type': 'object'},
    'type_de_certification': {'name': 'Type de certification',
                              'new_name': 'certif_type',
                              'type': 'object'},
    'eligibilite_du_dispositiff': {'name': 'Eligibilité du dispositif',
                                  'new_name': 'eligibility',
                                  'type': 'object'},
    'categorie': {'name': 'Catégorie',
                  'new_name': 'category',
                  'type': 'object'},
    'fournisseur_externe': {'name': 'Fournisseur externe',
                            'new_name': 'external_supplier',
                            'type': 'object'},
    'commande_externe': {'name': 'Commande externe',
                         'new_name': 'external_order',
                         'type': 'object'},
    'code_formation': {'name': 'Code formation',
                       'new_name': 'program_code',
                       'type': 'object'},
    'matieres_de_la_formation_parente': {'name': 'Matières de la formation parente',
                                         'new_name': 'parent_subject',
                                         'type': 'object'},
    'matieres_de_la_formation': {'name': 'Matières de la formation',
                                 'new_name': 'subject',
                                 'type': 'object'},
    'competences_pour_la_formation': {'name': 'Compétences pour la formation',
                                      'new_name': 'lo_skills',
                                      'type': 'object'},
    'aptitudes_pour_la_formation': {'name': 'Aptitudes pour la formation',
                                    'new_name': 'capabilities',
                                    'type': 'object'},
    'formation_active': {'name': 'Formation active',
                         'new_name': 'active_status',
                         'type': 'object'},
    'inscription_a_plusieurs_sessions_autorisee': {'name': 'Inscription à plusieurs sessions autorisée',
                                                   'new_name': 'multi_sessions_signup_ok',
                                                   'type': 'object'},
    'suivi_d_interet_autorise': {'name': 'Suivi d intérêt autorisé',
                                 'new_name': 'followup_ok',
                                 'type': 'object'},
    'administrateur_de_la_session_de_formation': {'name': 'Administrateur de la session de formation',
                                                  'new_name': 'session_admin',
                                                  'type': 'object'},
    'mot_cle': {'name': 'Mot clé', 'new_name': 'lo_keyword', 'type': 'object'},
    'contact_de_formation': {'name': 'Contact de formation',
                             'new_name': 'contact',
                             'type': 'object'},
    'cree_par_nom': {'name': 'Créé par (nom)',
                       'new_name': 'created_by',
                       'type': 'object'},
    'derniere_modification_par': {'name': 'Dernière modification par',
                                  'new_name': 'last_modif_y',
                                  'type': 'object'},
    'date_de_creation_de_la_formation': {'name': 'Date de création de la formation',
                                         'new_name': 'creation_date',
                                         'type': 'datetime64[ns]'},
    'date_de_desactivation_de_la_formation': {'name': 'Date de désactivation de la formation',
                                              'new_name': 'deactivation_date',
                                              'type': 'datetime64[ns]'},
    'date_de_derniere_modification': {'name': 'Date de dernière modification',
                                      'new_name': 'last_modif_date',
                                      'type': 'datetime64[ns]'},
    'Délai d inscription à la formation': {'name': 'Délai d inscription à la formation',
                                           'new_name': 'signup_period',
                                           'type': 'float64'},
    'nombre_maximal_d_inscriptions_a_la_formation': {'name': 'Nombre maximal d inscriptions à la formation',
                                                     'new_name': 'max_attendees',
                                                     'type': 'float64'},
    'nombre_minimal_d_inscriptions_a_la_formation': {'name': 'Nombre minimal d inscriptions à la formation',
                                                     'new_name': 'min_attendees',
                                                     'type': 'float64'},
    'commentaires': {'name': 'Commentaires',
                     'new_name': 'comments',
                     'type': 'object'},
    'gestion_automatique_de_la_liste_d_attente': {'name': 'Gestion automatique de la liste d attente',
                                                  'new_name': 'auto_wait_list',
                                                  'type': 'object'},
    'gestion_automatique_de_la_liste_d_attente1': {'name': 'Gestion automatique de la liste d attente1',
                                                   'new_name': 'auto_wait_list1',
                                                   'type': 'object'},
    'listes_d_attente_autorisees': {'name': 'Listes d attente autorisées',
                                    'new_name': 'wait_lists_ok',
                                    'type': 'object'},
    'formateur': {'name': 'Formateur', 'new_name': 'trainer', 'type': 'object'},
    'prerequis_de_la_formation': {'name': 'Prérequis de la formation',
                                  'new_name': 'prerequisites',
                                  'type': 'object'},
    'ix': {'name': 'Index', 'new_name': 'id_pbject', 'type': 'int64'}
}

columns = [
    'index"'
    'Numéro de référence de la formation',
    'Type de formation',
    'Titre de la formation',
    'Numéro d événement',
    'Fournisseur de formations',
    'Heures de formation',
    'ID de l objet de formation',
    'Description de la formation',
    'Nom du type de ressource',
    'Objectifs',
    'Langue',
    'Approbation requise à l inscription',
    'Niveau',
    'Type d action de formation',
    'Cette formation intègre-t-elle du digital ?',
    'Formation certifiante',
    'Contenu certifiant',
    'Période de validité',
    'Type de certification',
    'Eligibilité du dispositif',
    'Catégorie',
    'Fournisseur externe',
    'Commande externe',
    'Code formation',
    'Matières de la formation parente',
    'Matières de la formation',
    'Compétences pour la formation',
    'Aptitudes pour la formation',
    'Formation active',
    'Inscription à plusieurs sessions autorisée',
    'Suivi d intérêt autorisé',
    'Administrateur de la session de formation',
    'Mot clé',
    'Contact de formation',
    'Créé par (nom)',
    'Dernière modification par',
    'Date de création de la formation',
    'Date de désactivation de la formation',
    'Date de dernière modification',
    'Délai d inscription à la formation',
    'Nombre maximal d inscriptions à la formation',
    'Nombre minimal d inscriptions à la formation',
    'Commentaires',
    'Gestion automatique de la liste d attente',
    'Gestion automatique de la liste d attente1',
    'Listes d attente autorisées',
    'Formateur',
    'Prérequis de la formation'
]

names = [
    'lo_nb',
    'lo_type',
    'lo_title',
    'event_nb',
    'supplier',
    'training_hours',
    'lo_id',
    'lo_description',
    'resource_type',
    'goal',
    'language',
    'need_approbation',
    'level',
    'action_type',
    'contains_digital',
    'certifying',
    'certifying_content',
    'validity',
    'certif_type',
    'eligibility',
    'category',
    'external_supplier',
    'external_order',
    'program_code',
    'parent_subject',
    'subject',
    'lo_skills',
    'capabilities',
    'active_status',
    'multi_sessions_signup_ok',
    'followup_ok',
    'session_admin',
    'lo_keyword',
    'contact',
    'created_by',
    'last_modif_y',
    'creation_date',
    'deactivation_date',
    'last_modif_date',
    'signup_period',
    'max_attendees',
    'min_attendees',
    'comments',
    'auto_wait_list',
    'auto_wait_list1',
    'wait_lists_ok',
    'trainer',
    'prerequisites'
]

index_subset = [
    "ID de l objet de formation",
    "Numéro de référence de la formation",
    "Numéro d événement",
    "Code formation"
]

type_subset = [
    'Formation active',
    'Type de formation',
    "Type d action de formation",
    'Cette formation intègre-t-elle du digital ?',
    'Formation certifiante',
    'Contenu certifiant',
    'Type de certification',
    'Catégorie',
    'Commande externe'
]

skill_subset = [
    "Objectifs",
    "Niveau",
    "Matières de la formation parente",
    "Matières de la formation",
    "Compétences pour la formation",
    "Aptitudes pour la formation",
    "Prérequis de la formation"
]

rule_subset = [
    "Approbation requise à l inscription",
    "Eligibilité du dispositif",
    "Inscription à plusieurs sessions autorisée",
    "Suivi d intérêt autorisé",
    "Délai d inscription à la formation",
    "Nombre maximal d inscriptions à la formation",
    "Nombre minimal d inscriptions à la formation",
    "Listes d attente autorisées",
    "Gestion automatique de la liste d attente",
    "Gestion automatique de la liste d attente1"
]

description_subset = [
    "Titre de la formation",
    "Description de la formation",
    "Langue",
    "Mot clé"
]

provider_subset = [
    "Fournisseur de formations",
    "Fournisseur externe",
    "Administrateur de la session de formation",
    "Contact de formation",
    "Créé par (nom)",
    "Dernière modification par",
    "Formateur"
]

time_subset = [
    "Heures de formation",
    "Période de validité",
    "Date de création de la formation",
    "Date de désactivation de la formation"
]
