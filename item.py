import json

class item:
    def __init__(self,
                 name=None, price=None, 
                 type=None, category=None, 
                 subcategory=None, date=None, 
                 date_payment=None, account=None,
                 parcelas=None,n_parcelas=None):
        self.name = name
        self.price = price
        self.type = type
        self.category = category
        self.subcategory = subcategory
        self.date = date
        self.date_payment = date_payment
        self.account = account
        self.parcelas = parcelas
        self.n_parcelas = n_parcelas

    def __str__(self):
        return f'{self.name} - {self.price}'

    def __repr__(self):
        return f'{self.name} - {self.price}'
    
    def to_dict(self):
        return {
            'DATA COMPETÊNCIA': self.date,
            'DATA CAIXA': self.date_payment,
            'DESCRIÇÃO': self.name,
            'VALOR': self.price,
            'CONTA': self.account,
            'POTE': self.type,
            'CATEGORIA': self.category,
            'SUBCATEGORIAS': self.subcategory,
            'OBSERVAÇÃO': "-",
            'PARCELAS': self.parcelas,
            'N PARCELA': self.n_parcelas,
            'NATUREZA': '-',
            'AUTOMÁTICO': '-'
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())
    
    def from_dict(self, data):
        self.name = data['DESCRIÇÃO']
        self.price = data['VALOR']
        self.type = data['POTE']
        self.category = data['CATEGORIA']
        self.subcategory = data['SUBCATEGORIAS']
        self.date = data['DATA COMPETÊNCIA']
        self.date_payment = data['DATA CAIXA']
        self.account = data['CONTA']
        self.parcelas = data['PARCELAS']
        self.n_parcelas = data['N PARCELA']

    def from_json(self, data):
        self.from_dict(json.loads(data))

    def set_type(self, type):
        self.type = type
    
    def set_category(self, category):
        self.category = category

    def set_subcategory(self, subcategory):
        self.subcategory = subcategory
    
    def set_date(self, date):
        self.date = date
    
    def set_date_payment(self, date_payment):
        self.date_payment = date_payment

    def set_account(self, account):
        self.account = account
    
    def get_all(self):
        return {
            'name': self.name,
            'price': self.price,
            'type': self.type,
            'category': self.category,
            'subcategory': self.subcategory,
            'date': self.date,
            'date_payment': self.date_payment,
            'account': self.account
        }