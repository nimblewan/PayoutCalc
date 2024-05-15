from flask import Flask, request, render_template
import numpy as np
from scipy.optimize import fsolve
import math

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    # Set default values
    total_players_default = 10
    entry_fee_default = 11
    percent_field_paid_default = 40

    if request.method == 'POST':
        total_players_default = int(request.form.get('total_players'))
        entry_fee_default = int(request.form.get('entry_fee'))
        percent_field_paid_default = int(request.form.get('percent_field_paid'))

    total_players = total_players_default
    entry_fee = entry_fee_default
    percent_field_paid = percent_field_paid_default / 100.0

    purse = total_players * entry_fee
    winners = math.floor(total_players * percent_field_paid)

    a, prizes = calculate_prizes(entry_fee, purse, winners)
    total_payout = sum(prizes)

    # Check if the total payout equals the purse
    if total_payout < purse:
        prizes[0] += purse - total_payout
    elif total_payout > purse:
        prizes[0] -= total_payout - purse

    total_payout = sum(prizes)  # Recalculate the total payout

    return render_template('form.html', winners=winners, prizes=prizes, total_players_default=total_players_default, entry_fee_default=entry_fee_default, percent_field_paid_default=percent_field_paid_default, purse=purse, total_payout=total_payout)

def calculate_prizes(E, P, W):
    def equation(a):
        eq = sum([a*(W-1-x)**2 + E for x in range(W)]) - P
        return eq

    a = fsolve(equation, (1))[0]
    prizes = [round(a*(W-1-x)**2 + E) for x in range(W)]

    return a, prizes

if __name__ == '__main__':
    app.run(debug=True)
