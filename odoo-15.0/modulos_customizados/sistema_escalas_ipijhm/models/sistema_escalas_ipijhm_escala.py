from odoo import fields, models, api


class SistemaEscalasEscalaModel(models.Model):
    _name = "sistema_escalas_ipijhm.escala"
    _description = "Modelo de escalas"
    _order = "name desc"

    create_date = fields.Datetime(string="Data Criação", readonly=True)

    name = fields.Char(string="Nome da Escala", required=True)

    logo = fields.Image(string="Logo da Escala")

    evento_ids = fields.One2many("sistema_escalas_ipijhm.evento", "escala_id")

    status = fields.Selection(string="Status", selection=[("0", "Sem Eventos"),
                                                          ("1", "Em Andamento"),
                                                          ("2", "Eventos Concluídos")], compute="_status_escala",
                              required=True)

    @api.depends('evento_ids')
    def _status_escala(self):

        for record in self:
            if len(record.evento_ids) == 0:
                record.status = "0"
                continue
            else:
                status_eventos = [x.status for x in record.evento_ids]
                set_status = set(status_eventos)

                if len(set_status) == 1 and status_eventos[0] == "3":
                    record.status = "2"
                    continue
                else:
                    record.status = "1"
                    continue
