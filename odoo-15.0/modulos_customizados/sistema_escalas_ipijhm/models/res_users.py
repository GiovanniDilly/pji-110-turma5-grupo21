from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    cpf = fields.Char(string="CPF", size=11, help="Digite o seu CPF sem os pontos")
    telefone = fields.Char(string="Telefone", size=25, help="Digite o telefone no formato (XX) 9XXXX-XXXX")
    data_nascimento = fields.Date(string="Data Nascimento")
    genero = fields.Selection(string="Gênero", selection=[("M", "Masculino"), ("F", "Feminino")])

    solicitacoes_ausencia_ids = fields.One2many("sistema_escalas_ipijhm.solicitacao", "colaborador",
                                                string="Solicitações de Ausência", readonly=True)
