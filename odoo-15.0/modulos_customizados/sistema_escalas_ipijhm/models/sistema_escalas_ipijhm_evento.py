from datetime import datetime
from odoo.exceptions import UserError

from odoo import fields, models, api


class SistemaEscalasEventoModel(models.Model):
    _name = "sistema_escalas_ipijhm.evento"
    _description = "Modelo de Eventos"
    _order = "data_horario asc"

    create_date = fields.Datetime(string="Data Criação", readonly=True)

    descricao = fields.Text(string="Descrição do Evento", required=True)
    data_horario = fields.Datetime(string="Data e Horário do Evento", required=True)

    escala_id = fields.Many2one("sistema_escalas_ipijhm.escala", string="Escala", required=True)

    evento_concluido = fields.Boolean(string="Evento foi Concluído?", default=False)
    evento_cancelado = fields.Boolean(string="Evento foi Cancelado?", default=False)

    status = fields.Selection(string="Status", selection=[("0", "Rascunho"),
                                                          ("1", "Publicada"),
                                                          ("2", "Em Andamento"),
                                                          ("3", "Concluída"),
                                                          ("4", "Cancelada")], compute="_status_evento", readonly=True)

    def write(self, vals):
        if vals.get('evento_rascunhado', False):
            vals['evento_rascunhado'] = True

        return super(SistemaEscalasEventoModel, self).write(vals)

    def concluir_evento(self):
        for record in self:

            if record.status == '3':
                continue

            if record.status == '4':
                raise UserError("O evento já foi cancelado!")

            record.evento_concluido = True

        return True

    def cancelar_evento(self):
        for record in self:

            if record.status == '4':
                continue

            if record.status == '3':
                raise UserError("O evento já foi concluído!")

            record.evento_cancelado = True

        return True

    @api.depends('create_date', 'evento_concluido', 'evento_cancelado', 'data_horario')
    def _status_evento(self):

        for record in self:
            if record.evento_cancelado:
                record.status = '4'
                continue
            if record.evento_concluido:
                record.status = '3'
                continue

            if not record.create_date:
                record.status = '0'
                continue
            else:
                if datetime.now() >= record.data_horario:
                    record.status = '2'
                    continue
                else:
                    record.status = '1'
                    continue
