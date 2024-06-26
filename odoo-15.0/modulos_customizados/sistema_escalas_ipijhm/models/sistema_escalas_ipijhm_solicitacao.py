from odoo import fields, models, api


class SistemaEscalasSolicitacoesModel(models.Model):
    _name = "sistema_escalas_ipijhm.solicitacao"
    _description = "Modelo de Solicitações"
    _order = "id asc"

    create_date = fields.Datetime(string="Data Criação", readonly=True)

    name = fields.Char(string="Nome da Solicitação", compute="_define_nome", readonly=True)
    motivo = fields.Text(string="Motivo da Solicitação", required=True)
    atividades_afetadas = fields.Text(string="Atividades Afetadas", compute="_atividades_afetadas", readonly=True)

    data_inicio = fields.Date(string="Data de Início", required=True)
    data_fim = fields.Date(string="Data do Fim", required=True)

    colaborador = fields.Many2one("res.users", string="Colaborador", default=lambda self: self.env.user, readonly=True)

    colaborador_nome = fields.Char(string="Nome do Colaborador", related="colaborador.name")

    categoria = fields.Selection(string="Categoria", selection=[("0", "Motivos de Saúde"),
                                                                ("1", "Motivos Pessoais"),
                                                                ("2", "Outros Motivos")], required=True)

    status = fields.Selection(string="Status", selection=[("-1", "Rascunho"),
                                                          ("0", "Postado")], default="-1", readonly=True)

    def write(self, vals):
        if vals.get('status') == "-1":
            vals['status'] = "0"

        return super(SistemaEscalasSolicitacoesModel, self).write(vals)

    @api.depends('data_inicio', 'data_fim', 'colaborador_nome', 'categoria')
    def _define_nome(self):

        for record in self:

            try:
                if record["categoria"]:
                    rotulo_categoria = dict(self._fields['categoria'].selection).get(record["categoria"])
                else:
                    rotulo_categoria = ""

                if record['data_inicio']:
                    data_inicio_formatada = record['data_inicio'].strftime(r"%d/%m")
                else:
                    data_inicio_formatada = ""

                if record['data_fim']:
                    data_fim_formatada = record['data_fim'].strftime(r"%d/%m")
                else:
                    data_fim_formatada = ""

                if rotulo_categoria + data_inicio_formatada + data_fim_formatada != "":
                    record['name'] = f"Solicitação de {record['colaborador_nome']}" + \
                                     f" - {data_inicio_formatada} à {data_fim_formatada}, {rotulo_categoria}"
                    continue
                else:
                    record['name'] = ''
                    continue
            except:
                record['name'] = ''

    def _atividades_afetadas(self):

        for record in self:

            mensagem = ""
            atividades_impactadas = self.env['sistema_escalas_ipijhm.atividade'].search(
                [('escalados_ids', '=', self.colaborador.id),
                 ('evento_id.data_horario', '>=', self.data_inicio),
                 ('evento_id.data_horario', '<=', self.data_fim)])

            for ativ in atividades_impactadas:
                if ativ.status in ('-1', '0', '5'):
                    mensagem += \
                        f'→ "{ativ.name}" de "{ativ.evento_id.name}" de data e horário: ' + \
                        f'[{ativ.evento_id.data_horario.strftime("%d/%m/%Y - %H:%M:%S")}] conflitam com esta solicitação. \n'

            record['atividades_afetadas'] = mensagem
