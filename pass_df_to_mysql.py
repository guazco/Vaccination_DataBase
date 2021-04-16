##############################################################
# File      :   pass_df_to_mysql.py
# Project   :   PCS3623 - Banco de Dados I
# Date      :   April/2021
##############################################################

import sqlalchemy
from generate_df import *
import real_inf
from sqlalchemy import create_engine
import pymysql

#cria município
print("Lendo arquivo de municípios")
arquivo = 'c3d64a3788342bbdd97d01ef7694f1a0.xlsx'
municipio = Municipio("Município")
municipio.fill_table(arquivo)
municipio.create_df()
df_municipio = municipio.out_df()
# removendo último digito do código do municipio
df_municipio = df_municipio.astype({"Código" : str})
df_municipio['Código'] = df_municipio['Código'].str[:-3]
# ---------------------------------------------------------
df_municipio = df_municipio.drop(df_municipio.loc[645:659].index).astype({"Código" : int}) # para remover o rodapé como "notas" e converter o código para inteiro

#cria o resto daqui pra baixo
print("Lendo arquivo com outros dados")
arquivo_2 = 'part-00000-9cca567b-94bf-4d83-88ae-c2efe6fb4794.c000.csv'
df_other_info = other_info(arquivo_2)
df_other_info = df_other_info.drop(['vacina_fabricante_referencia', 'paciente_endereco_cep'], axis=1) # removendo colunas com muitos vazios
df_other_info = df_other_info.loc[df_other_info['vacina_categoria_codigo'].notnull()].astype({"vacina_categoria_codigo" : str})
df_other_info['vacina_categoria_codigo'] = df_other_info['vacina_categoria_codigo'].str[:-2]
df_other_info = df_other_info.astype({"vacina_categoria_codigo" : int})
df_other_info = df_other_info.loc[df_other_info['paciente_endereco_coIbgeMunicipio'].notnull()].astype({"paciente_endereco_coIbgeMunicipio" : int}) # converte o código de cidade para inteiro
df_other_info = df_other_info.astype({"vacina_categoria_codigo" : int})
df_other_info['vacina_dataAplicacao'] = df_other_info['vacina_dataAplicacao'].str[:-14]

# GENERATING IDS

dose_id = fake_id("dose",10,len(df_other_info["vacina_lote"]))
lab_id = fake_id("lab",5,len(df_other_info["vacina_fabricante_nome"].unique().tolist()))
lab_vac_id = fake_id("lab",5,len(df_other_info["vacina_fabricante_nome"].tolist()))

#cria pessoa
print("Gerando DataFrame Pessoa")
pessoa = Pessoa("Pessoa")
pessoa.fill_table(df_other_info)
pessoa.create_df()
df_pessoa = pessoa.out_df()

#cria vacina
print("Gerando DataFrame Vacina")
vacina = Vacina("Vacina")
vacina.fill_table(df_other_info)
vacina.create_df()
df_vacina = vacina.out_df()

#cria laboratório
print("Gerando DataFrame Laboratorio")
laboratorio = Laboratorio("Laboratorio")
laboratorio.fill_table(df_other_info,lab_id)
laboratorio.create_df()
df_laboratorio = laboratorio.out_df()

#cria dose
print("Gerando DataFrame Dose")
dose = Dose("Dose")
dose.fill_table(df_other_info,dose_id)
dose.create_df()
df_dose = dose.out_df()

#cria Unidade Saúde
print("Gerando DataFrame Unidade Saude")
unidade_saude = Unidade_Saude("Unidade_Saude")
unidade_saude.fill_table(df_other_info)
unidade_saude.create_df()
df_unidade_saude = unidade_saude.out_df()

#cria aplica em
print("Gerando DataFrame Aplica_Em")
aplicada_em = Aplicada_Em("Aplica_Em")
aplicada_em.fill_table(df_other_info,dose_id)
aplicada_em.create_df()
df_aplicada_em = aplicada_em.out_df()

#cria habita em
print("Gerando DataFrame Habita_Em")
habita_em = Habita_Em("Habita_Em")
habita_em.fill_table(df_other_info)
habita_em.create_df()
df_habita_em = habita_em.out_df()

#cria tem
print("Gerando DataFrame Tem")
tem = Tem("Tem")
tem.fill_table(df_other_info,dose_id)
tem.create_df()
df_tem = tem.out_df()

#cria fica no
print("Gerando DataFrame Fica_No")
fica_no = Fica_No("Fica_No")
fica_no.fill_table(df_other_info)
fica_no.create_df()
df_fica_no = fica_no.out_df()

#cria enviada para
print("Gerando DataFrame Enviada_Para")
enviada_para = Enviada_Para("Enviada_Para")
enviada_para.fill_table(df_other_info)
enviada_para.create_df()
df_enviada_para = enviada_para.out_df()

#cria do tipo
print("Gerando DataFrame Do_Tipo")
do_tipo = Do_Tipo("Do_Tipo")
do_tipo.fill_table(df_other_info, dose_id)
do_tipo.create_df()
df_do_tipo = do_tipo.out_df()

#cria porduzida por
print("Gerando DataFrame Produzida_Por")
produzida_por = Produzida_Por("Produzida_Por")
produzida_por.fill_table(df_other_info, lab_vac_id)
produzida_por.create_df()
df_produzida_por = produzida_por.out_df()

# Credentials to database connection ADD
hostname=""
dbname=""
username=""
pwd=""

connection = pymysql.connect(
    host=hostname,
    user=username,
    password=pwd,
    db=dbname
    )
cursor = connection.cursor()

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host=hostname, db=dbname, user=username, pw=pwd))

# Convert dataframe to sql table
print("Criando tabela Pessoa")
df_pessoa['Data_de_Nascimento'] = pd.to_datetime(df_pessoa['Data_de_Nascimento'], format='%Y-%m-%d')
df_pessoa.to_sql('pessoas', engine, index=False,
            dtype={
                'Id' : sqlalchemy.types.VARCHAR(length=64),
                'CPF' : sqlalchemy.types.BIGINT,
                'Nome' : sqlalchemy.types.VARCHAR(length=50),
                'Gênero' : sqlalchemy.types.VARCHAR(length=1),
                'Idade' : sqlalchemy.types.SMALLINT,
                'Data_de_Nascimento' : sqlalchemy.types.DATE,
                'Etnia_código' : sqlalchemy.types.SMALLINT,
                'Etnia' : sqlalchemy.types.VARCHAR(length=15),
                'Ocupação' : sqlalchemy.types.VARCHAR(length=50),
                'Grupo' : sqlalchemy.types.VARCHAR(length=50)

            })
print("Tabela Pessoa criada")

print("Criando tabela Município")
df_municipio.to_sql('municipios', engine, index=False,
                   dtype={
                     'Código' : sqlalchemy.types.INT,
                     'População' : sqlalchemy.types.INT,
                     'Nome' : sqlalchemy.types.VARCHAR(length=30),
                   })
print("Tabela Pessoa criada")

print("Criando tabela Vacinas")
df_vacina.to_sql('vacinas', engine, index=False,
                dtype={
                    'IdVacina' : sqlalchemy.types.SMALLINT,
                    'Nome' : sqlalchemy.types.VARCHAR(length=64)
                })
print("Tabela Vacinas criada")

print("Criando tabela Dose")
df_dose.to_sql('doses', engine, index=False,
              dtype={
                  'IdDose' : sqlalchemy.types.VARCHAR(length=15),
                  'Data de Validade' : sqlalchemy.types.DATE,
                  'Número' : sqlalchemy.types.VARCHAR(length=11)
              })
print("Tabela Doses criada")

print("Criando tabela Unidade Saude")
df_unidade_saude.to_sql('Unidade Saude', engine, index=False,
                       dtype={
                           'IdUBS' : sqlalchemy.types.INT,
                           'Nome' : sqlalchemy.types.VARCHAR(length=60),
                           'Endereco' : sqlalchemy.types.VARCHAR(length=100)
                       })
print("Tabela Unidade Saude criada")

print("Criando tabela Laboratorio")
df_laboratorio.to_sql('laboratorio', engine, index=False,
                     dtype={
                         'IdLaboratorio' : sqlalchemy.types.VARCHAR(length=10),
                         'Pais' : sqlalchemy.types.VARCHAR(length=30),
                         'Nome' : sqlalchemy.types.VARCHAR(length=32)
                     })
print("Tabela Laboratorio criada")

print("Criando tabela Aplicada_Em")
df_aplicada_em.to_sql('Aplicada_em', engine, index=False,
                     dtype={
                         'IdPessoa' : sqlalchemy.types.VARCHAR(length=64),
                         'IdDose' : sqlalchemy.types.VARCHAR(length=15),
                         'Data' : sqlalchemy.types.DATE
                     })
print("Tabela Aplicada_Em criada")

print("Criando tabela Habita_Em")
df_habita_em.to_sql('Habita_Em', engine, index=False,
                   dtype={
                       'IdPessoa' : sqlalchemy.types.VARCHAR(length=64),
                       'IdMunicipio' : sqlalchemy.types.INT
                   })
print("Tabela Habita_Em criada")

print("Criando tabela Tem")
df_tem.to_sql('Tem', engine, index=False,
             dtype={
                 'IdDose' : sqlalchemy.types.VARCHAR(length=15),
                 'IdUBS' : sqlalchemy.types.INT
             })
print("Tabela Tem criada")

print("Criando tabela Fica_No")
df_fica_no.to_sql('Fica_No', engine, index=False,
                 dtype={
                     'IdUBS' : sqlalchemy.types.INT,
                     'IdMunicipio' : sqlalchemy.types.INT
                 })
print("Tabela Fica_No criada")

print("Criando tabela Enviada_Para")
df_enviada_para.to_sql('Enviada_Para', engine, index=False,
                      dtype={
                          'IdVacina' : sqlalchemy.types.SMALLINT,
                          'IdUBS' : sqlalchemy.types.INT
                      })
print("Tabela Enviada_Para criada")

print("Criando tabela Do_Tipo")
df_do_tipo.to_sql('Do_Tipo', engine, index=False,
                 dtype={
                     'IdDose' : sqlalchemy.types.VARCHAR(length=15),
                     'IdVacina' : sqlalchemy.types.SMALLINT
                 })
print("Tabela Do_Tipo criada")

print("Criando tabela Produzida_Por")
df_produzida_por.to_sql('Produzida_Por', engine, index=False,
                       dtype={
                           'IdVacina' : sqlalchemy.types.SMALLINT,
                           'IdLaboratorio' : sqlalchemy.types.VARCHAR(length=10)
                       })
print("Produzida_Por criada")

"""connection = pymysql.connect(
    host=hostname,
    user=username,
    password=pwd,
    db=dbname)
cursor = connection.cursor()

cursor.execute("SELECT * FROM municipios")

for x in cursor:
    print(x)"""
