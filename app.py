from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'segredo123'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'historico' not in session:
        session['historico'] = []

    if request.method == 'POST':
        try:
            valor = float(request.form['valor'])
            garantido = float(request.form['garantido'])

            if valor > garantido:
                resultado = f"Valor excede o garantido de R$ {garantido:.2f}. Não precisa ajuste."
            else:
                dif = garantido - valor
                v = dif / 0.8
                resultado = f"Valor para ajustar: R$ {v:.2f} (Garantido: R$ {garantido:.2f})"
        except ValueError:
            resultado = "Valor inválido inserido."

        # Salva no histórico
        historico = session['historico']
        historico.append(resultado)
        session['historico'] = historico

        # Salva último garantido
        session['ultimo_garantido'] = garantido

        return redirect(url_for('index'))

    historico = session.get('historico', [])
    garantido_atual = session.get('ultimo_garantido', '')

    rendered = render_template('index.html', historico=historico, garantido_atual=garantido_atual)
    session['historico'] = []

    return rendered

if __name__ == '__main__':
    app.run(debug=True)