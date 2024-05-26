from datetime import datetime

from odoo import fields, models, api
from odoo.exceptions import UserError


class SistemaEscalasEventoModel(models.Model):
    _name = "sistema_escalas_ipijhm.evento"
    _description = "Modelo de Eventos"
    _order = "data_horario asc"

    create_date = fields.Datetime(string="Data Criação", readonly=True)

    name = fields.Char(string="Nome do Evento", required=True)
    descricao = fields.Text(string="Descrição do Evento")
    data_horario = fields.Datetime(string="Data e Horário do Evento", required=True)

    escala_id = fields.Many2one("sistema_escalas_ipijhm.escala", string="Escala", required=True)
    atividade_ids = fields.One2many("sistema_escalas_ipijhm.atividade", "evento_id")

    qtd_atividades_pendentes = fields.Integer(string="Qtd. Atividades Pendentes", compute="_qtd_atividades_pendentes",
                                              readonly=True)

    qtd_atividades = fields.Integer(string="Qtd. Atividades", compute="_qtd_atividades",
                                    readonly=True)

    evento_concluido = fields.Boolean(string="Evento foi Concluído?", default=False)
    evento_cancelado = fields.Boolean(string="Evento foi Cancelado?", default=False)

    status = fields.Selection(string="Status", selection=[("0", "Rascunho"),
                                                          ("1", "Publicada"),
                                                          ("2", "Em Andamento"),
                                                          ("3", "Concluída"),
                                                          ("4", "Cancelada"),
                                                          ("5", "Atividades com Erro")], compute="_status_evento",
                              readonly=True)

    def write(self, vals):
        if vals.get('status', "0"):
            vals['status'] = "1"

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

    @api.depends('atividade_ids')
    def _qtd_atividades_pendentes(self):

        for record in self:
            status_atividades = [x.status for x in record.atividade_ids]

            record.qtd_atividades_pendentes = status_atividades.count("0")

    @api.depends('atividade_ids')
    def _qtd_atividades(self):
        for record in self:
            record.qtd_atividade = len([x for x in record.atividade_ids])

    @api.depends('create_date', 'evento_concluido', 'evento_cancelado', 'data_horario')
    def _status_evento(self):

        for record in self:
            if record.evento_cancelado:
                record.status = '4'
                continue
            if record.evento_concluido:
                record.status = '3'
                continue

            atividades_com_erro = [x for x in record.atividade_ids if x.possui_erro]

            if len(atividades_com_erro) > 0:
                record.status = '5'
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
