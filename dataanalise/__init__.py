import base64
import io

import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def retorna_dataFrame(rows):
    df = pd.DataFrame(rows, columns=['mes', 'total_vendas'])
    df = df.sort_values(by='mes')
    y = df['total_vendas'].values

    x = pd.DataFrame(pd.Series(range(1, len(y) + 1)))

    xFuturo = pd.DataFrame(pd.Series(range(1, len(y) + 13)))

    reg = LinearRegression().fit(x, y)
    plt.figure()
    plt.plot(xFuturo[0], reg.predict(xFuturo), 'b')
    plt.xlabel('Mês')
    plt.ylabel('Total de Compras')
    plt.title('Previsão de Compras')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_base64
