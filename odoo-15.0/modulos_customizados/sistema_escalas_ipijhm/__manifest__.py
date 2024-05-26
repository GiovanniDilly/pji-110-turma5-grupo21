{
    'name': 'Sistemas de Escalas da IPIJHM',
    'version': '1.0.0',
    'author': 'PJI110-TURMA005-GRUPO21',
    'category': 'Contabilidade',
    'summary': """
        Módulo para gerenciar escalas, eventos e os colaboradores na Igreja Presbiteriana Independente Jardim Helena Maria.
    """,
    'description': """
        Módulo para gerenciar escalas, eventos e os colaboradores na Igreja Presbiteriana Independente Jardim Helena Maria.
    """,
    'depends': ['base'],
    'data': [
        'security\\ir.model.access.csv',
        'views\\sistema_escalas_ipijhm_escala.xml',
        'views\\sistema_escalas_ipijhm_evento.xml',
        'views\\sistema_escalas_ipijhm_atividade.xml',
        'views\\sistema_escalas_ipijhm_solicitacao.xml',
        'views\\res_user_sistema_escalas_view.xml',
        'views\\sistema_escalas_ipijhm_menus.xml'
    ],
    'installable': True,
    'auto_install': False,
    "application": True,
    'license': 'LGPL-3',
}
