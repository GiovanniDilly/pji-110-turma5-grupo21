from datetime import datetime
from odoo.exceptions import UserError

from odoo import fields, models, api


class SistemaEscalasAtividadeModel(models.Model):
    _name = "sistema_escalas_ipijhm.atividade"
    _description = "Modelo de Atividades"
    _order = "name asc"

    create_date = fields.Datetime(string="Data Criação", readonly=True)

    name = fields.Char(string="Nome da Atividade", required=True)
    descricao = fields.Text(string="Descrição da Atividade", required=True)

    evento_id = fields.Many2one("sistema_escalas_ipijhm.evento", string="Evento", required=True)

    status = fields.Selection(string="Status", selection=[("-1", "Rascunho"),
                                                          ("0", "Pendente"),
                                                          ("1", "Concluída"),
                                                          ("2", "Cancelada")], default="-1", readonly=True)

    def write(self, vals):
        if vals.get('status') == "-1":
            vals['status'] = "0"

        return super(SistemaEscalasAtividadeModel, self).write(vals)

    def concluir_atividade(self):
        for record in self:

            if record.status == '1':
                continue

            if record.status == '2':
                raise UserError("A atividade já foi cancelada!")

            record.status = "1"

        return True

    def cancelar_atividade(self):
        for record in self:

            if record.status == '2':
                continue

            if record.status == '1':
                raise UserError("A atividade já foi concluída!")

            record.status = "2"

        return True
