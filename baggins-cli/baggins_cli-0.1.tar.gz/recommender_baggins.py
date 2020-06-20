import pandas as pd
import pyodbc
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from flask import Flask, request, redirect, url_for
from flask import render_template, jsonify
from flask_cors import CORS
from flask import request
import json
from collections import namedtuple
from nltk.corpus import stopwords
from flask import make_response
import sys

app = Flask("RecSys")
CORS(app)

server = '35.199.106.130'
database = 'bagginsdb'
username = 'baggins'
password = 'baggins'

strConn = 'DRIVER=MySQL ODBC 8.0 ANSI Driver;SERVER=' + \
    server+';DATABASE='+database+';UID='+username+';PWD=' + password


class oportunidade:
    def __init__(self, id, titulo, descricao, idTipoOportunidade, idAnfitriao, disponibilidadeInicio, disponibilidadeFinal, horasSemanais, requisitos, mediaAvaliacao, salario, score):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.idTipoOportunidade = idTipoOportunidade
        self.idAnfitriao = idAnfitriao
        self.disponibilidadeInicio = disponibilidadeInicio
        self.disponibilidadeFinal = disponibilidadeFinal
        self.horasSemanais = horasSemanais
        self.requisitos = requisitos
        self.mediaAvaliacao = mediaAvaliacao
        self.salario = salario
        self.score = score


def obj_dict(obj):
    return obj.__dict__


@app.route('/recommender/<int:userId>')
def recommendTest(userId):

    # sql connection
    mysql_conn = pyodbc.connect(strConn)
    cursor = mysql_conn.cursor()

    # getting historic
    cursor.execute(
        "SELECT idOportunidade FROM bagginsdb.historico_usuario where idUsuario = ?", userId)

    historic = []
    for row in cursor.fetchall():
        historic.extend([x for x in row])

    validHistoric = len(historic)

    if validHistoric > 0:

        query = "SELECT * FROM bagginsdb.oportunidade"

        df = pd.read_sql(query, mysql_conn)

        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3),
                             min_df=0, stop_words=stopwords.words('portuguese'))

        tfidf_matrix = tf.fit_transform(df['descricao'])

        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        results = {}

        for idx, row in df.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], df['id'][i])
                             for i in similar_indices]

            results[row['id']] = similar_items
            # print(similar_items, file=sys.stderr)

        def item(jobid, score):
            it = df.loc[df['id'] == jobid]
            op = []
            op.extend(it.values.tolist()[0])
            op.append(score)
            oportuni = oportunidade(
                op[0], op[1], op[2], op[3], op[4], op[5], op[6], op[7], op[8], op[9], op[10], op[11])
            return oportuni
            # return json.dumps(oportuni.__dict__)

        recommendResult = []

        for jobId in historic:
            recs = results[jobId]
            resultsss = []
            for rec in recs:
                resultsss.append(item(rec[1], rec[0]))

            recommendResult.append(resultsss)

        recsFinal = []

        cursor.execute(query)
        allOp = cursor.fetchall()

        for row in allOp:
            score = 0
            lenght = 0

            for res in recommendResult:
                for opt in res:
                    if row[0] == opt.id:
                        score = score + opt.score
                        lenght = lenght + 1

            score = score/lenght
            oport = oportunidade(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                score)

            recsFinal.append(oport)

        cursor.execute(
            "SELECT id FROM bagginsdb.anfitriao where idPessoa = ?", userId)

        anfId = cursor.fetchone()

        for jobId in historic:
            for res in recsFinal:
                if jobId == res.id:
                    recsFinal.remove(res)

        recsFinalAnfId = []
        if not anfId is None:
            for ress in recsFinal:
                if anfId[0] != ress.idAnfitriao:
                    recsFinalAnfId.append(ress)
        else:
            recsFinalAnfId.extend(recsFinal)

        recsFinalBiggerScore = []
        for res in recsFinalAnfId:
            if res.score > 0.4:
                recsFinalBiggerScore.append(res)

        recsFinalBiggerScore.sort(key=lambda x: x.score, reverse=True)

        cursor.close()
        mysql_conn.commit()
        mysql_conn.close()

        recs = json.dumps(recsFinalBiggerScore, default=obj_dict)
        r = make_response(recs)
        r.mimetype = 'application/json'

        return r

    else:
        cursor.close()
        mysql_conn.commit()
        mysql_conn.close()

        return 'empityHistoric'


@app.route("/recommender/generatehistoric/<int:jobId>/<int:userId>")
def savejob(jobId, userId):
    conn = pyodbc.connect(strConn)
    cursor = conn.cursor()

    valid = 'true'

    cursor.execute(
        "SELECT idAnfitriao FROM bagginsdb.oportunidade where id = ?", jobId)

    opAnfId = cursor.fetchone()

    cursor.execute(
        "SELECT idPessoa FROM bagginsdb.anfitriao where id = ?", opAnfId)

    userJobId = cursor.fetchone()

    if userJobId[0] == userId:
        valid = 'false'

    cursor.execute(
        "SELECT idOportunidade FROM bagginsdb.historico_usuario where idUsuario = ?", userId)

    historic = []
    for row in cursor.fetchall():
        historic.extend([x for x in row])

    for job in historic:
        if job == jobId:
            valid = 'false'

    if valid == 'true':
        cursor.execute(
            """INSERT INTO bagginsdb.historico_usuario
            (`idUsuario`,`idOportunidade`) VALUES (?,?)""", userId, jobId)

        cursor.close()
        conn.commit()
        conn.close()
        return "job saved!"

    cursor.close()
    conn.commit()
    conn.close()

    return "error"


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
